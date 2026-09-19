"""Measured composition and conditional outmigration sensitivity, no causal claims."""
import argparse
import importlib.util
import sys
from pathlib import Path
import numpy as np
import pandas as pd


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def age_vector(frame, group, column="net_per_person"):
    rows = frame[frame.group.eq(group)].sort_values("band")
    if rows.band.tolist() != list(range(8)):
        raise ValueError(f"Missing canonical age profile: {group}")
    return np.repeat(rows[column].to_numpy(), [18,7,10,10,10,10,10,26])


def npv(profile, survival, start=25, rate=.03, resident=None):
    ages = np.arange(start, 101)
    exposures = survival.Lx.to_numpy()[start:] / survival.lx.iloc[start]
    if resident is None:
        resident = np.ones(len(ages))
    if len(resident) != len(ages) or np.any(np.diff(resident)>1e-12):
        raise ValueError("Invalid nonreturning resident retention schedule")
    return float(np.sum(profile[start:] * exposures * resident / (1+rate)**(ages-start)))


def retention_after_exit(start, exit_year, exit_fraction):
    if not 0 <= exit_fraction <= 1 or exit_year < 0:
        raise ValueError("Invalid exit scenario")
    return np.where(np.arange(101-start) >= exit_year, 1-exit_fraction, 1.0)


def run(root, out):
    fiscal = root / "infra/immigration-fiscal"
    education_helper_path = fiscal / "education_origin_fiscal_2026_09_19/builder.py"
    E = import_file("projection_education_helper", education_helper_path)
    fingerprints = E.verified_upstream_inputs(root)
    fingerprints[str(education_helper_path)] = E.sha(education_helper_path)
    education_manifest_path = fiscal / "education_origin_fiscal_2026_09_19/derived/manifest.json"
    fingerprints[str(education_manifest_path)] = E.sha(education_manifest_path)
    import json
    education_manifest = json.loads(education_manifest_path.read_text())
    for filename, expected in education_manifest["outputs"].items():
        path = education_manifest_path.parent / filename
        if E.sha(path) != expected:
            raise ValueError(f"Stale education-profile export: {path}")
        fingerprints[str(path)] = expected
    A, AL, arrival = E.configure(root)
    cps = fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    state = A.ext.build(argparse.Namespace(cps_zip=cps))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2)|d.A_AGE.lt(15)).to_numpy()
    bands = np.digitize(d.A_AGE,[18,25,35,45,55,65,75])
    shared, personal, _ = A.matrices(state)
    medical_zip = root / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical, _ = A.read_meps(medical_zip, medical_zip.with_name("h256su.txt"))
    cells, codes, _ = A.donor_model(medical,d,False)
    payer_means = arrival._payer_means(medical,cells)
    exposure = ~(d.PUB.eq(0)&d.PRIV.eq(0)).to_numpy()
    health = np.eye(len(cells))[codes] * exposure[:,None]
    means = cells.mean_public_paid.to_numpy()
    params_path = fiscal / "ledger_absolute_2026_09_17/params/params.json"
    p = AL.Params(params_path,False)
    resid = arrival.resid; state_population = resid.read_state_population()
    groups = {g:state["group"][g]&civilian for g in AL.TARGETS+["third_plus_nh_white","all_native"]}
    ctx = dict(d=d,index=state["index"],n_units=state["n_units"],civilian=civilian,weights=weights,
               heads=d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID"),
               general_services=resid.read_general_services_per_capita(state_population),
               assf=AL.read_assf_k12(arrival.GENEXT/"census_assf_fy2024_summary_tables.xlsx"),
               omb=AL.read_omb_functions(arrival.RESIDUAL/"_cache/omb_hist03z1_fy2027.xlsx"),
               capital=AL.read_cog_capital(arrival.RESIDUAL/"_cache/22slsstab1.xlsx",state_population),
               donor_codes=codes,donor_payer_means=payer_means,exposure=exposure,
               n_civilian=float(weights[civilian,0].sum()),us_resident=p.pick("population",["2024"],"count"),
               consumption_proxy=personal[:,4],off=[],allocation="personal",is_white_ref=groups["third_plus_nh_white"],
               is_target=np.logical_or.reduce([groups[g] for g in AL.TARGETS]))
    charges, dropped, centrals, _, _ = AL.build_charges(ctx,p)
    if any(x is None for x in centrals.values()):
        raise ValueError(f"Missing central fiscal arm: {centrals}")
    net = personal @ A.COEFFICIENTS - health @ means + sum(charges.data[charges.columns.index(f"{k}|{v}")] for k,v in centrals.items())
    canonical_path = fiscal/"ledger_absolute_2026_09_17/derived/age_profiles.csv"
    canonical = pd.read_csv(canonical_path)
    canonical = canonical[canonical.allocation.eq("personal")&canonical.account.eq("expanded")]
    component = pd.read_csv(fiscal/"ledger_absolute_2026_09_17/derived/age_profile_components.csv")
    component = component[component.allocation.eq("personal")&component.account.eq("expanded")&component.component.eq("N")]
    errors = {}
    for group in ["mexico_born","mexican_second_gen","third_plus_nh_white"]:
        use=groups[group]
        actual=np.bincount(bands[use],weights=net[use]*weights[use,0],minlength=8)
        expect=canonical[canonical.group.eq(group)].sort_values("band").net_total.to_numpy()-component[component.group.eq(group)].sort_values("band").signed_total.to_numpy()
        errors[group]=float(np.max(np.abs(actual-expect)))
        if not np.allclose(actual,expect,rtol=1e-10,atol=.10):
            raise ValueError(f"Canonical personal account does not reproduce for {group}: {errors[group]}")
    # Preserve all second-generation respondents; neither unknown nor another
    # foreign birthplace is silently treated as a US-born second parent.
    us=[57,60,66,69,73,78]
    g2=groups["mexican_second_gen"]
    both=(d.PEFNTVTY.eq(303)&d.PEMNTVTY.eq(303)).to_numpy()&g2
    mixed=((d.PEFNTVTY.eq(303)&d.PEMNTVTY.isin(us))|(d.PEMNTVTY.eq(303)&d.PEFNTVTY.isin(us))).to_numpy()&g2
    residual=g2&~both&~mixed
    if not np.array_equal(both.astype(int)+mixed.astype(int)+residual.astype(int),g2.astype(int)):
        raise ValueError("Parentage partition fails")
    subgroups={"two_Mexico_born_parents":both,"one_Mexico_one_US_area_parent":mixed,"other_or_unresolved_parent":residual,"all_Mexican_G2":g2}
    rows=[]
    for name, mask in subgroups.items():
        for band in range(8):
            use=mask&(bands==band); w=weights[use,0]
            if not len(w):
                continue
            pop=float(w.sum()); ess=pop**2/float(w@w)
            rows.append(dict(group=name,band=band,n=int(use.sum()),population=pop,ess=ess,supported=bool(use.sum()>=30 and ess>=20),
                             net_per_person_excluding_N=float(np.average(net[use],weights=w)),
                             below_HS=float(np.average(d.loc[use,"A_HGA"].le(38),weights=w)) if band>=2 else np.nan,
                             BAplus=float(np.average(d.loc[use,"A_HGA"].ge(43),weights=w)) if band>=2 else np.nan))
    mixed_table=pd.DataFrame(rows); mixed_table.to_csv(out/"mixed_parentage_age_profiles.csv",index=False)
    source_survival=fiscal/"lifetime_longevity_sstiming_2026_09_18/derived/survival_tables.csv"
    all_survival=pd.read_csv(source_survival)
    survival=all_survival[all_survival.year.eq(2024)&all_survival.table.eq("total")].sort_values("age")
    if survival.age.tolist()!=list(range(101)):
        raise ValueError("Life table ages must be 0..100")
    mixrows=[]; original=age_vector(canonical,"mexican_second_gen")
    base_g2=mixed_table[mixed_table.group.eq("all_Mexican_G2")].set_index("band")
    for name in ["two_Mexico_born_parents","one_Mexico_one_US_area_parent"]:
        sub=mixed_table[mixed_table.group.eq(name)].set_index("band")
        prof=original.copy()
        if not sub.reindex(range(2,6)).supported.fillna(False).all():
            raise ValueError(f"Mixed-parent working-age profile has insufficient support: {name}")
        for b in range(2,6):
            lo=25+10*(b-2)
            prof[lo:lo+10]+=sub.loc[b,"net_per_person_excluding_N"]-base_g2.loc[b,"net_per_person_excluding_N"]
        for start in [0,25]:
            for rate in [0.,.03,.05]:
                mixrows.append(dict(profile=name,start_age=start,rate=rate,npv=npv(prof,survival,start,rate),
                                    original_G2_npv=npv(original,survival,start,rate),
                                    change_from_original=npv(prof-original,survival,start,rate),
                                    replaced_ages="25-64_only_child_senior_N_held_fixed"))
    pd.DataFrame(mixrows).to_csv(out/"mixed_parentage_lifetime_sensitivity.csv",index=False)
    # Education composition transported to the same current stock's educational
    # profiles; this is a descriptive composition scenario, not entrants' NPV.
    edu_path=fiscal/"education_origin_fiscal_2026_09_19/derived/age_profiles.csv"
    edu=pd.read_csv(edu_path)
    edu=edu[edu.allocation.eq("personal")&edu.account.eq("expanded_excluding_N")&edu.origin.eq("mexico_born")&edu.entry.eq("stock")]
    eds=E.education_masks(d)
    compositions={}
    composition_rows=[]
    for name,selection in [("stock_25_54",np.ones(len(d),bool)),("recent_2016_2025_25_54",d.PEINUSYR.isin([25,26,27,28]).to_numpy())]:
        domain=groups["mexico_born"]&d.A_AGE.between(25,54).to_numpy()&selection
        denom=weights[domain,0].sum()
        shares={k:weights[domain&v,0].sum()/denom for k,v in eds.items() if k!="all"}
        if not np.isclose(sum(shares.values()),1):
            raise ValueError("Education shares fail partition")
        compositions[name]=shares
        composition_rows.extend(dict(domain=name,education=k,share=v,n=int((domain&eds[k]).sum()),population=float(denom)) for k,v in shares.items())
    pd.DataFrame(composition_rows).to_csv(out/"recent_arrival_education_mix.csv",index=False)
    edrows=[]
    for name, shares in compositions.items():
        prof=np.zeros(101); supported=True; working_supported=True
        for ed,share in shares.items():
            block=edu[edu.education.eq(ed)].sort_values("band")
            if block.band.tolist()!=list(range(6)):
                raise ValueError("Missing education fiscal profile")
            supported=supported and bool(block.support.all())
            working_supported=working_supported and bool(block[block.band.lt(4)].support.all())
            prof[25:]+=share*np.repeat(block.net_per_person.to_numpy(),[10,10,10,10,10,26])
        if not working_supported:
            raise ValueError("Working-age education mixture lacks adequate cell support")
        common_senior=edu[edu.education.eq("all")].sort_values("band").net_per_person.to_numpy()
        working_only=prof.copy(); working_only[65:]=np.repeat(common_senior[4:],[10,26])
        for label, vector, status in [("working_age_mix_common_senior",working_only,True),("all_age_mix_sparse_senior_diagnostic",prof,supported)]:
            for rate in [0.,.03,.05]:
                edrows.append(dict(composition=name,rate=rate,npv_age25=npv(vector,survival,25,rate),all_age_education_cells_supported=status,account="expanded_excluding_N_F",profile=label))
    pd.DataFrame(edrows).to_csv(out/"arrival_mix_lifetime_sensitivity.csv",index=False)
    # NRC's approximately30% return share is an old all-origin assumption, not
    # measured Mexican exit probability. Timing and children-left-behind differ.
    founder=age_vector(canonical,"mexico_born")
    ss_ratio=p.admin_over_survey("underreporting",[["social_security"],["social","security"],["oasdi"]],"social_security",preferred="ratio_social_security")
    ss_bands=[]
    for band in range(8):
        use=groups["mexico_born"]&(bands==band)
        ss_bands.append(float(np.average(d.loc[use,"SS_VAL"]*ss_ratio,weights=weights[use,0])))
    ss_profile=np.repeat(ss_bands,[18,7,10,10,10,10,10,26])
    exitrows=[]
    for exit_year in [5,10,20,40]:
        for fraction in [0.,.30]:
            retention=retention_after_exit(25,exit_year,fraction)
            for rate in [0.,.03,.05]:
                base=npv(founder,survival,25,rate)
                val=npv(founder,survival,25,rate,retention)
                cost=float(np.sum(ss_profile[25:]*survival.Lx.to_numpy()[25:]/survival.lx.iloc[25]
                                  *(1-retention)/(1+rate)**np.arange(76)))
                for keep_ss in [0.,1.]:
                    adjusted=val-keep_ss*cost
                    exitrows.append(dict(exit_year=exit_year,exit_fraction=fraction,rate=rate,retained_SS_profile_share=keep_ss,
                                         founder_npv=adjusted,no_exit_npv=base,change=adjusted-base,
                                         assumption="nonSS_US_flows_stop_after_exit_descendants_not_scaled_SS_profile_is_sensitivity"))
    pd.DataFrame(exitrows).to_csv(out/"return_migration_timing.csv",index=False)
    # Reproduce the century lane's neutral per-capita generation accounting,
    # with current repaired profiles and without its imputed status penalty.
    # Export100 intervals for a century and a101-interval compatibility arm
    # because the original implementation includes calendar indices0..100.
    lane=fiscal/"lineage_cost_2026_09_19"
    I=import_file("projection_lineage_inputs",lane/"inputs.py")
    fingerprints[str(lane/"inputs.py")]=E.sha(lane/"inputs.py")
    fertility=I.fertility()["low_cps2025"]
    fertility_path=I.P_FERT
    fingerprints[str(fertility_path)]=E.sha(fertility_path)
    streams=[]; count=1.; birth=-25
    for gen in range(1,6):
        group="mexico_born" if gen==1 else "mexican_second_gen" if gen==2 else "mexican_third_plus_selfid"
        if gen>1:
            parent="mexico_born" if gen==2 else "mexican_second_gen" if gen==3 else "mexican_third_plus_selfid"
            count*=fertility[parent]/2
            birth=4 if gen==2 else birth+29
        start=25 if gen==1 else 0
        profile=age_vector(canonical,group)
        stream=np.zeros(101)
        for age in range(start,101):
            year=birth+age
            if 0<=year<=100:
                stream[year]=count*profile[age]*survival.Lx.iloc[age]/survival.lx.iloc[start]
        streams.append(stream)
    base_stream=np.sum(streams,axis=0)
    family_rows=[]
    for exit_year in [5,10,20,40]:
        for leave_children in [False,True]:
            alternative=base_stream.copy()
            # Descendants leave only if G2 is still dependent at founder exit.
            departing=[0]
            if leave_children and 0<=exit_year-4<18:
                departing+=list(range(1,5))
            alternative[exit_year:]-=.3*np.sum([streams[i][exit_year:] for i in departing],axis=0)
            ss_stream=np.zeros(101)
            for year in range(exit_year,76):
                age=25+year
                ss_stream[year]=.3*ss_profile[age]*survival.Lx.iloc[age]/survival.lx.iloc[25]
            for keep_ss in [0.,1.]:
                adjusted=alternative-keep_ss*ss_stream
                for rate in [0.,.03,.05]:
                    factor=(1+rate)**-np.arange(101,dtype=float)
                    for horizon in [100,101]:
                        family_rows.append(dict(exit_year=exit_year,exit_fraction=.3,dependent_children_leave=leave_children,
                                                departure_generations=",".join(str(x+1) for x in departing),rate=rate,retained_founder_SS_profile_share=keep_ss,
                                                calendar_intervals=horizon,no_exit_lineage_npv=float(base_stream[:horizon]@factor[:horizon]),
                                                exit_lineage_npv=float(adjusted[:horizon]@factor[:horizon]),change=float((adjusted-base_stream)[:horizon]@factor[:horizon])))
    pd.DataFrame(family_rows).to_csv(out/"lineage_return_migration.csv",index=False)
    return dict(reproduced_group_max_abs_dollar_errors=errors,upstream_fingerprints=fingerprints,
                input_paths=[str(cps),str(medical_zip),str(source_survival),str(edu_path)],
                no_sampling_confidence_claim="New mixture and exit scenarios condition on point profiles; upstream sampling intervals are not model uncertainty.")

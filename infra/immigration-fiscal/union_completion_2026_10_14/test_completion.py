"""Behavioral controls for membership, biological linkage and accounting outputs."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "generation_account_2026_09_24"))
from completion import siblings
import frame as F


def read(name):
    return json.loads((HERE / "derived" / name).read_text())


def test_observed_weights_and_generation_classes_do_not_overlap():
    counts = read("count_replicates.json")
    central = np.array(counts["reporter_central_by_age"])
    all_n = np.array(counts["reporter_all_by_age"])
    third = np.array(counts["observed_g3_rate_by_age"])
    later = np.array(counts["observed_later_by_age"])
    assert central.shape == all_n.shape == third.shape == later.shape == (17,161)
    assert np.all(all_n >= central)
    assert np.all(third >= 0) and np.all(later >= 0)
    assert abs((third+later)[:,0].sum()-read("summary.json")["identity_loss"]["biological"]["nonreporters"]["estimate"]) < 1e-6
    assert read("summary.json")["counts"]["two_US_parent_omitted_records"] == 0


def test_parent_linkage_excludes_step_and_two_native_parent_pairs():
    d = pd.DataFrame(dict(PH_SEQ=[1]*4, A_LINENO=[1,2,3,4], PEPAR1=[0,0,1,1], PEPAR2=[0,0,2,2],
                          PEPAR1TYP=[0,0,1,1],PEPAR2TYP=[0,0,1,2], PENATVTY=[57,313,57,57],
                          PRCITSHP=[1,5,1,1],PRDTHSP=[1,0,1,0],A_AGE=[40,40,10,10],
                          PEFNTVTY=[57,313,57,57],PEMNTVTY=[57,313,313,313]))
    union = np.array([True,False,False,False])
    arms, mex, _ = siblings(d,F,np.ones(4,bool),union)
    assert np.array_equal(arms["biological"], [False,False,True,False])
    assert np.array_equal(arms["all_parent_types"] & ~mex,[False,False,False,True])
    d.loc[1,"PENATVTY"] = 57
    d.loc[2:,"PEMNTVTY"] = 57
    arms, _, _ = siblings(d,F,np.ones(4,bool),union)
    assert not arms["all_parent_types"].any()


def test_original_case_and_national_tax_positive_controls():
    gates = read("gates.json")
    assert all(g["passed"] for g in gates)
    case = [g for g in gates if "union reproduced every replicate" in g["gate"]]
    assert len(case) == 4
    assert max(g["max_gap_bn"] for g in case) < 1e-6
    jobs = [g for g in gates if g["gate"].startswith("job ")]
    assert len(jobs) == 6
    assert all(g["max_gap_bn"] < 1e-6 for g in jobs)


def test_credit_difference_recomputed_on_joint_expansion():
    s = read("credits_interaction.json")["results"]
    base = np.array(s["canonical"]["replicate_net_bn"])
    for name,r in s.items():
        if name != "canonical":
            assert np.allclose(np.array(r["replicate_net_bn"])-base,r["replicate_delta_bn"],rtol=0,atol=1e-12)
    assert s["one_us_parent_plus_observed"]["delta_bn"] < .5
    assert s["all_outsiders_plus_observed"]["delta_bn"] < .5


def test_candidate_counts_prices_and_materiality_close():
    candidate = read("candidate.json")
    kernel = read("summary.json")
    base_n = candidate["counts"]["baseline"]
    for basis,ends in candidate["results"].items():
        for end,r in ends.items():
            base_cost = kernel["pricing"][basis][end]["engine_bn"]
            for name,arm in r["arms"].items():
                extra = candidate["counts"]["reporting_additions"][name.split("_")[0]]["estimate"]
                assert abs(arm["candidate_bn"]-base_cost-arm["delta_bn"]["estimate"]) < 1e-6
                assert abs(arm["identified_union_people"]["estimate"]-base_n["account_union"]-extra) < 1e-6
                assert abs(arm["lineage_people"]["estimate"]-base_n["lineage_population"]-extra
                           -arm["additional_nonreporters"]["estimate"]) < 1e-6
                assert isinstance(arm["passes_5bn_bar"],bool)
                assert arm["passes_5bn_bar"] == (abs(arm["delta_bn"]["estimate"])>=5)
                reps = np.array(arm["replicate_delta_bn"])
                assert len(reps) == 161 and np.isfinite(reps).all()

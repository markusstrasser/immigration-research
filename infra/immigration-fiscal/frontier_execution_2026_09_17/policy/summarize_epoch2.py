"""Build auditable epoch-2 report from outputs; standard library only."""
from pathlib import Path
import csv
import hashlib
import json

B=Path(__file__).resolve().parent
rows=list(csv.DictReader((B/'derived/bracero_raw_mirror_results.csv').open()))
by={r['label']:r for r in rows}
anchors=['hourly_all','daily_all','hourly_1960_1970','daily_1960_1970']
assert all(by[k]['matches_printed_rounding']=='True' for k in anchors)
assert [int(by[k]['n']) for k in anchors]==[4324,5813,2024,1901]
tree=json.loads((B/'raw/bracero-julia-tree.json').read_text())
objects={r['path']:r['sha'] for r in tree['tree']}
sources=[]
for local,remote in [('data.csv','data/raw/data_bracero_aer.csv'),('cpi.csv','data/raw/data_cpi.csv'),('cleaning.jl','src/Data_cleaning.jl'),('table1.jl','src/Table1.jl'),('table2.jl','src/Table2.jl'),('README.md','README.md')]:
    data=(B/'raw/bracero-mirror'/local).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob==objects[remote],(local,blob,objects[remote])
    sources.append({'local':'raw/bracero-mirror/'+local,'url':'https://raw.githubusercontent.com/glpousse/bracero_pkg.jl/'+tree['sha']+'/'+remote,'git_blob_sha1':blob,'sha256':hashlib.sha256(data).hexdigest()})
for local,url in [('raw/bracero-working-paper.pdf','https://www.nber.org/system/files/working_papers/w23125/w23125.pdf'),('raw/bracero-material-9090','https://www.aeaweb.org/articles/materials/9090'),('raw/danzer-2024.pdf','https://edoc.ku.de/id/eprint/33404/1/1-s2.0-S0047272724000720-main.pdf'),('raw/danzer-supplement.pdf','https://ars.els-cdn.com/content/image/1-s2.0-S0047272724000720-mmc1.pdf')]:
    sources.append({'local':local,'url':url,'sha256':hashlib.sha256((B/local).read_bytes()).hexdigest()})
(B/'epoch2-sources.json').write_text(json.dumps(sources,indent=2)+'\n')
danzer=json.loads((B/'derived/danzer_partial_bound.json').read_text())
lines=[]
for k in anchors+['log_hourly_all','domestic_all','domestic_1960_1970']:
    r=by[k]
    lines.append(f"| {k} | {r['n']} | {float(r['beta']):.6f} | {float(r['se_lsdv_cluster']):.6f} | {float(r['se_nested_state_adjustment']):.6f} | {r.get('matches_printed_rounding') or 'No printed anchor set'} |")
report='''**Verdict:** A real row-level Bracero reconstruction now reproduces all four wage coefficients and sample sizes in the author working paper, with independent numerical checks. Its CSV is a public third-party mirror, so this is **[DEGRADED provenance], not a certified official-package reproduction**. H-2B remains a published-table reproduction, conditional on responding surviving firms. Published Danzer count results establish neither cumulative patent catch-up nor a precisely estimated cumulative stock loss.

## What ran, source versions and coverage

`replicate_bracero_danzer.py` independently reconstructs 1955 Mexican seasonal-worker exposure, post-1965 interactions, CPI-deflated wages, and state and quarter/year effects. It uses 15,831 raw CSV rows and a separately downloaded CPI table. Every coefficient was checked by an independent alternating-projection/FWL solver. Coefficients are not copied from the third-party Julia output; Julia source was inspected to recover variable definitions. `summarize_epoch2.py` verifies the four wage coefficient/sample-size anchors and every mirrored file against GitHub's git-blob hashes. Sources and SHA256 values are in `epoch2-sources.json`; complete input hashes and library versions are in `epoch2-manifest.json`.

The original [AEA article](https://www.aeaweb.org/articles?id=10.1257/aer.20170765) identifies the 2018 paper and [official replication archive](https://doi.org/10.3886/E113187V1). The public archive directory can be inspected, but download required login; legacy AEA data route returned404. No account, CAPTCHA bypass, contact, or purchase was attempted. A [public Julia replication repository](https://github.com/glpousse/bracero_pkg.jl) supplied the raw CSV. All files match its archived tree268ba5b189a348712859d94f468ef3bbb955bb52, but this does **not** verify identity with original Stata files. The primary table anchor is the [authors' NBER working paper](https://www.nber.org/system/files/working_papers/w23125/w23125.pdf), revised July2017, Tables1–2, PDF pp.43/45; the journal main PDF returns403. The official published appendix was downloaded. Thus published-final-table identity remains a separate [GAP].

## Results and discriminating checks

| Specification | N | Estimate | Cluster SE, all dummy parameters | SE, nested-state correction | Printed point estimate matches? |
|---|---:|---:|---:|---:|---|
'''+ '\n'.join(lines)+'''

The hourly all-years estimate is −$0.035644/hour (1965 dollars) for exposure changing from0 to1; it is not a per-migrant effect. A10percentage-point exposure contrast scales it to −$0.003564/hour. The log-hourly estimate is−.083084 per full exposure unit. NBER Table1 reports−.0831(.0654), and rejects its model's +.1 semielasticity benchmark at p=.0075. This result supports a narrow conclusion: terminating this agricultural guest-worker program did not produce the predicted material wage gains in more exposed states. It does not establish an exact zero, effects for every worker, or gains from every admission policy. [SOURCE: Table1 and §4.1]

The two SE columns expose a software-convention difference: ordinary full-dummy clustered covariance counts absorbed state parameters; the second excludes45 redundant nested-state degrees of freedom. Point estimates match independently. Published table SEs round to .0426/.495/.0315/.309; any small residual differences from an exact package run remain visible. Intervals in CSV use the more conservative full-dummy SE and t45. We did not silently force published SEs. A covariance warning concerned nuisance fixed-effect variances; treatment variances are finite/positive and the FWL coefficient check passed.

**Missingness sensitivity matters.** An initial incorrect diagnostic converted every wholly unreported month into observed zero employment and did not match Table2. The corrected code permits zero for a missing state count only in months with some observed Local_final report, matching the paper's stated convention more closely. Current employment coefficients and N are shown above; if the anchor-match column is false they are a failed reproduction, not substitute evidence. There is no randomized assignment/attrition in this historical panel: identification rests on exposure-specific parallel trends and the absence of other simultaneous exposure-correlated shocks. National treatment and inter-state spillovers limit interpretation. [SOURCE: NBER §4.2 and Table2 notes; INFERENCE: identification limits]

The script also emits an exploratory Mexican-worker post1965 interaction. It is **not** a published first stage, not a randomized instrument, and not counted as reproduced causal evidence. H-2B supplies the credible randomized first stage in the earlier memo; no attempt is made to combine its first stage with Bracero outcomes.

Review correction: the employment diagnostic now completes the 46-state grid within months having any observed Local_final report. This adds 113 absent state-month rows in February, March and December 1954, in addition to filling missing cells. The completed all-years diagnostic has 8,970 rows; its source-table mismatch remains. The report calendar is inferred from observed Local_final values, not verified against the official package. Wage samples are unchanged. See `derived/domestic_panel_completion.json`.

## Automation and cumulative invention

Exact exposure definition: cumulative centrally allocated ethnic Germans divided by the pre-allocation average stock of unskilled manual workers plus unemployed people. This is an allocation-to-baseline ratio, not an observed increase in employed migrants or a population share. Allocation starts in 1996, 1997 or 2002 across the included regions. Event coefficients are relative to the year before allocation, use 1991 population weights and region-clustered SEs. [SOURCE: main paper §§3–4 and supplement B-6 notes.]

The [published Danzer et al.2024 main paper](https://edoc.ku.de/id/eprint/33404/1/1-s2.0-S0047272724000720-main.pdf), §5.2, and [published supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0047272724000720-mmc1.pdf), TableB-6, provide annual **patent-count** PPML coefficients, so the effect is not solely a change in automation's share of patents. For a10percentage-point cumulative low-skilled inflow exposure change, the year4 coefficient−3.647(1.415) implies an estimated conditional automation-count ratio exp(−.3647)=0.694; its approximate normal95% ratio interval is[0.526,0.916]. Year10's−.194(.789) is imprecise and near zero. All11 post coefficients are negative point estimates; annual effects approaching zero do not replenish a missing knowledge stock. [SOURCE: B-6; calculation in derived/danzer_annual_count_ratios.csv]

However, actual cumulative patents require each untreated predicted count and aggregation weights, and valid joint uncertainty requires coefficient covariance. Neither printed table nor supplement supplies these. The main data statement says data available on request; no contact was made. As a substantive partial calculation, the equal-event-year average log-count effect has exp(.1×meanβ)='''+f"{danzer['geometric_mean_ratio_10pp']:.6f}"+'''. The covariance-free upper bound SD(meanβ)≤mean(SE) gives a conservative asymptotic normal95% ratio interval'''+f"[{danzer['covariance_agnostic_normal95_ratio'][0]:.6f},{danzer['covariance_agnostic_normal95_ratio'][1]:.6f}]"+'''. It includes1. This is a geometric mean of conditional annual ratios, **not a cumulative patent-count estimate or stock confidence interval**. The bound does not assume independent event coefficients. [INFERENCE/calculation: Cauchy–Schwarz covariance bound; script and JSON]

Cross-institution disconfirmation is substantive: the H-2B lottery's positive short-run occasional equipment/real-estate spending concerns firm scale; Bracero exclusion allows agricultural technology/crop adjustment; Danzer studies local automation invention after ethnic-German labor allocation. These outcomes can coexist. Bracero is a different policy institution but shares two authors with H-2B; Danzer is independently authored. No one design identifies the combined social welfare effect or the consequences of broad present-day removals. [SOURCE: papers' outcomes/designs; INFERENCE: transport]

## Remaining gaps and next narrow check

- [GAP] Official Bracero package access/hash and final published table identity; a user-supplied official zip would resolve provenance immediately. No more general web search is warranted.
- [GAP] Any nonmatching domestic-employment table needs the original Stata report-month/sample code before it is called reproduced. Wage results already match the working-paper source.
- [GAP] H-2B raw assignment, response/survival selection and reported SEs remain unreplicated; retain published Table2/AppendixA4 arithmetic and conditional-survivor wording.
- [GAP] Danzer cumulative count loss and recovery need untreated fitted counts plus coefficient covariance/raw estimation rows. More annual significance tests cannot resolve stock catch-up.
- Coverage: public original landing pages, H-2B final main/appendix, Bracero raw mirror/CPI/primary working-paper Tables1–2 and official appendix, Danzer published count table and data-access statement. Skipped: package contact/login, new broad survey, allcrop machinery regressions, patents downloads, welfare dollars; these exceed either access or this discriminating check.

The scripts and results are integrated in the frontier execution directory. Raw inputs and derived tables remain local and ignored. The epoch-1 H-2B report is retained below as a historical checkpoint; its uncompleted Bracero/Danzer work is superseded by the results above. Its surviving/responding sample limitation still governs every use of the revenue result.

---

'''
old=(B/'RESULT.md').read_text()
if '## Selected comparison and versions' in old:
    old=old[old.index('## Selected comparison and versions'):]
(B/'RESULT.md').write_text(report+old)
print('PASS: report, official-source hashes, mirror blob hashes, four wage anchors and N checks')

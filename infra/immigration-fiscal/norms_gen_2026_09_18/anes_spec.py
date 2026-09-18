"""ANES 2020 and 2024 time series: variable map and outcome recodes.
Variable IDs were read out of the shipped user-guide codebooks (cb_index.py over
the 2020 and 2024 codebook PDFs), never guessed."""
RAW = "raw"
FILES = {
 2020: f"{RAW}/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_csv_20220210.csv",
 2024: f"{RAW}/anes_timeseries_2024_csv_20260519/anes_timeseries_2024_csv_20260519.csv"}

# design and demographics
DESIGN = {
 2020: dict(wpre="V200010a", wpost="V200010b", psu="V200010c", strat="V200010d",
            hisp="V201558x", race="V201549x", par="V201553", born="V201554",
            gpar="V201555", age="V201507x", educ5="V201511x", ideo="V201200",
            inc="V201617x", mode="V200002", lang="V201001"),
 2024: dict(wpre="V240107a", wpost="V240107b", psu="V240107c", strat="V240107d",
            hisp="V241512x", race="V241501x", par="V241506", born="V241507",
            gpar="V241509", age="V241458x", educ5="V241465x", ideo="V241177",
            inc="V241567x", mode="V240002a", lang="V241001")}

# outcome -> {year: (variable, stage)} plus recode rule and label
# stage "pre" uses the pre-election weight, "post" the post-election weight
ITEMS = {
 "strpres_helpful": dict(
   v={2020: ("V201372x", "pre"), 2024: ("V241330x", "pre")}, rule=("le", 3),
   label="president acting without regard to Congress and the courts would be HELPFUL "
         "(7-point summary, codes 1-3 = helpful)"),
 "strleader_agree": dict(
   v={2020: ("V202413", "post"), 2024: ("V242411", "post")}, rule=("le", 2),
   label="agrees a strong leader is good for the US even if the leader bends the rules"),
 "prefer_democracy": dict(
   v={2024: ("V242409", "post")}, rule=("le", 2),
   label="agrees democracy is preferable to any other kind of government (CSES6, 2024 only)"),
 "courts_authority": dict(
   v={2024: ("V242410", "post")}, rule=("le", 2),
   label="agrees the courts should be able to stop the government acting beyond its "
         "authority (CSES6 Q04B, 2024 only)"),
 "people_decide": dict(
   v={2020: ("V202414", "post")}, rule=("le", 2),
   label="agrees the people, not politicians, should make the most important policy "
         "decisions (CSES5, 2020 only)"),
 "votes_counted_fairly": dict(
   v={2020: ("V202219", "post"), 2024: ("V242207", "post")}, rule=("le", 2),
   label="votes are counted fairly all or most of the time"),
 "violence_justified": dict(
   v={2020: ("V201602", "pre"), 2024: ("V241579", "pre")}, rule=("ge_in", [2, 3, 4, 5]),
   label="political violence is at least 'a little' justified"),
 "satisfied_democracy": dict(
   v={2020: ("V202440", "post"), 2024: ("V242439", "post")}, rule=("le", 2),
   label="very or fairly satisfied with the way democracy works in the US"),
 "trust_govt": dict(
   v={2020: ("V201233", "pre"), 2024: ("V241229", "pre")}, rule=("le", 2),
   label="trusts the federal government to do what is right always or most of the time"),
 "trust_election_officials": dict(
   v={2020: ("V201352", "pre"), 2024: ("V241315", "pre")}, rule=("le", 2),
   label="trusts election officials a great deal or a lot"),
 "auth_obedience": dict(
   v={2020: ("V202268", "post"), 2024: ("V242262", "post")}, rule=("eq", 1),
   label="picks obedience over self-reliance as the more important child quality"),
 "auth_respect": dict(
   v={2020: ("V202266", "post"), 2024: ("V242260", "post")}, rule=("eq", 2),
   label="picks respect for elders over independence"),
 "auth_manners": dict(
   v={2020: ("V202267", "post"), 2024: ("V242261", "post")}, rule=("eq", 2),
   label="picks good manners over curiosity"),
 "auth_behaved": dict(
   v={2020: ("V202269", "post"), 2024: ("V242263", "post")}, rule=("eq", 2),
   label="picks well behaved over being considerate"),
 "minorities_adapt": dict(
   v={2020: ("V202416", "post")}, rule=("le", 2),
   label="agrees minorities should adapt to the customs and traditions of the US "
         "(CSES5, 2020 only)"),
 "born_here_important": dict(
   v={2020: ("V202421", "post"), 2024: ("V242454", "post")}, rule=("le", 2),
   label="says being born in the US is very or fairly important to being American"),
}
AUTH4 = ["auth_obedience", "auth_respect", "auth_manners", "auth_behaved"]

---

## 4. What a private-school switch does to GDP, to wealth, and to the public accounts

This is the operator's question, and the accounting has to be kept separate from the
welfare reading. Four distinct things happen when a native family moves one child from a
public school to a private one.

### 4.1 Measured GDP: it rises, but by less than the tuition

BEA measures general government output at the cost of its inputs, because that output is
not sold. The NIPA handbook is explicit and uses schools as its example: "The value of the
services that are provided by government free of charge, whether to individual members of
society (such as education at public elementary schools) or to society as a whole (such as
national defense or law enforcement), is included in government consumption expenditures."
Government consumption expenditures are "Valued as gross output, based on costs of inputs,
of federal and of state and local general government less sales to other sectors and
own-account investment" [SOURCE: BEA, NIPA Handbook, Chapter 9, "Government Consumption
Expenditures and Gross Investment," pp. 9-3 to 9-7; cached at `_cache/bea_nipa_ch09.pdf`].
Private school tuition paid by households is personal consumption expenditure.

So the switch moves the child's education from the government-consumption line of GDP to
the PCE line. The net change in measured GDP is

    ΔGDP  =  (cost of producing the private school place)  −  (reduction in the district's
             cost of producing the public place)

and **not** the tuition. Two cases:

- **Short run, enrolment-lagged funding, fixed staffing.** The district does not shed a
  teacher when one child leaves. Its input costs are unchanged, so government consumption
  is unchanged and PCE rises by the tuition. Measured GDP rises by roughly the full
  tuition. This is the case the operator described, and it is right for a single family in
  a single year.
- **Long run, enrolment adjusts.** The district eventually sheds marginal cost, and the
  comparison of unit costs then decides the sign. Average private tuition was **$12,790**
  in 2021-22, about $13,700 in 2024 dollars; average public current spending per pupil in
  FY2024 was **$17,846** [SOURCE: NCES Digest 2023 table 205.50; Census F-33 FY2024
  district file `elsec24t.txt`, 13,252 districts and 46.37m pupils, computed in
  `derived/f33_fy2024_per_pupil.csv`]. Private production of a school place costs roughly
  three-quarters of what the public place it replaces costs. **In the long run a switch
  therefore lowers measured GDP**, by something of the order of $4,000 per pupil-year.
  This is the opposite of the short-run direction, and both are accounting artefacts of
  valuing government output at input cost rather than statements about welfare.

A caution on the private side. Most US private K-12 schools are nonprofit, and NIPA
measures nonprofit output at cost too, with tuition recorded as the household's purchase
of that output. Sticker tuition also understates the resource cost where schools are
subsidised by donations or by a religious order's below-market labour, and overstates it
where tuition covers capital or endowment building. Treat the tuition figure as an
approximation to the private production cost, not an identity. [INFERENCE]

### 4.2 The family's position: this is a real resource cost, and it may buy nothing measurable

The tuition is not a transfer to another household. It purchases teaching services that are
really produced, so real resources are consumed. The household's consumption of everything
else, or its saving, falls by that amount.

Whether that consumption is *welfare-improving* depends on what the switch buys. If the
family would have received an equivalent education free, the tuition is a **defensive
expenditure**: it purchases relative position — peer composition, perceived safety, class
size — rather than additional real output. Defensive expenditure adds to GDP and subtracts
from welfare, the same way spending on locks does. This is the single most
[FRAMING-SENSITIVE] judgement in the memo, and it is empirically testable: the test is
whether switchers' measured outcomes improve.

The switcher-outcome evidence is summarised in §5.4. The short version is that the
credible experimental estimates of moving a child from a public school to a private one
with a voucher cluster near zero and include large negative results, which makes the
defensive-expenditure reading the better-supported one for the average switcher. It does
not follow that no family gains; it follows that the average measured academic gain is not
what the tuition is buying.

### 4.3 The public school's revenue: mostly a transfer, with a real diseconomy attached

Three components move in different directions.

| Component | What happens when one native child leaves | Resource cost or transfer |
|---|---|---|
| State formula aid | Falls, roughly by the state's marginal per-pupil aid rate; average state revenue was $9,589 per pupil in FY2024 | **Transfer** — the money is reallocated to other districts or other state uses |
| Local property tax revenue | Unchanged — the family still lives there and still pays; $5,815 per pupil in FY2024 | **Neither** — no flow changes |
| Federal categorical aid | Largely unchanged, since it tracks poverty and EL counts, not the departing child | **Neither** |
| Marginal instructional cost | Falls, but by less than average cost in the short run | **Real**, but a saving, not a cost |
| Fixed cost per remaining pupil | Rises: the same building, administration and transport over fewer pupils | **Real diseconomy** |

The headline consequence is not a district revenue collapse. Losing a pupil while keeping
the property tax base can *raise* revenue per remaining pupil, because the local share is
now divided among fewer children. The genuine resource cost is the duplication: an empty
seat in the public school plus a newly-built seat in the private one, plus the second
transport system. The genuine transfer is the state-aid reallocation, which is a
distributional question between districts, not a cost to the economy.

### 4.4 The median voter: the effect that is neither a cost nor a transfer

The family that leaves also leaves the public school's political constituency. It keeps
paying school taxes but no longer consumes the service, which moves its preferred level of
school spending down. If the departing families are disproportionately those with the
highest willingness to pay for school quality — and Betts & Fairlie's finding that flight
is concentrated among white natives at secondary level implies they are — then flight
shifts the median voter in local school elections.

This is the mechanism that links §4 back to §1.2 and to the fragmentation literature. It
is not an accounting entry. It shows up later, as lower bond passage rates, lower parcel
taxes, and lower local revenue per pupil, and that is exactly what design (b) and the
California bond analysis test directly.

### 4.5 Summary of the accounting

| Item | Direction | Classification |
|---|---|---|
| Private tuition paid | + to PCE | Real resource use; **defensive expenditure** to the extent outcomes do not improve |
| Public school input costs | Unchanged short run, − long run | Real |
| Measured GDP | + in the short run, ambiguous in the long run | Accounting artefact of valuing government output at cost |
| Household net worth / other consumption | − by the tuition | Real, borne by the family |
| State enrolment-linked aid to the district | − | **Transfer** between districts |
| Local property-tax revenue | Unchanged | Neither |
| Fixed cost per remaining pupil | + | Real diseconomy |
| Median voter for school taxes | Shifts against spending | Political-economy effect, measured in §3 |


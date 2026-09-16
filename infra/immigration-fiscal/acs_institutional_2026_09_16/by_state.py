"""Within-state decomposition: US-born Mexican-origin vs native NH-white institutional share, men 18-39, CA / TX / rest.
Inputs: h{yr}.json, r{yr}.json (national) and h{yr}_st06/48.json, r{yr}_st06/48.json (state filters), from the Census API."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
def load(fn):
    d = json.load(open(HERE / fn)); hdr = d[0]
    tc = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    return {tuple(str(x) for x in r[len(tc):]): (r[tc["2"]], sum(r[i] for i in tc.values())) for r in d[1:]}
def sub(a, b):
    return {k: (a[k][0] - b.get(k, (0, 0))[0], a[k][1] - b.get(k, (0, 0))[1]) for k in a}
for yr in ("2010", "2023"):
    us_h, us_r = load(f"h{yr}.json"), load(f"r{yr}.json")
    ca_h, ca_r = load(f"h{yr}_st06.json"), load(f"r{yr}_st06.json")
    tx_h, tx_r = load(f"h{yr}_st48.json"), load(f"r{yr}_st48.json")
    rest_h, rest_r = sub(sub(us_h, ca_h), tx_h), sub(sub(us_r, ca_r), tx_r)
    for label, h, r in (("California", ca_h, ca_r), ("Texas", tx_h, tx_r), ("all other states", rest_h, rest_r), ("US", us_h, us_r)):
        mi, mn = h[("1", "02")]; wi, wn = r[("1", "1")]; fi, fn = h[("2", "02")]
        print(f"{yr} {label:17s} US-born Mexican {100*mi/mn:5.2f}% (N {mn:>10,})  native white {100*wi/wn:5.2f}%  ratio {mi/mn/(wi/wn):4.2f}x   FB Mexican {100*fi/fn:5.2f}%")
    print()

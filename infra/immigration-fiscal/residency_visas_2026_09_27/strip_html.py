import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, t, a):
        if t in ("script","style","noscript","svg"): self.skip+=1
        if t in ("h1","h2","h3","h4","h5","p","li","br","div","tr"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script","style","noscript","svg") and self.skip: self.skip-=1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding="utf-8",errors="replace").read())
txt=re.sub(r"[ \t\xa0]+"," ","".join(p.out)); txt=re.sub(r"\n\s*\n+","\n",txt)
print(txt)

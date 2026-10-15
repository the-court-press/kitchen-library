#!/usr/bin/env python3
"""Add a chapter and rebuild index.html.
Usage: python3 add_chapter.py path/to/book.pdf "Title" "One-line description"
Run with no arguments to just rebuild index.html from chapters.json.
Needs poppler-utils (pdftoppm) for the cover thumbnail."""
import json, os, shutil, subprocess, sys, html
D = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(D, "chapters.json")

def add(pdf, title, desc):
    name = os.path.basename(pdf); stem = name[:-4]
    shutil.copy(pdf, os.path.join(D, "pdfs", name))
    subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-jpeg", "-jpegopt", "quality=80",
                    "-scale-to", "400", "-singlefile", pdf, os.path.join(D, "covers", stem)], check=True)
    ch = [c for c in json.load(open(J)) if c["file"] != name]
    ch.append({"file": name, "title": title, "desc": desc})
    json.dump(ch, open(J, "w"), indent=1, ensure_ascii=False)

def build():
    ch = json.load(open(J)); e = html.escape; cards = []
    for i, c in enumerate(ch, 1):
        stem = c["file"][:-4]; mb = os.path.getsize(os.path.join(D, "pdfs", c["file"])) / 1e6
        cards.append(f'''<article class="card"><a href="pdfs/{e(c["file"])}"><img src="covers/{e(stem)}.jpg" alt="Cover of {e(c["title"])}" loading="lazy"></a>
<div><p class="no">Chapter {i}</p><h2>{e(c["title"])}</h2><p>{e(c["desc"])}</p>
<a class="dl" href="pdfs/{e(c["file"])}" download>Download PDF ({mb:.1f} MB)</a></div></article>''')
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carl Weathers' Kitchen Library</title><style>
body{{margin:0;background:#f7f0e3;color:#3b2a1e;font-family:Georgia,"Times New Roman",serif;line-height:1.5}}
header{{text-align:center;padding:3rem 1rem 1.5rem;border-bottom:2px dashed #c9a77c}}
h1{{margin:0;font-size:2.4rem;color:#7a3e1d}} header p{{margin:.4rem 0 0;font-style:italic;color:#8a6a4f}}
main{{max-width:960px;margin:2rem auto;padding:0 1rem;display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fill,minmax(270px,1fr))}}
.card{{background:#fffaf1;border:1px solid #e3cfae;border-radius:10px;overflow:hidden;box-shadow:0 2px 6px rgba(90,60,30,.12)}}
.card img{{width:100%;display:block;aspect-ratio:3/4;object-fit:cover;border-bottom:1px solid #e3cfae}}
.card div{{padding:1rem 1.2rem 1.3rem}} .no{{margin:0;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:#a0794f}}
h2{{margin:.2rem 0 .4rem;font-size:1.3rem;color:#5c3a1e}} .card p{{margin:.3rem 0 .9rem}}
.dl{{display:inline-block;background:#7a3e1d;color:#fffaf1;text-decoration:none;padding:.45rem .9rem;border-radius:6px;font-size:.9rem}}
.dl:hover{{background:#9b5229}} footer{{text-align:center;color:#a0794f;font-size:.85rem;padding:2rem 1rem}}
</style></head><body><header><h1>Carl Weathers' Kitchen Library</h1><p>a new ingredient chapter most days</p></header>
<main>
{chr(10).join(cards)}
</main><footer>Field guides for a Thai kitchen. Prices are real purchases at the time of writing.</footer></body></html>'''
    open(os.path.join(D, "index.html"), "w").write(page)

if __name__ == "__main__":
    if len(sys.argv) == 4: add(*sys.argv[1:])
    elif len(sys.argv) != 1: sys.exit(__doc__)
    build(); print("index.html rebuilt")

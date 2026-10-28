# Carl Weathers' Kitchen Library

Static site (GitHub Pages, served from the repo root; `.nojekyll` included).

## Add a new chapter
    python3 add_chapter.py /path/to/the_new_book.pdf "The Title" "One-line description"
This copies the PDF into `pdfs/`, renders page 1 to `covers/<name>.jpg`, appends it to `chapters.json`, and rebuilds `index.html`. Commit and push all changed files.

## Add a Mastery Guide (technique or dish guides, separate shelf)
    python3 add_chapter.py --guide /path/to/the_guide.pdf "The Title" "One-line description"
Same as a chapter, but it is listed in `guides.json` and shown under "Mastery Guides" below the ingredient chapters.

Run `python3 add_chapter.py` with no arguments to just rebuild the page. Edit `chapters.json` or `guides.json` to fix titles, descriptions or ordering.

Before publishing, run a privacy check: `pdftotext new.pdf - | grep -nE '@|/workspace|/home|order|invoice'`.
The page keeps `noindex, nofollow` and `robots.txt` as before.

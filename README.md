# Carl Weathers' Kitchen Library

Static site (GitHub Pages, served from the repo root; `.nojekyll` included).

## Add a new chapter
    python3 add_chapter.py /path/to/the_new_book.pdf "The Title" "One-line description"
This copies the PDF into `pdfs/`, renders page 1 to `covers/<name>.jpg`, appends it to `chapters.json`, and rebuilds `index.html`. Commit and push all changed files.
Run `python3 add_chapter.py` with no arguments to just rebuild the page. Edit `chapters.json` to fix titles, descriptions or ordering.

Before publishing, run a privacy check: `pdftotext new.pdf - | grep -nE '@|/workspace|/home|order|invoice'`.

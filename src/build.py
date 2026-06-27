"""Build the Langfuse visual guide as a standalone bilingual static site.

Layout produced (relative to project root):

    index.html            entry point (table of contents)
    lessons/NN-*.html     lesson pages (each embeds zh + en; CSS toggles)

Pages use relative links so the site works via file:// or any static server.

Usage:
    cd src && python build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LESSONS_DIR = os.path.join(ROOT, "lessons")
sys.path.insert(0, HERE)

import shell  # noqa: E402
import quizzes  # noqa: E402
from registry import CONTENT  # noqa: E402


def build():
    os.makedirs(LESSONS_DIR, exist_ok=True)
    order = [p[0] for p in shell.PAGES]
    written = []
    for page in shell.PAGES:
        fname = page[0]
        if fname not in CONTENT:
            sys.exit(f"build error: no registry.CONTENT entry for {fname!r} (declared in shell.PAGES)")
        base = CONTENT[fname]
        self_num = order.index(fname) + 1
        content = {
            "zh": shell.autolink(base["zh"] + quizzes.render(fname, "zh"), self_num, order),
            "en": shell.autolink(base["en"] + quizzes.render(fname, "en"), self_num, order),
        }
        html = shell.page(fname, content, home_href="../index.html")
        with open(os.path.join(LESSONS_DIR, fname), "w", encoding="utf-8") as f:
            f.write(html)
        written.append(os.path.join("lessons", fname))
    with open(os.path.join(ROOT, shell.INDEX_FILE), "w", encoding="utf-8") as f:
        f.write(shell.index_page(lesson_prefix="lessons/"))
    written.append(shell.INDEX_FILE)
    return written


if __name__ == "__main__":
    done = build()
    print("Wrote", len(done), "files under", ROOT)
    for f in done:
        print("  -", f)

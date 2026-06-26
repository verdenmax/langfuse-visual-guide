"""Single source of truth: ordered map of output filename -> bilingual content.

Each value is a dict ``{"zh": html, "en": html}``. build.py and build_print.py
both import this so the lesson set stays in sync with shell.PAGES.

Grows one Part module per milestone (part1 .. part11). M0 ships only L01.
"""
import part1

# Filename -> {"zh": ..., "en": ...}. Keep keys in sync with shell.PAGES.
CONTENT = {
    "01-what-is-langfuse.html": part1.LESSON_01,
    "02-observability-2-and-wide-events.html": part1.LESSON_02,
    "03-three-pillars-deep.html": part1.LESSON_03,
}

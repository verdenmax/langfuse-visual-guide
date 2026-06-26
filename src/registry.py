"""Single source of truth: ordered map of output filename -> bilingual content.

Each value is a dict ``{"zh": html, "en": html}``. build.py and build_print.py
both import this so the lesson set stays in sync with shell.PAGES.

Grows one Part module per milestone (part1 .. part11). M0 ships only L01.
"""
import part1
import part2
import part3

# Filename -> {"zh": ..., "en": ...}. Keep keys in sync with shell.PAGES.
CONTENT = {
    "01-what-is-langfuse.html": part1.LESSON_01,
    "02-observability-2-and-wide-events.html": part1.LESSON_02,
    "03-three-pillars-deep.html": part1.LESSON_03,
    "04-project-map-monorepo.html": part1.LESSON_04,
    "05-life-of-a-trace.html": part1.LESSON_05,
    "06-instrumenting-an-llm-app.html": part2.LESSON_06,
    "07-dual-store-architecture.html": part2.LESSON_07,
    "08-clickhouse-wide-events.html": part2.LESSON_08,
    "09-postgres-metadata-schema.html": part2.LESSON_09,
    "10-multi-tenancy.html": part2.LESSON_10,
    "11-deployment-topology.html": part2.LESSON_11,
    "12-ingestion-api.html": part3.LESSON_12,
    "13-event-types-merge.html": part3.LESSON_13,
    "14-ingestion-queue.html": part3.LESSON_14,
    "15-ingestion-service.html": part3.LESSON_15,
}

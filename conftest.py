"""Repo-root pytest config, shared across all phase test suites.

Voyage's free tier caps embeddings at 3 requests/minute. Several tests
across phase3-rag, phase4-agent, and phase5-production call
embed_chunks() (directly, or transitively via retrieval()), and CI runs
them all in one process — without spacing, the 3rd+ call in the same
run gets a 429 RateLimitError, not because anything is broken.

voyage_pacing is a fixture (not a decorator or import) so any test file
under this rootdir can request it as a parameter with zero imports,
regardless of which phase directory it lives in.
"""

import time

import pytest

_last_voyage_call_at: float | None = None

# Seconds to wait between Voyage-calling tests. 3 RPM means at most 3
# calls in any rolling 60s window; spacing every call by 25s keeps any
# 60s window to at most 2-3 calls. Empirically-tuned, not guaranteed -
# Voyage's real limiter may be stricter than a clean rolling window, so
# this may need to grow if a future CI run still gets rate-limited.
MIN_SECONDS_BETWEEN_VOYAGE_CALLS = 25


@pytest.fixture
def voyage_pacing():
    global _last_voyage_call_at
    now = time.monotonic()
    if _last_voyage_call_at is not None:
        elapsed = now - _last_voyage_call_at
        remaining = MIN_SECONDS_BETWEEN_VOYAGE_CALLS - elapsed
        if remaining > 0:
            time.sleep(remaining)
    _last_voyage_call_at = time.monotonic()

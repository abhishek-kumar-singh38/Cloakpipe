"""Deterministic, inert canary representations for parser testing.

The module intentionally accepts no arbitrary payload input. This keeps the
generated corpus tied to a harmless marker and prevents it becoming a generic
payload-obfuscation utility.
"""

from __future__ import annotations

import base64
import json
import urllib.parse

CANARY = "CLOAKPIPE_DEFENSIVE_CANARY_V1"


def _hex(value: str) -> str:
    return value.encode("utf-8").hex()


def generate_network_corpus(label: str = "authorized-normalization-study") -> dict[str, object]:
    """Return a JSON-serializable corpus of fixed-canary test cases."""
    encoded_url = urllib.parse.quote(CANARY, safe="")
    double_url = urllib.parse.quote(encoded_url, safe="")
    cases = [
        {"id": "plain", "family": "plain", "value": CANARY, "expected": CANARY},
        {"id": "url-once", "family": "url-encoding", "value": encoded_url, "expected": CANARY},
        {"id": "url-twice", "family": "double-url-encoding", "value": double_url, "expected": CANARY},
        {
            "id": "base64",
            "family": "base64",
            "value": base64.b64encode(CANARY.encode()).decode("ascii"),
            "expected": CANARY,
        },
        {"id": "hex", "family": "hex", "value": _hex(CANARY), "expected": CANARY},
        {
            "id": "json-string",
            "family": "json-string",
            "value": json.dumps(CANARY),
            "expected": CANARY,
        },
        {
            "id": "form-value",
            "family": "form-url-encoding",
            "value": urllib.parse.urlencode({"canary": CANARY}),
            "expected": CANARY,
        },
    ]
    return {
        "tool": "CloakPipe",
        "schema_version": 1,
        "purpose": "authorized defensive normalization research",
        "label": label,
        "canary": CANARY,
        "cases": cases,
    }
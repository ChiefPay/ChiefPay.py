#!/usr/bin/env python3
"""
Postprocess chiefpay/types/models.py after regenerating it with datamodel-codegen.

Regeneration workflow:

    datamodel-codegen --input <public OpenAPI spec> --input-file-type openapi \
        --output chiefpay/types/models.py --output-model-type pydantic_v2.BaseModel
    python scripts/postprocess_models.py

datamodel-codegen emits ``extra="forbid"`` for every model. That is wrong for
response models: any additive server field (e.g. statusUpdatedAt, isExchange)
would break parsing of REST responses and socket notifications in already
deployed SDK versions. This script enforces the split that was previously a
hand edit (and would otherwise be silently reverted by the next regeneration):

- response/notification models -> ``extra="ignore"`` (forward compatible);
- request models (built by the caller) -> ``extra="forbid"`` so typos in
  caller-supplied fields keep failing client-side.

Request models are recognized by the ``*Request`` name suffix plus the
explicit REQUEST_MODELS set below. The script is idempotent.
"""

import re
import sys
from pathlib import Path

MODELS_PATH = Path(__file__).resolve().parent.parent / "chiefpay" / "types" / "models.py"

# Models built by the caller and sent to the API. Everything else is parsed
# from server data and must tolerate additive fields. Names ending in
# "Request" are treated as request models automatically.
REQUEST_MODELS = {"ChainToken"}

HEADER_NOTE = """\
#
# Postprocessed by scripts/postprocess_models.py (run it after every
# regeneration): response models use extra="ignore" so additive server fields
# (e.g. statusUpdatedAt, isExchange) never break parsing. Request models keep
# extra="forbid" to catch caller typos client-side.
"""


def is_request_model(name: str) -> bool:
    return name.endswith("Request") or name in REQUEST_MODELS


def main() -> int:
    source = MODELS_PATH.read_text()
    lines = source.splitlines(keepends=True)

    current_class = None
    changed = 0
    for i, line in enumerate(lines):
        class_match = re.match(r"class (\w+)\(", line)
        if class_match:
            current_class = class_match.group(1)
            continue
        if current_class and "model_config" in line and "extra=" in line:
            want = "forbid" if is_request_model(current_class) else "ignore"
            new_line = re.sub(r'extra="(?:forbid|ignore|allow)"', f'extra="{want}"', line)
            if new_line != line:
                lines[i] = new_line
                changed += 1

    result = "".join(lines)

    if "Postprocessed by scripts/postprocess_models.py" not in result:
        # Insert the note right after the leading comment block codegen emits.
        end_of_comments = 0
        for i, line in enumerate(lines):
            if line.startswith("#"):
                end_of_comments = i + 1
            else:
                break
        lines.insert(end_of_comments, HEADER_NOTE)
        result = "".join(lines)
        changed += 1

    if result != source:
        MODELS_PATH.write_text(result)
    print(f"{MODELS_PATH.relative_to(MODELS_PATH.parents[2])}: {changed} change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate data/nebius_kpis.csv: schema, value format, and sourcing rules.

Run: python scripts/validate_kpis.py [path]
Exits non-zero and lists every problem if any row breaks a rule.
"""

import csv
import re
import sys
from pathlib import Path

HEADER = ["period", "metric", "value", "unit", "source_quality", "source", "notes"]
QUALITIES = {"filing", "filing_derived", "primary_linked", "secondary", "author_notes"}
PERIOD_RE = re.compile(r"^\d{4}-(Q[1-4]|FY-guide|\d{2}(-\d{2})?)$")
METRIC_RE = re.compile(r"^[a-z0-9_]+$")
NUMBER = r"-?\d+(\.\d+)?"
VALUE_RE = re.compile(rf"^{NUMBER}(-{NUMBER})?$")  # a number, or a range like 3.0-3.4
URL_RE = re.compile(r"^https?://\S+$")
FILING_RE = re.compile(r"\b(6-K|20-F)\b")


def validate(path):
    errors = []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return [f"{path}: file is empty"]
    if rows[0] != HEADER:
        errors.append(f"header must be {','.join(HEADER)}; got {','.join(rows[0])}")

    seen = {}
    for lineno, row in enumerate(rows[1:], start=2):
        where = f"line {lineno}"
        if len(row) != len(HEADER):
            errors.append(f"{where}: expected {len(HEADER)} columns, got {len(row)}")
            continue
        rec = dict(zip(HEADER, (cell.strip() for cell in row)))
        for field in HEADER[:-1]:  # notes may be empty
            if not rec[field]:
                errors.append(f"{where}: '{field}' is empty")
        if rec["period"] and not PERIOD_RE.match(rec["period"]):
            errors.append(f"{where}: bad period '{rec['period']}' (e.g. 2026-Q2, 2026-FY-guide, 2026-10-01)")
        if rec["metric"] and not METRIC_RE.match(rec["metric"]):
            errors.append(f"{where}: metric '{rec['metric']}' must be snake_case")
        if rec["value"] and not VALUE_RE.match(rec["value"]):
            errors.append(f"{where}: value '{rec['value']}' must be a number or a range like 3.0-3.4")

        quality, source = rec["source_quality"], rec["source"]
        if quality and quality not in QUALITIES:
            errors.append(f"{where}: source_quality '{quality}' not in {sorted(QUALITIES)}")
        elif quality in {"filing", "filing_derived"} and not FILING_RE.search(source):
            errors.append(f"{where}: {quality} source must name the filing (6-K or 20-F) and page; got '{source}'")
        elif quality in {"primary_linked", "secondary"} and not URL_RE.match(source):
            errors.append(f"{where}: {quality} source must be a URL; got '{source}'")

        key = (rec["period"], rec["metric"])
        if key in seen:
            errors.append(f"{where}: duplicate {key[0]} / {key[1]} (first on line {seen[key]})")
        else:
            seen[key] = lineno
    return errors


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/nebius_kpis.csv")
    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"{path}: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

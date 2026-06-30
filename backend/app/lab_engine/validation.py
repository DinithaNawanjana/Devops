"""Parse validate.sh output into structured per-step results.

validate.sh emits one line per check:
    STEP:<name>:PASS
    STEP:<name>:FAIL
    STEP:<name>:FAIL:<human message>
and exits 0 only when every step passed. The score awarded is proportional
to the fraction of steps that passed, scaled by the lab's points.
"""
from __future__ import annotations

from ..schemas import CheckResult, CheckStep


def parse(exit_code: int, output: str, points: int) -> CheckResult:
    steps: list[CheckStep] = []
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("STEP:"):
            continue
        parts = line.split(":", 3)
        # STEP : name : PASS/FAIL : optional message
        if len(parts) < 3:
            continue
        name = parts[1].strip()
        verdict = parts[2].strip().upper()
        message = parts[3].strip() if len(parts) > 3 else ""
        steps.append(
            CheckStep(name=name, passed=(verdict == "PASS"), message=message)
        )

    if steps:
        passed_count = sum(1 for s in steps if s.passed)
        all_passed = passed_count == len(steps)
        score = round(points * passed_count / len(steps))
        # A non-zero exit overrides an all-pass step parse (defensive).
        passed = all_passed and exit_code == 0
    else:
        # No structured steps — fall back to the raw exit code.
        passed = exit_code == 0
        score = points if passed else 0
        steps.append(
            CheckStep(
                name="validation",
                passed=passed,
                message="exit 0" if passed else f"exit {exit_code}",
            )
        )

    return CheckResult(passed=passed, score=score, steps=steps, raw_output=output)

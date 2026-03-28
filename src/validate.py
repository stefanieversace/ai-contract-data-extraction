import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


REQUIRED_FIELDS = [
    "agreement_type",
    "parties",
    "effective_date",
    "term_length",
    "payment_terms",
    "auto_renewal",
    "termination_clause",
    "governing_law",
    "confidentiality",
    "indemnity",
    "exclusivity",
    "key_risks",
    "reviewer_notes",
    "confidence_score",
    "field_confidence"
]


def validate_contract_data(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validates and normalises extracted contract data.
    Returns:
        validated_data, issues
    """
    issues: List[str] = []
    validated = dict(data)

    for field in REQUIRED_FIELDS:
        if field not in validated:
            validated[field] = _default_value_for_field(field)
            issues.append(f"Missing required field added: {field}")

    if not isinstance(validated["parties"], list):
        validated["parties"] = []
        issues.append("Field 'parties' was not a list and was reset.")

    if not isinstance(validated["key_risks"], list):
        validated["key_risks"] = []
        issues.append("Field 'key_risks' was not a list and was reset.")

    if not isinstance(validated["field_confidence"], dict):
        validated["field_confidence"] = {}
        issues.append("Field 'field_confidence' was not an object and was reset.")

    validated["effective_date"], date_issue = _normalise_date(validated["effective_date"])
    if date_issue:
        issues.append(date_issue)

    validated["payment_terms"], payment_issue = _normalise_payment_terms(validated["payment_terms"])
    if payment_issue:
        issues.append(payment_issue)

    validated["auto_renewal"], auto_issue = _normalise_bool(validated["auto_renewal"], "auto_renewal")
    if auto_issue:
        issues.append(auto_issue)

    validated["exclusivity"], excl_issue = _normalise_bool(validated["exclusivity"], "exclusivity")
    if excl_issue:
        issues.append(excl_issue)

    validated["confidence_score"], score_issue = _normalise_confidence(validated["confidence_score"])
    if score_issue:
        issues.append(score_issue)

    validated["parties"] = [str(p).strip() for p in validated["parties"] if str(p).strip()]

    return validated, issues


def _default_value_for_field(field: str) -> Any:
    defaults = {
        "agreement_type": None,
        "parties": [],
        "effective_date": None,
        "term_length": None,
        "payment_terms": None,
        "auto_renewal": None,
        "termination_clause": None,
        "governing_law": None,
        "confidentiality": None,
        "indemnity": None,
        "exclusivity": None,
        "key_risks": [],
        "reviewer_notes": None,
        "confidence_score": None,
        "field_confidence": {}
    }
    return defaults.get(field)


def _normalise_date(value: Any) -> Tuple[Any, str]:
    if value is None:
        return None, ""

    if not isinstance(value, str):
        return None, "Effective date was not a string and was reset."

    value = value.strip()

    # Accepts formats like January 15, 2024
    if re.fullmatch(r"[A-Z][a-z]+ \d{1,2}, \d{4}", value):
        return value, ""

    return value, "Effective date format was not standardised."


def _normalise_payment_terms(value: Any) -> Tuple[Any, str]:
    if value is None:
        return None, ""

    if not isinstance(value, str):
        return None, "Payment terms were not a string and were reset."

    match = re.search(r"(\d{1,3})", value)
    if match:
        return f"Net {match.group(1)}", ""

    return value.strip(), "Could not standardise payment terms."


def _normalise_bool(value: Any, field_name: str) -> Tuple[Any, str]:
    if value is None or isinstance(value, bool):
        return value, ""

    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "y", "1"}:
            return True, ""
        if lowered in {"false", "no", "n", "0"}:
            return False, ""

    return None, f"Field '{field_name}' could not be normalised to boolean."

def _normalise_confidence(value: Any) -> Tuple[Any, str]:
    if value is None:
        return None, ""

    try:
        numeric = round(float(value), 2)
        if numeric < 0:
            return 0.0, "Confidence score was below 0 and was clamped."
        if numeric > 1:
            return 1.0, "Confidence score was above 1 and was clamped."
        return numeric, ""
    except (TypeError, ValueError):
        return None, "Confidence score was invalid and was reset."


def load_json(file_path: str) -> Dict[str, Any]:
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


def save_json(data: Dict[str, Any], file_path: str) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate extracted contract JSON.")
    parser.add_argument("input_file", help="Path to extracted JSON")
    parser.add_argument(
        "--output",
        default="outputs/scored_results/validated_contract.json",
        help="Path to save validated JSON"
    )
    args = parser.parse_args()

    raw = load_json(args.input_file)
    validated, issues = validate_contract_data(raw)
    save_json(validated, args.output)

    print(json.dumps(validated, indent=2))
    print("\nValidation issues:")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("- None")

    print(f"\nSaved to: {args.output}")

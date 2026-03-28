import json
import re
from pathlib import Path
from typing import Any, Dict, List


def generate_risk_flags(contract: Dict[str, Any]) -> List[str]:
    risks: List[str] = []

    payment_terms = contract.get("payment_terms")
    auto_renewal = contract.get("auto_renewal")
    termination_clause = contract.get("termination_clause")
    governing_law = contract.get("governing_law")
    exclusivity = contract.get("exclusivity")
    indemnity = contract.get("indemnity")

    payment_days = _extract_net_days(payment_terms)
    if payment_days is not None and payment_days > 60:
        risks.append("Extended payment terms (>60 days)")

    if auto_renewal is True:
        risks.append("Auto-renewal clause present")

    if termination_clause:
        lowered = termination_clause.lower()
        if "for cause only" in lowered:
            risks.append("No termination for convenience")
    else:
        risks.append("Termination clause missing or unclear")

    if not governing_law:
        risks.append("Missing governing law")

    if exclusivity is True:
        risks.append("Exclusivity clause present")

    if indemnity and _is_broad_indemnity(indemnity):
        risks.append("Broad or one-sided indemnity language")

    return risks


def _extract_net_days(payment_terms: Any) -> int | None:
    if not payment_terms or not isinstance(payment_terms, str):
        return None

    match = re.search(r"(\d{1,3})", payment_terms)
    if not match:
        return None

    return int(match.group(1))


def _is_broad_indemnity(indemnity_text: str) -> bool:
    lowered = indemnity_text.lower()

    broad_patterns = [
        "any and all claims",
        "all losses",
        "all liabilities",
        "defend, indemnify, and hold harmless",
        "without limitation"
    ]

    return any(pattern in lowered for pattern in broad_patterns)


def append_risks_to_contract(contract: Dict[str, Any]) -> Dict[str, Any]:
    contract = dict(contract)
    contract["key_risks"] = generate_risk_flags(contract)
    return contract


def load_json(file_path: str) -> Dict[str, Any]:
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


def save_json(data: Dict[str, Any], file_path: str) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate risk flags for contract JSON.")
    parser.add_argument("input_file", help="Path to validated contract JSON")
    parser.add_argument(
        "--output",
        default="outputs/scored_results/risk_flagged_contract.json",
        help="Path to save final JSON"
    )
    args = parser.parse_args()

    contract = load_json(args.input_file)
    enriched = append_risks_to_contract(contract)
    save_json(enriched, args.output)

    print(json.dumps(enriched, indent=2))
    print(f"\nSaved to: {args.output}")

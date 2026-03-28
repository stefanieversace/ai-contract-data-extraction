import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class ContractExtractor:
    """
    Lightweight contract field extractor.

    This version uses deterministic pattern matching so the project works
    without requiring a paid API key. Later, you can swap the extraction
    logic for an LLM call while keeping the same output structure.
    """

    def __init__(self) -> None:
        self.patterns = {
            "agreement_type": [
                r"(vendor services agreement)",
                r"(licen[cs]ing agreement)",
                r"(service agreement)",
                r"(master services agreement)",
                r"(production services agreement)",
                r"(talent agreement)",
                r"(advertising insertion order)",
                r"(non-disclosure agreement)",
                r"(nda)"
            ],
            "effective_date": [
                r"effective date[:\s]+([A-Z][a-z]+ \d{1,2}, \d{4})",
                r"dated as of[:\s]+([A-Z][a-z]+ \d{1,2}, \d{4})",
                r"effective as of[:\s]+([A-Z][a-z]+ \d{1,2}, \d{4})"
            ],
            "payment_terms": [
                r"(net\s+\d{1,3})",
                r"payment terms[:\s]+([A-Za-z0-9\s\-]+)",
                r"invoice[s]? payable within (\d{1,3}\s+days)"
            ],
            "governing_law": [
                r"governed by the laws of ([A-Za-z\s]+)",
                r"governing law[:\s]+([A-Za-z\s]+)"
            ],
            "term_length": [
                r"term of (\d{1,2}\s+(?:month|months|year|years))",
                r"initial term[:\s]+(\d{1,2}\s+(?:month|months|year|years))",
                r"for a period of (\d{1,2}\s+(?:month|months|year|years))"
            ],
            "termination_clause": [
                r"(termination for convenience[^.]+[.])",
                r"(termination for cause only[^.]*[.])",
                r"(either party may terminate[^.]+[.])",
                r"(this agreement may be terminated[^.]+[.])"
            ],
            "confidentiality": [
                r"(confidentiality[^.]+[.])",
                r"(confidential information[^.]+[.])"
            ],
            "indemnity": [
                r"(indemnif(?:y|ication)[^.]+[.])"
            ]
        }

    def extract(self, text: str) -> Dict[str, Any]:
        text_clean = self._normalise_whitespace(text)

        result: Dict[str, Any] = {
            "agreement_type": self._extract_first_match(text_clean, "agreement_type"),
            "parties": self._extract_parties(text_clean),
            "effective_date": self._extract_first_match(text_clean, "effective_date"),
            "term_length": self._extract_first_match(text_clean, "term_length"),
            "payment_terms": self._extract_payment_terms(text_clean),
            "auto_renewal": self._detect_auto_renewal(text_clean),
            "termination_clause": self._extract_first_match(text_clean, "termination_clause"),
            "governing_law": self._extract_first_match(text_clean, "governing_law"),
            "confidentiality": self._extract_first_match(text_clean, "confidentiality"),
            "indemnity": self._extract_first_match(text_clean, "indemnity"),
            "exclusivity": self._detect_exclusivity(text_clean),
            "key_risks": [],
            "reviewer_notes": None,
            "confidence_score": None,
            "field_confidence": {}
        }

        result["field_confidence"] = self._score_fields(result)
        result["confidence_score"] = self._overall_confidence(result["field_confidence"])

        return result

    def _extract_first_match(self, text: str, field_name: str) -> Optional[str]:
        for pattern in self.patterns.get(field_name, []):
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                return self._clean_value(value)
        return None

    def _extract_payment_terms(self, text: str) -> Optional[str]:
        value = self._extract_first_match(text, "payment_terms")
        if not value:
            return None

        value_lower = value.lower().strip()

    if re.fullmatch(r"\d{1,3}\s+days", value_lower):
    match = re.search(r"(\d{1,3})", value_lower)
    if match:
        return "Net " + match.group(1)
return value.title()

    def _extract_parties(self, text: str) -> List[str]:
        """
        Tries to find patterns like:
        - between Company A and Company B
        - by and between Company A and Company B
        """
        patterns = [
            r"between\s+(.+?)\s+and\s+(.+?)(?:\n|\.|,)",
            r"by and between\s+(.+?)\s+and\s+(.+?)(?:\n|\.|,)"
        ]

        parties: List[str] = []

        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                p1 = self._clean_party_name(match.group(1))
                p2 = self._clean_party_name(match.group(2))
                for party in [p1, p2]:
                    if party and party not in parties:
                        parties.append(party)
                break

        return parties

    def _detect_auto_renewal(self, text: str) -> Optional[bool]:
        positive_patterns = [
            r"automatically renew",
            r"auto[-\s]?renew",
            r"renew for successive",
            r"renewal term"
        ]
        negative_patterns = [
            r"shall not automatically renew",
            r"no automatic renewal"
        ]

        for pattern in negative_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return False

        for pattern in positive_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return True

        return None

    def _detect_exclusivity(self, text: str) -> Optional[bool]:
        if re.search(r"\bexclusive\b|\bexclusivity\b", text, flags=re.IGNORECASE):
            return True
        if re.search(r"\bnon-exclusive\b|\bnonexclusive\b", text, flags=re.IGNORECASE):
            return False
        return None

    def _score_fields(self, result: Dict[str, Any]) -> Dict[str, float]:
        field_confidence: Dict[str, float] = {}

        for field, value in result.items():
            if field in {"key_risks", "reviewer_notes", "confidence_score", "field_confidence"}:
                continue

            if value is None:
                field_confidence[field] = 0.20
            elif isinstance(value, list):
                field_confidence[field] = 0.90 if value else 0.25
            elif isinstance(value, bool):
                field_confidence[field] = 0.90
            elif isinstance(value, str):
                field_confidence[field] = 0.88 if len(value.strip()) > 3 else 0.45
            else:
                field_confidence[field] = 0.50

        return field_confidence

    def _overall_confidence(self, field_confidence: Dict[str, float]) -> float:
        if not field_confidence:
            return 0.0
        avg = sum(field_confidence.values()) / len(field_confidence)
        return round(avg, 2)

    @staticmethod
    def _clean_value(value: str) -> str:
        value = re.sub(r"\s+", " ", value)
        value = value.strip(" .,:;")
        return value

    @staticmethod
    def _clean_party_name(value: str) -> str:
        value = re.sub(r"\s+", " ", value)
        value = value.strip(" .,:;()")
        return value

    @staticmethod
    def _normalise_whitespace(text: str) -> str:
        return re.sub(r"[ \t]+", " ", text).strip()


def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def save_json(data: Dict[str, Any], file_path: str) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract contract fields from a text file.")
    parser.add_argument("input_file", help="Path to the contract text file")
    parser.add_argument(
        "--output",
        default="outputs/extracted_json/contract_output.json",
        help="Path to save extracted JSON"
    )
    args = parser.parse_args()

    raw_text = load_text_file(args.input_file)
    extractor = ContractExtractor()
    extracted = extractor.extract(raw_text)
    save_json(extracted, args.output)

    print(json.dumps(extracted, indent=2))
    print(f"\nSaved to: {args.output}")

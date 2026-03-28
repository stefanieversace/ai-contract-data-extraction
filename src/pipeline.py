import argparse
import json
from pathlib import Path
from typing import Any, Dict

from extract import ContractExtractor, load_text_file
from validate import validate_contract_data
from risk_flags import append_risks_to_contract


def save_json(data: Dict[str, Any], file_path: str) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_pipeline(input_file: str, output_dir: str = "outputs/pipeline_run") -> Dict[str, Any]:
    """
    End-to-end contract intelligence pipeline:
    1. Extract fields from raw contract text
    2. Validate and normalise extracted data
    3. Apply risk flagging logic
    4. Save intermediate and final outputs
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    raw_text = load_text_file(input_file)

    extractor = ContractExtractor()
    extracted = extractor.extract(raw_text)
    save_json(extracted, output_path / "01_extracted.json")

    validated, validation_issues = validate_contract_data(extracted)
    validated["validation_issues"] = validation_issues
    save_json(validated, output_path / "02_validated.json")

    final_output = append_risks_to_contract(validated)
    save_json(final_output, output_path / "03_final_output.json")

    return final_output


def print_summary(result: Dict[str, Any]) -> None:
    print("\n" + "=" * 60)
    print("AI CONTRACT INTELLIGENCE PIPELINE RESULT")
    print("=" * 60)

    print(f"Agreement Type   : {result.get('agreement_type')}")
    print(f"Parties          : {', '.join(result.get('parties', [])) or 'N/A'}")
    print(f"Effective Date   : {result.get('effective_date')}")
    print(f"Term Length      : {result.get('term_length')}")
    print(f"Payment Terms    : {result.get('payment_terms')}")
    print(f"Auto Renewal     : {result.get('auto_renewal')}")
    print(f"Governing Law    : {result.get('governing_law')}")
    print(f"Exclusivity      : {result.get('exclusivity')}")
    print(f"Confidence Score : {result.get('confidence_score')}")

    print("\nKey Risks:")
    risks = result.get("key_risks", [])
    if risks:
        for risk in risks:
            print(f" - {risk}")
    else:
        print(" - None identified")

    print("\nValidation Issues:")
    issues = result.get("validation_issues", [])
    if issues:
        for issue in issues:
            print(f" - {issue}")
    else:
        print(" - None")

    print("\nPipeline completed successfully.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full AI contract intelligence pipeline.")
    parser.add_argument("input_file", help="Path to the input contract text file")
    parser.add_argument(
        "--output-dir",
        default="outputs/pipeline_run",
        help="Directory for pipeline outputs"
    )
    args = parser.parse_args()

    result = run_pipeline(args.input_file, args.output_dir)
    print_summary(result)

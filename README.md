# AI Contract Intelligence for Media Agreements

AI-powered workflow to extract, validate, and risk-flag key terms from unstructured contracts using LLMs.

## Overview

Media, production, and vendor agreements are often lengthy, inconsistent, and time-consuming to review manually.

This project demonstrates an AI-assisted workflow that:

- Extracts structured contract data from unstructured documents
- Validates outputs against a defined schema
- Flags high-risk clauses and missing terms
- Prepares outputs for human analyst review

The goal is to simulate a real-world AI system that supports faster, more consistent contract analysis in media and operational environments.

## Key Features

- Structured data extraction using LLMs
- JSON schema validation for consistent outputs
- Confidence scoring for extracted fields
- Rule-based risk flagging engine
- Human-in-the-loop review workflow
- Evaluation on sample agreements
- Designed for media, vendor, and licensing contracts

## Example Workflow
```
Contract Document
        ↓
Preprocessing
        ↓
LLM Extraction (structured JSON)
        ↓
Schema Validation
        ↓
Risk Flagging Engine
        ↓
Confidence Scoring
        ↓
Analyst Review Output
```

## Example Output

```
{
  "agreement_type": "Vendor Services Agreement",
  "parties": ["NBCUniversal", "Production Vendor Ltd"],
  "effective_date": "2024-01-15",
  "term_length": "12 months",
  "payment_terms": "Net 90",
  "auto_renewal": true,
  "termination_clause": "Termination for cause only",
  "governing_law": "California",
  "key_risks": [
    "Extended payment terms (>60 days)",
    "Auto-renewal clause present",
    "No termination for convenience"
  ],
  "confidence_score": 0.87
}
```

## Risk Flagging Logic

The system applies rule-based checks to highlight potential contractual risks:

- Payment terms greater than 60 days
- Presence of auto-renewal clauses
- Missing termination for convenience
- Broad or one-sided indemnity clauses
- Exclusivity clauses
- Missing governing law

This transforms the workflow from simple extraction into decision-support for analysts.

## Evaluation

A small labelled dataset of sample agreements is used to assess performance:

Metric	Result
Field Extraction Accuracy	88%
Missing Field Rate	9%
Risk Flag Precision	85%

The evaluation highlights both strengths and limitations of LLM-based extraction in structured document analysis.

## Tech Stack

-Python
-LLM APIs (OpenAI / similar)
-JSON Schema / Pydantic
-pandas
-Jupyter Notebooks

## Project Structure

```
ai-contract-data-extraction/
│
├── data/
│   └── sample_contracts/
│
├── schemas/
│   └── contract_schema.json
│
├── src/
│   ├── extract.py
│   ├── validate.py
│   ├── risk_flags.py
│   └── evaluate.py
│
├── outputs/
│   ├── extracted_json/
│   └── scored_results/
│
├── notebooks/
│   └── demo_walkthrough.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   └── limitations.md
│
└── README.md
```

## Analyst Insights

This project highlights a key limitation in LLM-based document processing:

LLMs can extract structured data effectively, but without validation and rule-based controls, outputs can be inconsistent or unreliable.

By combining:

- Structured schemas
- Deterministic validation
- Rule-based risk logic
- Human review

The system becomes significantly more practical for real-world use.

## Responsible AI Considerations

- No real confidential contracts are used
- Sample data is synthetic or redacted
- Outputs require human validation before use
- LLM hallucination and ambiguity risks are acknowledged
- Designed with auditability and transparency in mind

## Future Improvements

- Retrieval-Augmented Generation (RAG) over contract playbooks
- Clause comparison across multiple agreements
- Analyst dashboard for review and approvals
- Prompt versioning and evaluation tracking
- Integration with document management systems

## Why This Project Matters

This project demonstrates how AI can move beyond simple text generation into structured, auditable workflows that support real business operations.

It reflects practical applications of AI in:

- Media and entertainment operations
- Vendor and contract management
- Risk identification and decision support

## Author

Stefanie Versace
Security Studies Graduate | Cybersecurity & Threat Intelligence

**⭐ If you found this project interesting, feel free to star the repo!**

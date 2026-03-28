<h1 align="center">🚀 AI Contract Intelligence for Media Agreements</h1>


<p align="center">
  <b>AI-powered pipeline for extracting, validating, and risk-flagging contract data</b><br>
  Built for real-world media, vendor, and operational workflows
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/AI-LLM%20Ready-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Focus-Contract%20Intelligence-orange?style=for-the-badge">
</p>

## 🌐 Live App

👉 **Try it here:**  
https://stefanieversace-ai-contract-data-extraction-app-wcsat8.streamlit.app/

---

## 🧠 Overview

Media, production, and vendor agreements are often lengthy, inconsistent, and time-consuming to review manually.

This project demonstrates an **end-to-end AI-assisted workflow** that:

- extracts structured contract data from unstructured text  
- validates outputs against a defined schema  
- applies rule-based risk detection  
- produces analyst-ready outputs for review  

💡 Designed to simulate how AI systems can support **real operational and decision-making workflows**.

---

## ⚙️ End-to-End Pipeline


Contract Document
↓
Extraction (Pattern / LLM-ready)
↓
Validation & Normalisation
↓
Risk Flagging Engine
↓
Final Analyst Output (JSON + Tables)


---

## ✨ Key Features

✔ Structured contract field extraction  
✔ Schema-based validation  
✔ Confidence scoring (field-level + overall)  
✔ Rule-based risk detection  
✔ Human-in-the-loop workflow design  
✔ End-to-end pipeline execution  
✔ Notebook demo for analyst-friendly output  

---

## 📸 Demo 

### Pipeline Execution

<p align="center">
  <img src="Screenshots/pipeline_run.png" width="800">
</p>

---

### Final Structured Output

<p align="center">
  <img src="Screenshots/final_output.png" width="800">
</p>

---

### Risk Detection

<p align="center">
  <img src="Screenshots/risk_flags.png" width="800">
</p>
---

## 📂 Project Structure

```
ai-contract-data-extraction/
│
├── data/
│ └── sample_contracts/
│
├── schemas/
│ └── contract_schema.json
│
├── src/
│ ├── extract.py
│ ├── validate.py
│ ├── risk_flags.py
│ ├── pipeline.py
│
├── outputs/
│ ├── extracted_json/
│ ├── scored_results/
│ └── pipeline_run/
│
├── notebooks/
│ └── demo_walkthrough.ipynb
│
├── docs/
│ └── screenshots/
│
└── README.md
```

---

## ▶️ Usage

Run the full pipeline:

```bash
python src/pipeline.py data/sample_contracts/sample_vendor_agreement.txt
```

## 📊 Output

```
outputs/pipeline_run/
├── 01_extracted.json
├── 02_validated.json
└── 03_final_output.json
```

## 📊 Example Output

```
{
  "agreement_type": "Vendor Services Agreement",
  "parties": ["NBCUniversal", "Production Vendor Ltd"],
  "effective_date": "January 15, 2024",
  "term_length": "12 months",
  "payment_terms": "Net 90",
  "auto_renewal": true,
  "governing_law": "California",
  "exclusivity": true,
  "confidence_score": 0.88,
  "key_risks": [
    "Extended payment terms (>60 days)",
    "Auto-renewal clause present",
    "Exclusivity clause present",
    "Broad or one-sided indemnity language"
  ]
}
```

## 🚨 Risk Detection Engine

This system identifies high-risk contract elements such as:

⚠️Extended payment terms (>60 days)

⚠️ Auto-renewal clauses
  
⚠️ Missing termination flexibility

⚠️ Exclusivity clauses

⚠️ Missing governing law

⚠️ Broad indemnity language

➡️ This transforms the project from data extraction → decision support system

## 📓 Notebook Demo

jupyter notebook notebooks/demo_walkthrough.ipynb

Includes:

- Full pipeline walkthrough
- Structured outputs
- Analyst-friendly tables
- Risk insights

## 🧠 Analyst Insights

LLMs alone are not enough for reliable contract analysis.

This project shows the importance of combining:

- Structured schemas
- Validation layers
- Rule-based controls
- Confidence scoring
- Human review

➡️ Result: more reliable, auditable AI systems

## 🛡️ Responsible AI

- No real contracts used
- Synthetic / redacted data only
- Outputs require human validation
- Designed for auditability
- Acknowledges hallucination risk

## 🔮 Future Improvements

- LLM integration (OpenAI / RAG pipeline)
- Contract clause comparison engine
- Streamlit dashboard for analysts
- Evaluation framework (accuracy metrics)
- Real-time document ingestion

## 💼 Why This Project Matters

This project demonstrates how AI can be applied to:

- Contract intelligence
- Operational workflows
- Risk identification
- Decision support systems

Highly relevant to:

- Media & entertainment
- Vendor management
- Compliance & risk teams

## 👩‍💻 Author

Stefanie Versace
Security Studies Graduate | Cybersecurity | Threat Intelligence

**⭐ If you found this useful, feel free to star the repo!**

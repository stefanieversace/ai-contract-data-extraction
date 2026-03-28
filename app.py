import json
import sys
from pathlib import Path

import streamlit as st

# -------------------------------
# Fix import path for Streamlit Cloud
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))

from extract import ContractExtractor
from validate import validate_contract_data
from risk_flags import append_risks_to_contract

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Contract Intelligence",
    page_icon="📄",
    layout="wide",
)

# -------------------------------
# Header
# -------------------------------
st.title("📄 AI Contract Intelligence")
st.caption("Extract, validate, and risk-flag key terms from unstructured contracts")

# -------------------------------
# File Input
# -------------------------------
st.markdown("### Upload a contract or use the sample file")

sample_path = BASE_DIR / "data" / "sample_contracts" / "sample_vendor_agreement.txt"

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload contract (.txt)", type=["txt"])

with col2:
    use_sample = st.button("Use sample contract")

contract_text = None
source_name = None

# -------------------------------
# Load contract
# -------------------------------
if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")
    source_name = uploaded_file.name

elif use_sample and sample_path.exists():
    contract_text = sample_path.read_text(encoding="utf-8")
    source_name = "Sample Contract"

# -------------------------------
# Process contract
# -------------------------------
if contract_text:

    st.success(f"Loaded: {source_name}")

    extractor = ContractExtractor()
    extracted = extractor.extract(contract_text)

    validated, issues = validate_contract_data(extracted)

    final_output = append_risks_to_contract(validated)

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Summary", "🧾 JSON Output", "🚨 Risk Flags", "⚠️ Validation"]
    )

    # -------------------------------
    # Summary Tab
    # -------------------------------
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Key Fields")
            st.write("**Agreement Type:**", final_output.get("agreement_type"))
            st.write("**Parties:**", ", ".join(final_output.get("parties", [])) or "N/A")
            st.write("**Effective Date:**", final_output.get("effective_date"))
            st.write("**Term Length:**", final_output.get("term_length"))
            st.write("**Payment Terms:**", final_output.get("payment_terms"))

        with col2:
            st.subheader("Flags")
            st.write("**Auto Renewal:**", final_output.get("auto_renewal"))
            st.write("**Governing Law:**", final_output.get("governing_law"))
            st.write("**Exclusivity:**", final_output.get("exclusivity"))
            st.write("**Confidence Score:**", final_output.get("confidence_score"))

    # -------------------------------
    # JSON Tab
    # -------------------------------
    with tab2:
        st.subheader("Final Structured Output")
        st.json(final_output)

    # -------------------------------
    # Risk Tab
    # -------------------------------
    with tab3:
        st.subheader("Identified Risks")

        risks = final_output.get("key_risks", [])

        if risks:
            for risk in risks:
                st.warning(risk)
        else:
            st.success("No risks identified")

    # -------------------------------
    # Validation Tab
    # -------------------------------
    with tab4:
        st.subheader("Validation Issues")

        if issues:
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.success("No validation issues")

    # -------------------------------
    # Download Button
    # -------------------------------
    st.download_button(
        "Download JSON",
        data=json.dumps(final_output, indent=2),
        file_name="contract_analysis.json",
        mime="application/json",
    )

# -------------------------------
# Empty State
# -------------------------------
else:
    st.info("Upload a contract file or click 'Use sample contract' to begin")

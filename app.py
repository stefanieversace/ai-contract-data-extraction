import json
from pathlib import Path

import streamlit as st

import sys
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from extract import ContractExtractor
from validate import validate_contract_data
from risk_flags import append_risks_to_contract


st.set_page_config(
    page_title="AI Contract Intelligence",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Contract Intelligence")
st.caption("Extract, validate, and risk-flag key terms from unstructured contracts.")

st.markdown("Upload a `.txt` contract file or use the built-in sample.")

sample_path = Path("data/sample_contracts/sample_vendor_agreement.txt")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload contract text file", type=["txt"])

with col2:
    use_sample = st.button("Use sample contract")

contract_text = None
source_name = None

if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")
    source_name = uploaded_file.name
elif use_sample and sample_path.exists():
    contract_text = sample_path.read_text(encoding="utf-8")
    source_name = sample_path.name

if contract_text:
    st.success(f"Loaded: {source_name}")

    extractor = ContractExtractor()
    extracted = extractor.extract(contract_text)
    validated, issues = validate_contract_data(extracted)
    final_output = append_risks_to_contract(validated)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Summary", "Final JSON", "Risk Flags", "Validation Issues"]
    )

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Key Fields")
            st.write("**Agreement Type:**", final_output.get("agreement_type"))
            st.write("**Parties:**", ", ".join(final_output.get("parties", [])) or "N/A")
            st.write("**Effective Date:**", final_output.get("effective_date"))
            st.write("**Term Length:**", final_output.get("term_length"))
            st.write("**Payment Terms:**", final_output.get("payment_terms"))
        with c2:
            st.subheader("Flags")
            st.write("**Auto Renewal:**", final_output.get("auto_renewal"))
            st.write("**Governing Law:**", final_output.get("governing_law"))
            st.write("**Exclusivity:**", final_output.get("exclusivity"))
            st.write("**Confidence Score:**", final_output.get("confidence_score"))

    with tab2:
        st.subheader("Final Structured Output")
        st.json(final_output)

    with tab3:
        st.subheader("Identified Risks")
        risks = final_output.get("key_risks", [])
        if risks:
            for risk in risks:
                st.warning(risk)
        else:
            st.info("No risks identified.")

    with tab4:
        st.subheader("Validation Issues")
        if issues:
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.write("No validation issues.")

    st.download_button(
        "Download JSON",
        data=json.dumps(final_output, indent=2),
        file_name="contract_analysis.json",
        mime="application/json",
    )

else:
    st.info("Upload a contract file or click 'Use sample contract' to begin.")

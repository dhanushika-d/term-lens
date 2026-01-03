import streamlit as st
import os
import tempfile
from rag_engine import process_document, analyze_document # Importing backend

st.set_page_config(page_title="Before You Click Agree", page_icon="⚖️")

# Sidebar
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    st.divider()
    
    analysis_choice = st.radio(
        "Analysis Mode",
        ["🚩 Red Flags", "💰 Hidden Costs", "🔒 Privacy Risks"]
    )
    
    analyze_btn = st.button("Analyze Now", type="primary")

# Main Area
st.title("🕵️‍♂️ Before You Click 'Agree'")
st.markdown("### AI Contract Detective")

if uploaded_file is not None:
    # Save file temporarily so the backend can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    st.success(f"✅ Loaded: {uploaded_file.name}")

    if analyze_btn:
        with st.spinner("🧠 Reading the fine print..."):
            try:
                # CALL THE BACKEND (Ingest)
                vector_db = process_document(tmp_file_path)
                
                # DEFINE THE QUESTION based on user button
                if "Red Flags" in analysis_choice:
                    query = "Find the top 3 most dangerous or unfair clauses in this contract. Explain why they are risky."
                elif "Hidden Costs" in analysis_choice:
                    query = "List all fees, penalties, auto-renewals, or financial obligations."
                else:
                    query = "How is my personal data used? Can they sell it to third parties?"
                
                # GET THE ANSWER
                response = analyze_document(vector_db, query)
                
                # SHOW RESULT
                st.markdown("### 📋 Detective's Report")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                os.remove(tmp_file_path) # Cleanup
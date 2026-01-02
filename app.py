import streamlit as st

# 1. Configuration
st.set_page_config(page_title="Before You Click Agree", page_icon="⚖️")

# 2. The Header
st.title("🕵️‍♂️ Before You Click 'Agree'")
st.markdown("""
**Don't sign blindly.** Upload a contract, Terms of Service, or Privacy Policy. 
This AI Detective will find the **Red Flags** 🚩 for you.
""")

# 3. Sidebar for File Upload
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    st.divider()
    
    st.header("2. Analysis Mode")
    analysis_type = st.radio(
        "What should I look for?",
        ["🚫 Red Flags (Risks)", "💰 Hidden Costs", "🔒 Privacy Loopholes", "📄 Summarize Full Text"]
    )
    
    # Add a "Go" button
    analyze_btn = st.button("🔍 Analyze Document")

# 4. Main Display Area (Placeholder)
if uploaded_file is not None:
    st.success("✅ Document Uploaded Successfully!")
    
    # Show a preview (optional)
    st.write(f"**Filename:** {uploaded_file.name}")
    
    if analyze_btn:
        st.info("🤖 The AI is reading your document... (Logic coming soon!)")
        
else:
    st.info("👈 Please upload a PDF from the sidebar to start.")
# Before You Click 'Agree'
### *The AI-Powered Contract Detective*

**Ever clicked "I Agree" without reading the 50-page Terms of Service?**

**Before You Click Agree** is a RAG (Retrieval-Augmented Generation) application that acts as your skeptical, protective lawyer. It scans PDF contracts, hunts for hidden fees, and flags risky clauses before you sign your life away.

---

## What It Does
* **PDF Ingestion:** Upload any contract, lease, or Terms of Service.
* **Smart Analysis:** Uses Azure OpenAI to "read" and understand the legal jargon.
* **Red Flag Detection:** Specifically hunts for unfair terms, hidden costs, and privacy risks.

---

## Tech Stack
* **Frontend:** Streamlit (for the clean, fast UI)
* **AI Logic:** LangChain & Azure OpenAI (GPT-3.5 + Embeddings)
* **Memory:** ChromaDB (Vector Database for document search)
* **Backend:** Python

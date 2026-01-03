import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_CHAT_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_CHAT_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    temperature=0
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
)

PERSIST_DIRECTORY = "./chroma_db"

def process_document(file_path):
    print(f"Processing file: {file_path}")
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    clean_splits = [s for s in splits if s.page_content.strip() != ""]
    
    print(f"Split into {len(clean_splits)} chunks. Ingesting...")
    
    vectorstore = Chroma(
        embedding_function=embeddings, 
        persist_directory=PERSIST_DIRECTORY
    )
    
    batch_size = 5
    for i in range(0, len(clean_splits), batch_size):
        batch = clean_splits[i : i + batch_size]
        try:
            vectorstore.add_documents(batch)
        except Exception as e:
            print(f"❌ Error in batch {i}: {e}")
        time.sleep(1) 
    
    print("Database Ready!")
    return vectorstore

def analyze_document(vectorstore_ignored, query):
    print(f"Analyzing query: {query}")
    
    try:
        # LOAD DB
        print("Loading Database...")
        db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        
        # SEARCH
        print(f"Searching...")
        docs = db.similarity_search(query, k=5)
        
        if not docs:
            return "⚠️ No relevant information found."
            
        print(f"Found {len(docs)} chunks.")
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        # ASK AI
        print("Asking the AI Lawyer...")
        
        system_instruction = f"""You are a skeptical, protective lawyer. 
    Your client is about to sign this contract. 
    
    YOUR TASK:
    1. Answer the user's question based STRICTLY on the provided context.
    2. Look for "Red Flags" (risks, hidden fees, unfair terms).
    3. If you find a risk, start the sentence with "🚩 **RED FLAG:**".
    4. Always cite the section or clause number.

        
        Context:
        {context_text}
        """
        
        messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=query)
        ]
        
        response = llm.invoke(messages)
        print("Analysis Complete!")
        return response.content

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return f"⚠️ Error detail: {str(e)}"
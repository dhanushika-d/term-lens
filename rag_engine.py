import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv

# Load the API Key
load_dotenv()

# Setup GPT-3.5
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
embeddings = OpenAIEmbeddings()

# Setup the Memory (Vector Database location)
PERSIST_DIRECTORY = "./chroma_db"

def process_document(file_path):

    print(f"📄 Processing file: {file_path}")
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # Split text into 1000-character chunks with overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=PERSIST_DIRECTORY
    )
    return vectorstore

def analyze_document(vectorstore, query):

    print(f"Analyzing query: {query}")
    
    # Create the Retriever (The Search Engine) find the 5 chunks of text that are most conceptually similar
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    # The "Paranoid Lawyer" Prompt (System Instruction)
    system_prompt = """You are a skeptical, protective lawyer. 
    Your client is about to sign this contract. 
    
    YOUR TASK:
    1. Answer the user's question based STRICTLY on the provided context.
    2. Look for "Red Flags" (risks, hidden fees, unfair terms).
    3. If you find a risk, start the sentence with "🚩 **RED FLAG:**".
    4. Always cite the section or clause number.
    
    Context:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Build the Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Run
    response = rag_chain.invoke({"input": query})
    return response["answer"]
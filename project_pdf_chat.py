
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
# project_pdf_chat.py
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



# This is a placeholder for the full chain we'll build in the next step
def get_conversational_rag_chain(retriever):
    """Builds the full conversational RAG chain with the fix."""
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

    # 1. Contextualize Question Chain (No changes here)
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    contextualize_q_chain = contextualize_q_prompt | model | StrOutputParser()

    # 2. RAG Chain (No changes here)
    rag_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Keep the answer concise."""

    rag_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", rag_system_prompt),
            ("human", "Context: {context}\n\nQuestion: {question}"),
        ]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(retriever.invoke(x["question"]))))
        | rag_prompt
        | model
        | StrOutputParser()
    )

    # 3. Full Conversational Chain (THIS IS THE FIX)
    # We add a step to wrap the output of contextualize_q_chain into a dictionary.
    full_chain = (
        contextualize_q_chain
        | RunnableLambda(lambda standalone_question: {"question": standalone_question})
        | rag_chain
    )

    return full_chain




# Use Streamlit's caching to store the retriever
@st.cache_resource
def create_retriever_from_pdf(pdf_file):
    """Load, split, and create a retriever from the uploaded PDF."""
    # PyPDFLoader needs a file path. We save the uploaded file temporarily.
    temp_file_path = os.path.join("./", pdf_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(pdf_file.getvalue())

    st.info("Processing your PDF...")
    loader = PyPDFLoader(temp_file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"), transport="rest")
    vector_store = Chroma.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever()
    st.success("PDF processed! You can now ask questions.")
    return retriever

# --- Main App Logic ---
# (Existing UI code from Step 1...)

# Load environment variables
st.set_page_config(page_title="Chat with Your PDF", page_icon="📄")
st.title("📄 Chat with Your PDF")

# UI for uploading a PDF
with st.sidebar:
    st.header("Your PDF Document")
    pdf_file = st.file_uploader("Upload your PDF and click 'Process'", type="pdf")

if not pdf_file:
    st.info("Please upload a PDF file to begin.")
    st.stop()

if pdf_file:
    # Process the PDF and create the retriever
    retriever = create_retriever_from_pdf(pdf_file)

    # Get the full conversational chain
    rag_chain = get_conversational_rag_chain(retriever)

    # The rest of the chat logic will go here in the next step...

# (Add this to the end of your script)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_question := st.chat_input("Ask a question about your PDF"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Prepare the input for the chain
    chain_input = {
        "question": user_question,
        "chat_history": [
            (msg["role"], msg["content"]) for msg in st.session_state.messages[:-1]
        ],
    }

    # Get the AI's response
    with st.spinner("Thinking..."):
        ai_response = rag_chain.invoke(chain_input)

        # Add AI response to chat history and display it
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)
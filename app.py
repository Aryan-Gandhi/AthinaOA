# Importing all the dependencies
import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory

os.environ["OPENAI_API_KEY"] = "<ENTER KEY HERE>"

# Load environment variables from a .env file
load_dotenv()

# Function to load the pdf files and extract text 
def load_document(file):
    pdf_reader = PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Creating chunks of size 1000 from the extracted text
def text_splitter(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = splitter.split_text(text)
    return all_splits

# Creating vector embeddings for the chunks and storing them in the vector store
def get_embeddings(all_splits):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(all_splits, embeddings)
    return vector_store

# Initializing the model and the retriever, and creating a chain for Question Answering
def chat_with_pdf(question, vector_store):
    # System prompt template to guide the model's response behavior
    system_template = """You are an AI assistant tasked with answering questions based on the provided context information. If you don't know the answer, just say 'Please ask me relevant questions!', don't try to make up an answer. Keep the answer short and to the point and do not add text that is not asked. Always say "thanks for asking!" at the end of the answer.
            {context}
            Question: {question}
            Helpful Answer:"""
    
    # Setting up the prompt template
    QA_CHAIN_PROMPT = PromptTemplate.from_template(system_template)

    # Initializing the GPT-4 model
    model = ChatOpenAI(model='gpt-4', max_tokens=1000)

    # Setting up the retriever with the vector store
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})

    # Setting up memory to keep track of the conversation history
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Creating the conversational retrieval chain
    chain = ConversationalRetrievalChain.from_llm(
                    llm=model,
                    retriever=retriever,
                    memory=memory,
                    chain_type='stuff',
                    combine_docs_chain_kwargs={'prompt': QA_CHAIN_PROMPT},
                    verbose=False
                                )
 
    # Getting the answer from the chain
    result = chain.invoke(question)

    return result['answer']

# Function to clear the chat history
def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']

# Main function
if __name__ == "__main__":
    load_dotenv()
    st.header("Chat with Churchill Insurance")

    # File uploader widget for PDF upload
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf:
        # Load and process the PDF file
        data = load_document(pdf)
        chunks = text_splitter(data)
        vector_store = get_embeddings(chunks)

        # Store the vector store in the session state
        st.session_state.vs = vector_store
        st.success('File uploaded, chunked and embedded successfully.')

        # Input widget for user queries
        query = st.text_input("Ask questions about your PDF file:")
        
        if query:
            if 'vs' in st.session_state: 
                vector_store = st.session_state.vs
                answer = chat_with_pdf(query,vector_store)

                 # Display the answer
                st.text_area('LLM Answer: ', value=answer)
                st.divider()

                # Maintain and display chat history
                if 'history' not in st.session_state:
                    st.session_state.history = ''

                    value = f'Q: {query} \nA: {answer}'

                    st.session_state.history = f'{value} \n {"-" * 100} \n {st.session_state.history}'
                    h = st.session_state.history

                    st.text_area(label='Chat History', value=h, key='history', height=400)

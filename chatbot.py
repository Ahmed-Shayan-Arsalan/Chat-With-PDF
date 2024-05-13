# chatbot.py
import os
import PyPDF2
from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

class ChatbotAgent:
    def __init__(self, pdf_filename="Fazail-e-Ramazan English.pdf", conversation_filename="conversation.pdf"):
        self.qa_interface = self.setup_chatbot(pdf_filename, conversation_filename)

    def setup_chatbot(self, pdf_filename, conversation_filename):
        # Extract text from PDF
        pdf_file_obj = open(pdf_filename, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_pages = len(pdf_reader.pages)
        pdf_text = ""

        for page_num in range(num_pages):
            page_obj = pdf_reader.pages[page_num]
            pdf_text += page_obj.extract_text() + "\n\n"

        pdf_file_obj.close()

        # Load conversation history from conversation.txt
        conversation_text = ""
        if os.path.exists(conversation_filename):
            with open(conversation_filename, "r") as conv_file:
                conversation_text = conv_file.read()

        # Combine PDF text and conversation text
        combined_text = pdf_text + "\n\n" + conversation_text

        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = "KEY HERE"

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents([combined_text])

        # Create and save FAISS index
        directory = "index_store"
        vector_index = FAISS.from_documents(texts, OpenAIEmbeddings())
        vector_index.save_local(directory)

        # Load FAISS index
        vector_index = FAISS.load_local("index_store", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

        # Set up retriever and QA interface
        retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        qa_interface = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )

        return qa_interface

    def query_qa_interface(self, query):
        response = self.qa_interface(query)["result"]
        return response

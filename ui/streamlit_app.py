import requests
import streamlit as st

"""
Simple Streamlit interface for the AI Document Assistant.

The UI communicates with the FastAPI backend through HTTP requests.
All document processing and LLM interactions remain inside the API.
"""

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Document Assistant",
    layout="centered"
)

st.title("AI Document Assistant")

st.write("Upload a PDF document and ask questions about its content.")

# File uploader for PDF documents
uploaded_file = st.file_uploader(
    "Choose a PDF",
    type="pdf",
)

if uploaded_file is not None:

    if "document_id" not in st.session_state:

        with st.spinner("Uploading document..."):
            # Send the uploaded PDF to the FastAPI backend for processing and storage
            response = requests.post(
                f"{API_URL}/documents",             
                files={                         
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                },
            )

        if response.ok: 
            data = response.json()                              # dict[str, str] = response.json()
            # Store the document ID in the session state for later use
            st.session_state.document_id = data["document_id"]
            st.success(f"Uploaded {data['filename']}")
        else:
            st.error(response.json()["detail"])

if "document_id" in st.session_state:                           # If a document has been uploaded and its ID is stored in the session state, display the question input and handle the question submission
    question = st.text_input(
        "Ask a question"
    )

    if st.button("Ask"):
        with st.spinner("Loading..."):
            response = requests.post(
                f"{API_URL}/ask",                               # Send the question to the FastAPI backend for processing and answer generation
                json={
                    "document_id": st.session_state.document_id,
                    "question": question,
                },
            )

        if response.ok:
            answer = response.json()                            # dict[str, str] = response.json()
            st.subheader("Answer")
            st.write(answer["answer"])
            st.subheader("Source Pages")
            st.write(answer["source_pages"])
        else:
            st.error(response.json()["detail"])   
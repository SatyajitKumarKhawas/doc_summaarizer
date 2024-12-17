import streamlit as st
import pdfplumber
from transformers import pipeline

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to summarize the extracted text
def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Streamlit app interface
def main():
    st.title("PDF Document Summarizer")
    st.markdown("Upload a PDF file, and this app will generate a summary of its content.")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from PDF
        with st.spinner("Extracting text..."):
            text = extract_text_from_pdf(uploaded_file)
        
        if text:
            st.subheader("Extracted Text:")
            st.text_area("Full Document Text", text, height=300)

            # Generate summary
            st.subheader("Summary:")
            with st.spinner("Summarizing..."):
                summary = summarize_text(text)
            st.write(summary)
        else:
            st.warning("No text found in this PDF.")

if __name__ == "__main__":
    main()

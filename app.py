import streamlit as st
import pandas as pd
import difflib
import docx
from io import BytesIO
import re
from html import escape

def read_text(file):
    return file.read().decode("utf-8")

def read_word(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_excel(file):
    df = pd.read_excel(file)
    return df.to_csv(index=False)

def highlight_differences(text1, text2):
    d = difflib.ndiff(text1.splitlines(), text2.splitlines())
    highlighted_text1, highlighted_text2 = "", ""
    
    for line in d:
        if line.startswith("  "):
            highlighted_text1 += escape(line[2:]) + "\n"
            highlighted_text2 += escape(line[2:]) + "\n"
        elif line.startswith("- "):
            highlighted_text1 += f'<span style="background-color: #ffcccc">{escape(line[2:])}</span>\n'
        elif line.startswith("+ "):
            highlighted_text2 += f'<span style="background-color: #ccffcc">{escape(line[2:])}</span>\n'
    
    return highlighted_text1, highlighted_text2

def main():
    st.title("Satya's DiffMate App")
    
    st.markdown("""
    **Instructions:**
    1. Upload two files of the same type (TXT, DOCX, or XLSX) for comparison.
    2. The app will extract and display the content side by side.
    3. Differences will be highlighted:
       - **Red Highlight**: Text removed from File 1.
       - **Green Highlight**: Text added in File 2.
    4. Scroll through both panels to review changes easily.
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        file1 = st.file_uploader("Upload First File", type=["txt", "docx", "xlsx"])
        file2 = st.file_uploader("Upload Second File", type=["txt", "docx", "xlsx"])
    
    if file1 and file2:
        ext1, ext2 = file1.name.split(".")[-1], file2.name.split(".")[-1]
        
        if ext1 != ext2:
            st.error("Please upload files of the same type")
            return
        
        if ext1 == "txt":
            text1, text2 = read_text(file1), read_text(file2)
        elif ext1 == "docx":
            text1, text2 = read_word(file1), read_word(file2)
        elif ext1 == "xlsx":
            text1, text2 = read_excel(file1), read_excel(file2)
        else:
            st.error("Unsupported file format")
            return
        
        highlighted_text1, highlighted_text2 = highlight_differences(text1, text2)
        
        with col2:
            col_left, col_right = st.columns(2)
            with col_left:
                st.subheader("File 1 Contents")
                st.markdown(f'<div style="white-space: pre-wrap; height: 600px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">{highlighted_text1}</div>', unsafe_allow_html=True)
            with col_right:
                st.subheader("File 2 Contents")
                st.markdown(f'<div style="white-space: pre-wrap; height: 600px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">{highlighted_text2}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

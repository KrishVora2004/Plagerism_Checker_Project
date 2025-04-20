import streamlit as st
import fitz  # PyMuPDF for PDFs
from compare_reports import compute_similarity
from extract_text import extract_text_from_pdf
from textstat import flesch_reading_ease

# Function to generate title suggestions if plagiarism is high
def generate_suggestions(title):
    suggestions = [
        f"Improved version of: {title}",
        f"Enhanced {title.split()[0]} project" if len(title.split()) > 0 else "Enhanced project",
        f"Next generation {title}"
    ]
    return suggestions[:3]

# Streamlit UI
st.title("Project Report Plagiarism Checker")

uploaded_file = st.file_uploader("Upload a project report (.pdf)", type=["pdf"])

if uploaded_file is not None:
    # Extract title & abstract directly from uploaded PDF (without saving)
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
        title, abstract = extract_text_from_pdf(pdf)

    # Display extracted information
    st.subheader("Extracted Title:")
    st.write(title)

    st.subheader("Extracted Abstract:")
    st.write(abstract)

    # Check for plagiarism
    if st.button("Check Plagiarism"):
        results = compute_similarity(title, abstract)

        if results:
            st.write("### Potential Matches Found:")
            for report, title_score, abstract_score in results:
                st.write(f"📄 **{report}**")
                st.write(f"📌 Title Similarity: {title_score:.2f}%")
                st.write(f"📌 Abstract Similarity: {abstract_score:.2f}%")
                st.write("---")
        else:
            st.write("✅ No significant plagiarism detected.")

        # Additional Features
        st.subheader("Additional Analysis")

        # Title uniqueness score: (1 - plagiarism_score) / 100
        title_similarity = results[0][1] if results else 0  # Get title similarity from results
        uniqueness_score = max(0, (1 - title_similarity / 100))

        # Readability score using Flesch Reading Ease formula
        rsc= flesch_reading_ease(abstract)
        readability_score =rsc+10

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Uniqueness Score", 
              f"{uniqueness_score:.2f}/1.0",
              help="Higher is better (1.0 = completely unique)")

        with col2:
            st.metric("Readability (Flesch)", 
              f"{readability_score:.1f}",
              help="60+ is good (higher = easier to read)")

        if title_score > 50 and abstract_score < 30:
            st.warning("🚨 Your title is highly plagiarized! Consider changing it.")
            suggested_titles = generate_suggestions(title)
            st.write("### Suggested Titles:")
            for suggestion in suggested_titles:
                st.write(f"🔹 {suggestion}")


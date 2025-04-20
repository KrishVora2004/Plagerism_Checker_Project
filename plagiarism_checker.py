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

def format_student_group(raw_text):
    """Formats student names and IDs from newline-separated text into a readable list."""
    lines = raw_text.strip().split('\n')
    formatted = []

    for i in range(0, len(lines), 2):
        name = lines[i]
        student_id = lines[i+1] if i + 1 < len(lines) else ""
        formatted.append(f"{name} ({student_id})\n")

    return '\n'.join(formatted)

def compute_score_stats(results):
    """Computes weighted average and max scores for title and abstract."""
    avg_title = (sum(r[1] for r in results) / len(results)) * 3
    avg_abstract = (sum(r[2] for r in results) / len(results)) * 1.5
    max_title = max(r[1] for r in results)
    max_abstract = max(r[2] for r in results)
    return avg_title, avg_abstract, max_title, max_abstract


# Streamlit UI
st.title("Project Report Plagiarism Checker")

uploaded_file = st.file_uploader("Upload a project report (.pdf)", type=["pdf"])

if uploaded_file is not None:
    # Extract title & abstract directly from uploaded PDF (without saving)
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
        title, abstract,matched_students_cur, matched_guide_cur = extract_text_from_pdf(pdf)

    # Display extracted information
    st.subheader("Extracted Title:")
    st.write(title)

    st.subheader("Extracted Abstract:")
    st.write(abstract)

    # Check for plagiarism
    if st.button("Check Plagiarism"):
        results = compute_similarity(title, abstract)

        if results:
            # st.write("### Potential Matches Found:")
            avg_title, avg_abstract, max_title, max_abstract = compute_score_stats(results)

            if(max_title>avg_title or max_abstract>avg_abstract):
                st.write("### Potential Matches Found:")

                # Filter and display only significant results
                for report, title_score, abstract_score,students,guide, in results:
                    title_score = max(0, title_score)
                    abstract_score = max(0, abstract_score)

                    if title_score > avg_title or abstract_score > avg_abstract:
                        st.write(f"📄 **{report}**")
                        st.write(f"📌 Title Similarity: {title_score:.2f}%")
                        st.write(f"📌 Abstract Similarity: {abstract_score:.2f}%")
                        st.write("\n")
                        st.write(f"🎓 **Student Group:**\n {format_student_group(students)}")
                        st.write(f"🧑‍🏫 **Guide:** {guide}")
                        st.write("---")
            else:
                st.write("✅ No significant plagiarism detected.")
                st.write("---")

        else:
            st.write("✅ No significant plagiarism detected.")
            st.write("---")

        # Additional Features
        st.subheader("Additional Analysis on Title")

        # Title uniqueness score: (1 - plagiarism_score) / 100
        title_similarity = results[0][1] if results else 0  # Get title similarity from results
        uniqueness_score = max(0, (1 - max_title / 100))

        # Readability score using Flesch Reading Ease formula
        rsc= flesch_reading_ease(abstract)
        readability_score =abs(rsc+10)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Uniqueness Score", 
              f"{uniqueness_score:.2f}/1.0",
              help="Higher is better (1.0 = completely unique)")

        with col2:
            st.metric("Readability (Flesch)", 
              f"{readability_score:.1f}",
              help="60+ is good (higher = easier to read)")

        #     if title_score > 50 and abstract_score < 30:
        #         suggested_titles = generate_suggestions(title)
        #         st.write("### Suggested Titles:")
        #         for suggestion in suggested_titles:
        #             st.write(f"🔹 {suggestion}")


# to make datbase: python compare_reports.py
#
#to run the app: python -m streamlit run plagiarism_checker.py
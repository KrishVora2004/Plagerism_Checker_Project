# Plagerism_Checker_Project

A Streamlit-based web application that detects plagiarism in undergraduate project reports by analyzing titles and abstracts, with additional features like title uniqueness, readability scoring, and title suggestions for improvement.

# Features
* 🔍 Extracts title, abstract, student group, and guide’s name from uploaded PDFs.
* 📊 Computes plagiarism scores using cosine similarity against a department library.
* 📈 Shows title uniqueness score and Flesch Reading Ease readability.
* 💡 Suggests alternative project titles if plagiarism is detected.
* ✅ Displays only significant matches (based on average score thresholds).

# Technologies Used
* Python
* Streamlit – UI framework
* PyMuPDF (fitz) – PDF parsing
* Scikit-learn – TF-IDF and Cosine Similarity
* textstat – Readability scores
* Regex – Custom text extraction logic

# Notes
* Place previous project reports (PDFs) inside the libraries_inserted/ folder.
* Run compare_reports.py once to populate the database (report_database.json).
* Then, use plagiarism_checker.py to upload and analyze new project reports.

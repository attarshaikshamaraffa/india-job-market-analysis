# India Job Market Analysis

Analysis of 5,000 tech job postings (Kaggle dataset) using Python, SQL and Streamlit.

**Live dashboard:** https://YOUR-APP.streamlit.app

## Key findings
- Median pay rises steeply with experience: about 5.5 LPA average for freshers to 53 LPA for leads.
- Python appears in 31% of fresher postings, the most of any skill.
- About 40% of postings are remote.
- City differences are small compared with experience differences.

## What I did
- Cleaned the data with pandas (dates, whitespace, duplicates).
- Split the skills column into its own table and joined it with SQL.
- Answered business questions in SQLite (GROUP BY, JOIN, HAVING).
- Built an interactive Streamlit dashboard with filters.

## Run locally
pip install -r requirements.txt
streamlit run app/dashboard.py

## Data
Kaggle dataset of India job postings. Not scraped by me.

## Tools
Python, pandas, SQL (SQLite), Plotly, Streamlit, Git

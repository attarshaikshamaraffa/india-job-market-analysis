from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="India Job Market", layout="wide")

DATA = Path(__file__).resolve().parent.parent / "data" / "clean"
ORDER = ["Fresher", "Junior", "Mid", "Senior", "Lead"]


@st.cache_data
def load():
    jobs = pd.read_csv(DATA / "jobs_clean.csv")
    skills = pd.read_csv(DATA / "job_skills.csv")
    return jobs, skills


jobs, skills = load()

st.title("India Job Market Analysis")
st.caption("5,000 tech job postings from a Kaggle dataset. Analysis with Python and SQL.")

st.sidebar.header("Filters")
exp = st.sidebar.multiselect("Experience", ORDER, default=ORDER)
cities = st.sidebar.multiselect(
    "City", sorted(jobs["city"].unique()), default=sorted(jobs["city"].unique())
)
min_jobs = st.sidebar.slider("Min jobs per city (for city chart)", 10, 100, 30)

f = jobs[jobs["experience_group"].isin(exp) & jobs["city"].isin(cities)]

if f.empty:
    st.warning("No jobs match these filters. Change the filters on the left.")
    st.stop()

sk = skills[skills["job_id"].isin(f["job_id"])]

c1, c2, c3 = st.columns(3)
c1.metric("Job postings", f"{len(f):,}")
c2.metric("Median salary (LPA)", f"{f['salary_lpa'].median():.1f}")
c3.metric("Most demanded skill", sk["skill"].value_counts().idxmax())

by_exp = (
    f.groupby("experience_group")["salary_lpa"].median()
    .reindex(ORDER).dropna().reset_index()
)
fig1 = px.bar(by_exp, x="experience_group", y="salary_lpa",
              title="Median salary by experience (LPA)",
              labels={"experience_group": "Experience", "salary_lpa": "Median LPA"})
st.plotly_chart(fig1, use_container_width=True)

left, right = st.columns(2)

top = sk["skill"].value_counts().head(10).rename_axis("skill").reset_index(name="postings")
fig2 = px.bar(top.sort_values("postings"), x="postings", y="skill", orientation="h",
              title="Top 10 skills in demand")
left.plotly_chart(fig2, use_container_width=True)

by_city = f.groupby("city").agg(jobs=("job_id", "count"),
                                median_salary=("salary_lpa", "median")).reset_index()
by_city = by_city[by_city["jobs"] >= min_jobs].sort_values("median_salary")
if by_city.empty:
    right.info("No city has enough jobs. Lower the slider on the left.")
else:
    fig3 = px.bar(by_city, x="median_salary", y="city", orientation="h",
                  title=f"Median salary by city (cities with {min_jobs}+ jobs)")
    right.plotly_chart(fig3, use_container_width=True)

st.subheader("Key insights")
st.markdown(
    "- Pay rises about 10x from Fresher (5.5 LPA avg) to Lead (53.0 LPA avg).\n"
    "- Python appears in 31% of fresher postings, the most of any skill.\n"
    "- About 40% of postings are Remote.\n"
    "- City differences are small compared with experience differences."
)
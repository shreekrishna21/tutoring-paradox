import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_rows", 100)

DATA = "/home/Fall2026 Share folder/final-project/Topic5_Education_The_Tutoring_Paradox/data"
read = lambda name: pd.read_csv(f"{DATA}/{name}", dtype={"student_id": str})

grades = read("term_grades.csv")
courses = read("courses.csv")
students = read("students.csv")
refs = read("tutoring_referrals.csv")

# Check the raw grade values before trusting the fail flag
print(grades["term_grade"].value_counts(dropna=False))

# Keep the three tutored subjects
df = grades.merge(courses[["course_code", "subject_area"]], on="course_code")
df = df[df["subject_area"].isin(["Mathematics", "English Language Arts", "Science"])]

# Mark failures: F in term 1, below 60 in terms 2 and 3
pct = pd.to_numeric(df["term_grade"], errors="coerce")
df["failed"] = df["term_grade"].eq("F") | pct.lt(60)

# Mark whether the student was referred in that subject
referred = refs[["student_id", "subject_area"]].drop_duplicates().assign(referred=True)
df = df.merge(referred, on=["student_id", "subject_area"], how="left")
df["referred"] = df["referred"].eq(True)

# Add prior GPA, keeping blanks as their own group
df = df.merge(students[["student_id", "prior_year_gpa"]], on="student_id")
df["gpa_band"] = pd.cut(df["prior_year_gpa"], [0, 1, 2, 3, 4], include_lowest=True)

print(df.groupby("referred")["failed"].agg(["mean", "size"]))
print(df.groupby(["gpa_band", "referred"], dropna=False, observed=True)["failed"]
        .agg(["mean", "size"]))


# Failure rate by term, grouped by when the student was referred
dates = pd.to_datetime(refs["referral_date"])
refs["referral_term"] = 1 + (dates > "2025-10-31").astype(int) + (dates > "2026-02-13").astype(int)

timing = df.merge(refs[["student_id", "subject_area", "referral_term"]],
                   on=["student_id", "subject_area"])

print(refs["referral_term"].value_counts().sort_index())
print(timing.pivot_table(index="referral_term", columns="term", values="failed"))
print(df[~df["referred"]].groupby("term")["failed"].mean())


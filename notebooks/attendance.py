import pandas as pd

pd.set_option("display.width", 120)

DATA = "/home/Fall2026 Share folder/final-project/Topic5_Education_The_Tutoring_Paradox/data"
read = lambda name: pd.read_csv(f"{DATA}/{name}", dtype={"student_id": str})

grades = read("term_grades.csv")
courses = read("courses.csv")
students = read("students.csv")
sessions = read("tutoring_sessions.csv.gz")

# Clean the session log and report what changed
print("Raw subject labels:", sessions["subject_area"].unique().tolist())
print("Rows before cleaning:", len(sessions))
sessions["subject_area"] = sessions["subject_area"].str.strip()
print("Exact copy rows:", sessions.duplicated().sum())
sessions = sessions.drop_duplicates()
print("Rows after cleaning:", len(sessions))

# Data checks
print("Repeated sessions:", sessions.duplicated(["student_id", "subject_area", "session_date"]).sum())
print(pd.crosstab(sessions["attendance"], sessions["minutes"]))

# Attendance rate for each student in each subject
sessions["present"] = sessions["attendance"].eq("Present")
att = sessions.groupby(["student_id", "subject_area"])["present"].agg(
    scheduled="size", attended="sum").reset_index()
att["attendance_rate"] = att["attended"] / att["scheduled"]

print("Student-subject pairs:", len(att))
print(att["attendance_rate"].describe())

# Attendance for bus riders vs. non-riders
att = att.merge(students[["student_id", "bus_rider"]], on="student_id")
print(att.groupby("bus_rider")["attendance_rate"].agg(["mean", "size"]))

# Term 3 failure rate by attendance level
term3 = grades[grades["term"] == 3].merge(courses[["course_code", "subject_area"]], on="course_code")
term3["failed"] = pd.to_numeric(term3["term_grade"], errors="coerce").lt(60)
result = att.merge(term3[["student_id", "subject_area", "failed"]], on=["student_id", "subject_area"])
result["attendance_band"] = pd.cut(result["attendance_rate"], [0, 0.25, 0.5, 0.75, 1], include_lowest=True)
print(result.groupby("attendance_band", observed=True)["failed"].agg(["mean", "size"]))

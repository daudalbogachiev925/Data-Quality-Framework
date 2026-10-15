import streamlit as st
import pandas as pd
import numpy as np
from src.rules import Rule, not_null, is_positive, in_range, matches_regex
from src.validator import DataValidator
from src.scoring import compute_score
from src.reports import to_dataframe, summary_report

st.set_page_config(page_title="Data Quality", layout="wide")
st.title("✅ Data Quality Framework")

np.random.seed(42)
df = pd.DataFrame({
    "customer_id": range(1, 1001),
    "email": [f"user{i}@ex.com" if np.random.random() > 0.05 else None for i in range(1000)],
    "age": [int(np.random.normal(40, 15)) for _ in range(1000)],
    "salary": [np.random.normal(80000, 20000) if np.random.random() > 0.1 else -1 for _ in range(1000)],
    "phone": [f"+7{np.random.randint(1000000000, 9999999999)}" for _ in range(1000)],
})

rules = [
    Rule("r1", "customer_id not null", "completeness", "customer_id", not_null, "critical"),
    Rule("r2", "email not null", "completeness", "email", not_null, "high"),
    Rule("r3", "email format", "validity", "email", matches_regex(r"^[\w\.\-]+@[\w\.\-]+\.\w+$"), "medium"),
    Rule("r4", "age in range 18-100", "validity", "age", in_range(18, 100), "high"),
    Rule("r5", "salary positive", "validity", "salary", is_positive, "critical"),
    Rule("r6", "phone format", "validity", "phone", matches_regex(r"^\+7\d{10}$"), "medium"),
]

validator = DataValidator(rules)
results = validator.validate(df)
results.append(validator.validate_unique(df, "customer_id", "uq_customer", "critical"))

score = compute_score(results)
summary = summary_report(results, score)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall Score", f"{score['score']}%")
c2.metric("Grade", score["grade"])
c3.metric("Passed", summary["passed"])
c4.metric("Failed", summary["failed"])

st.subheader("По dimensions")
st.bar_chart(pd.Series(score["by_dimension"]))

st.subheader("Результаты правил")
st.dataframe(to_dataframe(results))

st.subheader("❌ Failed Rules")
failed = [r for r in results if r["status"] == "FAIL"]
if failed:
    for r in failed:
        st.error(f"**{r['rule']}** ({r['column']}) — pass rate: {r['pass_rate']*100:.1f}% · severity: {r['severity']}")
else:
    st.success("Все правила пройдены!")

st.subheader("Данные")
st.dataframe(df.head(50))

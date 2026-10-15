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
    Rule("r2", "email

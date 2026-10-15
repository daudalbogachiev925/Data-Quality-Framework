import pandas as pd
from src.rules import Rule

class DataValidator:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, df: pd.DataFrame):
        results = []
        for rule in self.rules:
            if rule.column not in df.columns:
                results.append({
                    "rule_id": rule.id, "rule": rule.name,
                    "dimension": rule.dimension, "column": rule.column,
                    "status": "SKIPPED", "passed": 0, "total": len(df),
                    "pass_rate": 0.0, "severity": rule.severity,
                })
                continue

            series = df[rule.column]
            passed = 0
            for v in series:
                try:
                    if rule.check(v):
                        passed += 1
                except Exception:
                    pass

            total = len(series)
            pass_rate = passed / total if total else 0
            results.append({
                "rule_id": rule.id, "rule": rule.name,
                "dimension": rule.dimension, "column": rule.column,
                "status": "PASS" if pass_rate >= 0.95 else "FAIL",
                "passed": passed, "total": total,
                "pass_rate": round(pass_rate, 3),
                "severity": rule.severity,
            })
        return results

    def validate_unique(self, df, column, rule_id="uq_1", severity="high"):
        if column not in df.columns:
            return {"status": "SKIPPED"}
        from src.rules import is_unique
        ok = is_unique(df[column].tolist())
        return {
            "rule_id": rule_id, "rule": f"unique({column})",
            "dimension": "uniqueness", "column": column,
            "status": "PASS" if ok else "FAIL",
            "passed": int(df[column].nunique()), "total": len(df),
            "pass_rate": round(df[column].nunique() / max(len(df), 1), 3),
            "severity": severity,
        }

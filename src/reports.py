import pandas as pd
from datetime import datetime

def to_dataframe(results):
    return pd.DataFrame(results)

def summary_report(results, score):
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "total_rules": len(results),
        "passed": sum(1 for r in results if r["status"] == "PASS"),
        "failed": sum(1 for r in results if r["status"] == "FAIL"),
        "score": score,
    }

def failed_rules(results):
    return [r for r in results if r["status"] == "FAIL"]

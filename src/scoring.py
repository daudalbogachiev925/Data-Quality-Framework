SEVERITY_WEIGHTS = {"low": 1, "medium": 2, "high": 3, "critical": 5}

def compute_score(results):
    if not results:
        return {"score": 0.0, "by_dimension": {}, "by_severity": {}}
    total_weight = 0
    weighted_score = 0
    by_dim = {}
    by_sev = {}
    for r in results:
        if r["status"] == "SKIPPED":
            continue
        w = SEVERITY_WEIGHTS.get(r["severity"], 1)
        total_weight += w
        weighted_score += w * r["pass_rate"]
        by_dim.setdefault(r["dimension"], []).append(r["pass_rate"])
        by_sev.setdefault(r["severity"], []).append(r["pass_rate"])
    overall = weighted_score / total_weight if total_weight else 0
    return {
        "score": round(overall * 100, 1),
        "by_dimension": {k: round(sum(v)/len(v)*100, 1) for k, v in by_dim.items()},
        "by_severity": {k: round(sum(v)/len(v)*100, 1) for k, v in by_sev.items()},
        "grade": "A" if overall >= 0.95 else "B" if overall >= 0.85 else
                 "C" if overall >= 0.7 else "D" if overall >= 0.5 else "F",
    }

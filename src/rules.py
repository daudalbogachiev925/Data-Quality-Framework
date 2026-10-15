from dataclasses import dataclass, field
from typing import Callable, Any, Optional

@dataclass
class Rule:
    id: str
    name: str
    dimension: str
    column: str
    check: Callable[[Any], bool]
    severity: str = "medium"  # low/medium/high/critical
    description: str = ""

def not_null(value):
    return value is not None and value != ""

def is_positive(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False

def in_range(lo, hi):
    def _check(value):
        try:
            return lo <= float(value) <= hi
        except (TypeError, ValueError):
            return False
    return _check

def matches_regex(pattern):
    import re
    rx = re.compile(pattern)
    def _check(value):
        return isinstance(value, str) and bool(rx.match(value))
    return _check

def is_unique(values):
    """Проверка уникальности на уровне колонки."""
    non_null = [v for v in values if v is not None]
    return len(non_null) == len(set(non_null))

def is_fresh(max_days, date_value_fn):
    from datetime import datetime, timedelta
    def _check(value):
        try:
            d = date_value_fn(value)
            return (datetime.utcnow() - d) <= timedelta(days=max_days)
        except Exception:
            return False
    return _check

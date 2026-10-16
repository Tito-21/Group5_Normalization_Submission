import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "raw_data/big3_construction_raw_data.csv"

KEY_1NF = ["ProjectID", "WorkerName", "WorkerSkill", "WorkerCertification",
           "SupplierName", "SupplierPhone", "MaterialSupplied", "EquipmentUsed"]


def load(path):
    with open(os.path.join(ROOT, path), newline="") as f:
        return list(csv.DictReader(f))


def split(value):
    return value.split("|")


def is_unique(rows, cols):
    return len({tuple(r[c] for c in cols) for r in rows}) == len(rows)


def holds(rows, lhs, rhs):
    seen = {}
    for r in rows:
        k = tuple(r[c] for c in lhs)
        if seen.setdefault(k, tuple(r[c] for c in rhs)) != tuple(r[c] for c in rhs):
            return False
    return True


class Report:
    def __init__(self, title):
        self.title = title
        self.failures = 0
        print(f"== {title}")

    def check(self, label, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  ({detail})" if detail and not ok else ""))
        self.failures += not ok

    def note(self, label):
        print(f"  [NOTE] {label}")

    def finish(self):
        status = "all checks passed" if not self.failures else f"{self.failures} check(s) FAILED"
        print(f"== {self.title}: {status}\n")
        sys.exit(1 if self.failures else 0)

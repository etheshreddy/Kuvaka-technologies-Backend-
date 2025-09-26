# app/utils/csv_parser.py
import csv
from io import StringIO
from typing import List, Dict

def parse_csv_bytes(file_bytes: bytes) -> List[Dict[str, str]]:
    """
    Parse CSV bytes (uploaded file) into list of dicts.
    Expects header: name,role,company,industry,location,linkedin_bio
    """
    decoded = file_bytes.decode("utf-8-sig")  # handle BOM if present
    reader = csv.DictReader(StringIO(decoded))
    rows = []
    for row in reader:
        # Normalize keys by stripping whitespace
        normalized = {k.strip(): (v.strip() if v is not None else "") for k, v in row.items()}
        rows.append(normalized)
    return rows

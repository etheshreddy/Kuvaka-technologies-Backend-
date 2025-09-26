# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from app.models import Offer
from app.scoring.pipeline import score_lead
from app.utils.csv_parser import parse_csv_bytes
from app.storage.db import OFFERS, LEADS, RESULTS

app = FastAPI(title="Lead Scoring Backend")

# POST /offer
@app.post("/offer")
async def create_offer(offer: Offer):
    OFFERS["current_offer"] = offer.dict()
    return {"message": "Offer saved successfully", "offer": offer.dict()}

# POST /leads/upload
@app.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
    """
    Accept CSV file upload, parse and store leads in in-memory LEADS.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    rows = parse_csv_bytes(content)

    # validate/normalize rows (ensure keys exist)
    expected = ["name", "role", "company", "industry", "location", "linkedin_bio"]
    parsed = []
    for r in rows:
        # lower-case header keys if needed
        # normalize keys
        normalized = {k.strip(): v for k, v in r.items()}
        # ensure all expected keys exist
        for key in expected:
            if key not in normalized:
                normalized[key] = ""
        parsed.append(normalized)

    # Replace LEADS with uploaded ones
    LEADS.clear()
    LEADS.extend(parsed)
    return {"message": f"Uploaded {len(parsed)} leads", "uploaded": len(parsed)}

# POST /score
@app.post("/score")
async def score_leads():
    if "current_offer" not in OFFERS:
        raise HTTPException(status_code=400, detail="No offer available. Please POST /offer first.")
    if not LEADS:
        raise HTTPException(status_code=400, detail="No leads uploaded. Please POST /leads/upload first.")

    RESULTS.clear()
    offer = OFFERS["current_offer"]
    target_industries = offer.get("ideal_use_cases", []) or []

    for lead in LEADS:
        scored = score_lead(lead, offer, target_industries)
        RESULTS.append(scored)

    return {"message": f"Scored {len(RESULTS)} leads successfully"}

# GET /results
@app.get("/results")
async def get_results():
    if not RESULTS:
        raise HTTPException(status_code=400, detail="No results available. Please POST /score first.")
    return JSONResponse(content=RESULTS)

# GET /results/export (CSV)
@app.get("/results/export")
async def export_results_csv():
    if not RESULTS:
        raise HTTPException(status_code=400, detail="No results available. Please POST /score first.")

    import csv
    from io import StringIO

    csv_file = StringIO()
    fieldnames = ["name", "role", "company", "intent", "score", "reasoning"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in RESULTS:
        # ensure only fieldnames are written
        writer.writerow({k: row.get(k, "") for k in fieldnames})

    csv_file.seek(0)
    return StreamingResponse(csv_file, media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=results.csv"})

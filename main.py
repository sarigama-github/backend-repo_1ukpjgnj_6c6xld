import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Wardrobeitem, Review, Pickuprequest, Luxurykyc

app = FastAPI(title="Sirwa API", description="Backend for Sirwa platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sirwa API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Wardrobe Gallery endpoints
@app.post("/api/wardrobe", response_model=dict)
def create_wardrobe_item(item: Wardrobeitem):
    try:
        inserted_id = create_document("wardrobeitem", item)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/wardrobe", response_model=List[dict])
def list_wardrobe_items(limit: Optional[int] = 50):
    try:
        docs = get_documents("wardrobeitem", limit=limit)
        # Convert ObjectId to string if present
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reviews endpoints
@app.post("/api/reviews", response_model=dict)
def create_review(review: Review):
    try:
        inserted_id = create_document("review", review)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews", response_model=List[dict])
def list_reviews(limit: Optional[int] = 50):
    try:
        docs = get_documents("review", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pickup Requests
@app.post("/api/pickup", response_model=dict)
def create_pickup(req: Pickuprequest):
    try:
        inserted_id = create_document("pickuprequest", req)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Luxury KYC
@app.post("/api/luxury-kyc", response_model=dict)
def submit_luxury_kyc(payload: Luxurykyc):
    try:
        inserted_id = create_document("luxurykyc", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

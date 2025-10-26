from fastapi import FastAPI, UploadFile, Form
from core.query_handler import process_query
from core.scraper import scrape_pinterest
from core.recommender import recommend_outfits
from core.feedback import record_feedback
from core.storage import load_json, save_json

app = FastAPI(title="FitFindr API")

@app.post("/query")
async def query_user(style: str = Form(...), image: UploadFile = None):
    user_data = await process_query(style, image)
    save_json("users.json", [user_data])
    return {"message": "Query processed", "user": user_data}

@app.post("/scrape")
def scrape_items_route(payload: dict):
    keyword = payload.get("keyword", "vintage streetwear")
    items = scrape_pinterest(keyword)
    save_json("items.json", items)
    return {"count": len(items), "items": items}

@app.post("/recommend")
def recommend_route():
    user = load_json("users.json")[0]
    items = load_json("items.json")
    recs = recommend_outfits(user, items)
    save_json("recommendations.json", recs)
    return recs

@app.post("/feedback")
def feedback_route(payload: dict):
    record_feedback(payload)
    return {"message": "Feedback saved"}

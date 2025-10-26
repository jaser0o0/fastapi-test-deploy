from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/")
def home():
    return {"message": "Hello from DigitalOcean 👋"}

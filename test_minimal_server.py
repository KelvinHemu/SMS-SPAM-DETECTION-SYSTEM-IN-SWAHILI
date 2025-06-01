#!/usr/bin/env python3
from fastapi import FastAPI

app = FastAPI(
    title="Minimal Test Server",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Minimal server working"}

@app.get("/test")
async def test():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_minimal_server:app", host="0.0.0.0", port=8001, reload=False) 
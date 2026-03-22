from fastapi import FastAPI
from api.ingest import router as ingest_router
from api.digest import router as digest_router
import uvicorn
app = FastAPI()


app.include_router(ingest_router, prefix="/ingest")
app.include_router(digest_router, prefix="/digest")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
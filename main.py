from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
import app.schemas as schemas, app.crud as crud
from app.utils import validate_url

app = FastAPI(title="URL Shortener", version="1.0.0")

Base.metadata.create_all(bind=engine)

@app.get("/health", tags=["service"])
def healthcheck():
    return {"status": "ok"}

@app.post("/api/v1/shorten", response_model=schemas.ShortenResponse, tags=["shortener"], status_code=201)
def shorten(req: schemas.ShortenRequest, request: Request, db: Session = Depends(get_db)):
    validate_url(req.url)
    try:
        entry = crud.create_short_url(db, req.url)
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Failed to generate unique code")

    base = str(request.base_url).rstrip("/")
    short_url = f"{base}/s/{entry.code}"
    return schemas.ShortenResponse(code=entry.code, short_url=short_url)

@app.get("/s/{code}", tags=["redirect"])
def redirect(code: str, db: Session = Depends(get_db)):
    entry = crud.get_by_code(db, code)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code not found")
    crud.increment_click(db, entry)
    return RedirectResponse(url=entry.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/api/v1/stats/{code}", response_model=schemas.StatsResponse, tags=["stats"])
def stats(code: str, db: Session = Depends(get_db)):
    entry = crud.get_by_code(db, code)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code not found")
    return schemas.StatsResponse(
        code=entry.code,
        url=entry.original_url,
        clicks=entry.click_count or 0,
        created_at=entry.created_at,
    )
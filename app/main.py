from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from app.analyzer.ingest import save_and_extract, cleanup_temp_dir
from app.analyzer.parsers import parse_dump
from app.analyzer.heuristics import analyze_bundle

app = FastAPI(title="MKE Support Dump Analyzer")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def handle_upload(request: Request, file: UploadFile = File(...)):
    temp_path = await save_and_extract(file)
    try:
        # Parse
        parsed_data = await parse_dump(temp_path)
        
        # Analyze
        analysis_result = analyze_bundle(temp_path, parsed_data)
        
        return templates.TemplateResponse("report.html", {
            "request": request,
            "analysis": analysis_result
        })
    finally:
        # Cleanup
        cleanup_temp_dir(temp_path)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

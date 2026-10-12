from fastapi import FastAPI

app = FastAPI(
    title="DocuMind AI API",
    description="Backend API for the DocuMind AI document intelligence platform",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy",
            "service": "documind-api"
            }

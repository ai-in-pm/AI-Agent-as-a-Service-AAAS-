from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.api import (
    keyboard_routes, 
    scheduler_routes, 
    stakeholder_routes, 
    browser_routes,
    research_routes,
    technical_routes,
    business_routes
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="PhD-Level AI Agent as a Service",
    description="Advanced AI Agent with research, technical expertise, and business intelligence capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(keyboard_routes.router)
app.include_router(scheduler_routes.router)
app.include_router(stakeholder_routes.router)
app.include_router(browser_routes.router)
app.include_router(research_routes.router)
app.include_router(technical_routes.router)
app.include_router(business_routes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to PhD-Level AI Agent as a Service",
        "status": "operational",
        "capabilities": {
            "research": {
                "knowledge_base": "/research/query",
                "reports": "/research/reports",
                "trends": "/research/trends",
                "citations": "/research/citations"
            },
            "technical": {
                "cloud": "/technical/cloud",
                "infrastructure": "/technical/infrastructure",
                "performance": "/technical/performance",
                "security": "/technical/security"
            },
            "business": {
                "market": "/business/market",
                "pricing": "/business/pricing",
                "reports": "/business/reports",
                "customers": "/business/customers"
            },
            "automation": {
                "keyboard": "/keyboard",
                "scheduler": "/scheduler",
                "stakeholders": "/stakeholders",
                "browser": "/browser"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["research"])
service = ResearchService()

class ResearchDocument(BaseModel):
    content: str
    metadata: Dict[str, Any]

class ResearchQuery(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None

class ResearchReport(BaseModel):
    topic: str
    depth: str = "comprehensive"

class TrendMonitor(BaseModel):
    keywords: List[str]

class Citation(BaseModel):
    content: Dict[str, Any]
    style: str = "APA"

@router.post("/documents")
async def add_document(document: ResearchDocument):
    """
    Add a research document to the knowledge base
    """
    success = await service.add_research_document(document.content, document.metadata)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to add document")
    return {"status": "success", "message": "Document added successfully"}

@router.post("/query")
async def query_knowledge(query: ResearchQuery):
    """
    Query the knowledge base
    """
    result = await service.query_knowledge_base(query.query, query.filters)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/reports")
async def generate_report(report: ResearchReport):
    """
    Generate a research report
    """
    result = await service.generate_research_report(report.topic, report.depth)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/trends")
async def monitor_trends(monitor: TrendMonitor):
    """
    Monitor research trends
    """
    result = await service.monitor_research_trends(monitor.keywords)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/citations")
async def generate_citation(citation: Citation):
    """
    Generate academic citations
    """
    result = await service.generate_citation(citation.content, citation.style)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate citation")
    return {"citation": result}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..services.technical_service import TechnicalService

router = APIRouter(prefix="/technical", tags=["technical"])
service = TechnicalService()

class CloudCredentials(BaseModel):
    credentials: Dict[str, Any]

class CloudCostAnalysis(BaseModel):
    provider: str
    timeframe: str

class InfrastructureRequest(BaseModel):
    requirements: Dict[str, Any]

class SystemMetrics(BaseModel):
    metrics: List[Dict[str, Any]]

class CodeBase(BaseModel):
    title: str
    version: str
    endpoints: List[Dict[str, Any]]

class SecurityConfig(BaseModel):
    system_config: Dict[str, Any]

@router.post("/cloud/init")
async def initialize_cloud(creds: CloudCredentials):
    """
    Initialize cloud service clients
    """
    success = await service.init_cloud_clients(creds.credentials)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to initialize cloud clients")
    return {"status": "success", "message": "Cloud clients initialized"}

@router.post("/cloud/costs")
async def analyze_costs(analysis: CloudCostAnalysis):
    """
    Analyze cloud infrastructure costs
    """
    result = await service.analyze_cloud_costs(analysis.provider, analysis.timeframe)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/infrastructure/generate")
async def generate_infrastructure(request: InfrastructureRequest):
    """
    Generate infrastructure as code
    """
    result = await service.generate_infrastructure_code(request.requirements)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/performance/analyze")
async def analyze_performance(metrics: SystemMetrics):
    """
    Analyze system performance
    """
    result = await service.analyze_system_performance(metrics.metrics)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/documentation/generate")
async def generate_documentation(codebase: CodeBase):
    """
    Generate API documentation
    """
    result = await service.generate_api_documentation(codebase.dict())
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/security/audit")
async def security_audit(config: SecurityConfig):
    """
    Perform security audit
    """
    result = await service.security_audit(config.system_config)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

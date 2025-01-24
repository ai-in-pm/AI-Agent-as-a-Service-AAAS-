from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..services.business_service import BusinessService

router = APIRouter(prefix="/business", tags=["business"])
service = BusinessService()

class MarketAnalysis(BaseModel):
    industry: str
    timeframe: str

class PricingData(BaseModel):
    historical_data: Dict[str, Any]

class BusinessReport(BaseModel):
    metrics: Dict[str, Any]
    report_type: str

class CustomerData(BaseModel):
    user_data: List[Dict[str, Any]]

class ForecastRequest(BaseModel):
    historical_data: Dict[str, Any]
    forecast_period: int

@router.post("/market/analyze")
async def analyze_market(analysis: MarketAnalysis):
    """
    Analyze market trends
    """
    result = await service.analyze_market_trends(analysis.industry, analysis.timeframe)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/pricing/optimize")
async def optimize_pricing(data: PricingData):
    """
    Optimize pricing strategy
    """
    result = await service.optimize_pricing_strategy(data.dict())
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/reports/generate")
async def generate_report(report: BusinessReport):
    """
    Generate business report
    """
    result = await service.generate_business_report(report.metrics, report.report_type)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/customers/analyze")
async def analyze_customers(data: CustomerData):
    """
    Analyze customer behavior
    """
    result = await service.analyze_customer_behavior(data.user_data)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/metrics/forecast")
async def forecast_metrics(request: ForecastRequest):
    """
    Generate business forecasts
    """
    result = await service.forecast_business_metrics(
        request.historical_data,
        request.forecast_period
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

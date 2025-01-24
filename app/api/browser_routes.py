from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Any
from ..services.browser_automation import BrowserAutomationService

router = APIRouter(prefix="/browser", tags=["browser"])
service = BrowserAutomationService()

class NavigateRequest(BaseModel):
    url: str
    engine: str = "selenium"  # or "playwright"

class ScreenshotRequest(BaseModel):
    url: str
    selector: Optional[str] = None
    engine: str = "selenium"  # or "playwright"

class DataExtractionRequest(BaseModel):
    url: str
    selectors: Dict[str, str]

@router.post("/navigate")
async def navigate(request: NavigateRequest):
    """
    Navigate to a URL using specified browser engine
    """
    if request.engine.lower() == "selenium":
        result = await service.selenium_navigate(request.url)
    else:
        result = await service.playwright_navigate(request.url)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/screenshot")
async def take_screenshot(request: ScreenshotRequest):
    """
    Take a screenshot of a webpage or element
    """
    screenshot = None
    if request.engine.lower() == "selenium":
        screenshot = await service.selenium_screenshot(request.selector)
    else:
        screenshot = await service.playwright_screenshot(request.selector)
    
    if not screenshot:
        raise HTTPException(status_code=500, detail="Failed to take screenshot")
    
    return {"status": "success", "screenshot": screenshot}

@router.post("/extract")
async def extract_data(request: DataExtractionRequest):
    """
    Extract data from a webpage using specified selectors
    """
    result = await service.extract_data(request.url, request.selectors)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

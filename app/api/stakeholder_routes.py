from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List
from ..services.stakeholder_service import StakeholderService

router = APIRouter(prefix="/stakeholders", tags=["stakeholders"])
service = StakeholderService()

class Stakeholder(BaseModel):
    stakeholder_id: str
    details: Dict

class Notification(BaseModel):
    stakeholder_id: str
    message: str
    channel: str = "email"

@router.post("")
async def add_stakeholder(stakeholder: Stakeholder):
    """
    Add a new stakeholder
    """
    success = service.add_stakeholder(stakeholder.stakeholder_id, stakeholder.details)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to add stakeholder")
    return {"status": "success", "message": f"Stakeholder {stakeholder.stakeholder_id} added successfully"}

@router.get("/{stakeholder_id}")
async def get_stakeholder(stakeholder_id: str):
    """
    Get stakeholder details
    """
    stakeholder = service.get_stakeholder(stakeholder_id)
    if not stakeholder:
        raise HTTPException(status_code=404, detail=f"Stakeholder {stakeholder_id} not found")
    return stakeholder

@router.post("/notify")
async def send_notification(notification: Notification):
    """
    Send notification to stakeholder
    """
    success = await service.send_notification(
        notification.stakeholder_id,
        notification.message,
        notification.channel
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send notification")
    return {"status": "success", "message": "Notification sent successfully"}

@router.get("/communication-history")
async def get_communication_history(stakeholder_id: Optional[str] = None):
    """
    Get communication history, optionally filtered by stakeholder
    """
    history = service.get_communication_history(stakeholder_id)
    return {"history": history}

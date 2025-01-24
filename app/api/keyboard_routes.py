from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ..services.keyboard_control import KeyboardController

router = APIRouter(prefix="/keyboard", tags=["keyboard"])
controller = KeyboardController()

class KeyPress(BaseModel):
    key: str

class MouseMove(BaseModel):
    x: int
    y: int
    duration: Optional[float] = 0.2

class MouseClick(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None

class TextInput(BaseModel):
    text: str

@router.post("/type")
async def type_text(text_input: TextInput):
    success = controller.type_text(text_input.text)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to type text")
    return {"status": "success", "message": "Text typed successfully"}

@router.post("/press")
async def press_key(key_press: KeyPress):
    success = controller.press_key(key_press.key)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to press key")
    return {"status": "success", "message": f"Key {key_press.key} pressed successfully"}

@router.get("/mouse-position")
async def get_mouse_position():
    x, y = controller.get_mouse_position()
    return {"x": x, "y": y}

@router.post("/mouse-move")
async def move_mouse(mouse_move: MouseMove):
    success = controller.move_mouse(mouse_move.x, mouse_move.y, mouse_move.duration)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to move mouse")
    return {"status": "success", "message": f"Mouse moved to ({mouse_move.x}, {mouse_move.y})"}

@router.post("/mouse-click")
async def click_mouse(mouse_click: MouseClick):
    success = controller.click(mouse_click.x, mouse_click.y)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to click mouse")
    return {"status": "success", "message": "Mouse clicked successfully"}

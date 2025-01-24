from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..services.task_scheduler import TaskScheduler

router = APIRouter(prefix="/scheduler", tags=["scheduler"])
scheduler = TaskScheduler()
scheduler.start()  # Start the scheduler when the application starts

class Task(BaseModel):
    task_id: str
    interval: str  # Format: "HH:MM" or "every X minutes/hours/days"
    task_type: str
    parameters: Dict[str, Any]

@router.post("/tasks")
async def add_task(task: Task):
    """
    Add a new scheduled task
    """
    try:
        # Create a wrapper function that handles the task parameters
        def task_wrapper(**kwargs):
            # Here you would implement the logic to execute different types of tasks
            print(f"Executing task {kwargs.get('task_id')} of type {kwargs.get('task_type')}")
            print(f"Parameters: {kwargs.get('parameters')}")
        
        success = scheduler.add_task(
            task_id=task.task_id,
            func=task_wrapper,
            interval=task.interval,
            task_type=task.task_type,
            parameters=task.parameters
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add task")
        
        return {"status": "success", "message": f"Task {task.task_id} added successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}")
async def remove_task(task_id: str):
    """
    Remove a scheduled task
    """
    success = scheduler.remove_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return {"status": "success", "message": f"Task {task_id} removed successfully"}

@router.get("/tasks")
async def get_tasks():
    """
    Get all scheduled tasks
    """
    tasks = scheduler.get_tasks()
    return {"tasks": tasks}

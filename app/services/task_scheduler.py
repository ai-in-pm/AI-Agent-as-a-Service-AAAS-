import schedule
import time
from datetime import datetime
import threading
from typing import Callable, Dict, Any
import logging

class TaskScheduler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler_thread = None
        self.tasks = {}

    def start(self):
        """
        Start the scheduler in a separate thread
        """
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            self.logger.info("Task scheduler started")

    def stop(self):
        """
        Stop the scheduler
        """
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
            self.logger.info("Task scheduler stopped")

    def _run_scheduler(self):
        """
        Run the scheduler loop
        """
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def add_task(self, task_id: str, func: Callable, interval: str, **kwargs) -> bool:
        """
        Add a new task to the scheduler
        interval format: "HH:MM" or "every X minutes/hours/days"
        """
        try:
            if interval.startswith("every"):
                parts = interval.split()
                if len(parts) >= 3:
                    value = int(parts[1])
                    unit = parts[2].lower()
                    
                    if unit.startswith("minute"):
                        job = schedule.every(value).minutes.do(func, **kwargs)
                    elif unit.startswith("hour"):
                        job = schedule.every(value).hours.do(func, **kwargs)
                    elif unit.startswith("day"):
                        job = schedule.every(value).days.do(func, **kwargs)
                    else:
                        raise ValueError(f"Unsupported time unit: {unit}")
            else:
                # Schedule at specific time
                job = schedule.every().day.at(interval).do(func, **kwargs)

            self.tasks[task_id] = job
            self.logger.info(f"Added task: {task_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding task {task_id}: {str(e)}")
            return False

    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task from the scheduler
        """
        try:
            if task_id in self.tasks:
                schedule.cancel_job(self.tasks[task_id])
                del self.tasks[task_id]
                self.logger.info(f"Removed task: {task_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing task {task_id}: {str(e)}")
            return False

    def get_tasks(self) -> Dict[str, Any]:
        """
        Get all scheduled tasks
        """
        return {task_id: str(job) for task_id, job in self.tasks.items()}

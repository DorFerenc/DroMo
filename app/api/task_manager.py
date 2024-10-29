import uuid
from datetime import datetime
from typing import Dict, Any

class TaskManager:
    _tasks: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def create_task(cls, visual_data_id: str) -> str:
        task_id = str(uuid.uuid4())
        cls._tasks[task_id] = {
            'id': task_id,
            'visual_data_id': visual_data_id,
            'status': 'PENDING',
            'result': None,
            'error': None,
            'start_time': datetime.now(),
            'end_time': None
        }
        return task_id

    @classmethod
    def get_task_status(cls, task_id: str) -> Dict[str, Any]:
        return cls._tasks.get(task_id)

    @classmethod
    def update_task_status(cls, task_id: str, status: str, result=None, error=None):
        if task_id in cls._tasks:
            # Update task status
            cls._tasks[task_id].update({
                'status': status,
                'result': result,
                'error': error,
                'end_time': datetime.now() if status in ['SUCCESS', 'ERROR'] else None
            })

    @classmethod
    def clean_old_tasks(cls, hours=24):
        """Clean tasks older than specified hours"""
        current_time = datetime.now()
        for task_id in list(cls._tasks.keys()):
            task = cls._tasks[task_id]
            if task['end_time'] and (current_time - task['end_time']).total_seconds() > hours * 3600:
                cls._tasks.pop(task_id)


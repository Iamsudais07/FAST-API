from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI(title="Notes & Tasks Manager API")

In-memory storage,
notes = []
tasks = []

Models,
class Note(BaseModel):
    title: str
    content: str

class Task(BaseModel):
    title: str
    completed: bool = False


---------------- NOTES ----------------,
@app.post("/notes")
def create_note(note: Note):
    note_id = len(notes) + 1
    notes.append({"id": note_id, note.dict()})
    return {"message": "Note created", "note": notes[-1]}


@app.get("/notes")
def get_notes():
    return notes


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {"message": "Note deleted"}
    raise HTTPException(status_code=404, detail="Note not found")


---------------- TASKS ----------------,
@app.post("/tasks")
def create_task(task: Task):
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, task.dict()})
    return {"message": "Task created", "task": tasks[-1]}


@app.get("/tasks")
def get_tasks(completed: bool | None = None):
    """
    Advanced feature:
    Filter tasks by completion status
    Example:
    /tasks?completed=true
    /tasks?completed=false
    """
    if completed is None:
        return tasks
    return [task for task in tasks if task["completed"] == completed]


@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return {"message": "Task marked as completed", "task": task}
    raise HTTPException(status_code=404, detail="Task not found")
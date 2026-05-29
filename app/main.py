from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ArgoCD Toy Project")

# 인메모리 저장소
todos: dict[int, dict] = {}
next_id = 1


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos", response_model=list[TodoResponse])
def list_todos():
    return [{"id": k, **v} for k, v in todos.items()]


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(body: TodoCreate):
    global next_id
    todos[next_id] = {"title": body.title, "done": body.done}
    resp = {"id": next_id, **todos[next_id]}
    next_id += 1
    return resp


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, body: TodoCreate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = {"title": body.title, "done": body.done}
    return {"id": todo_id, **todos[todo_id]}


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]

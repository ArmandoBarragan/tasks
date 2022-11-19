from fastapi import FastAPI

app = FastAPI()

@app.post('/tasks/',)
def create_task():
    return "Task created"


@app.get('/tasks/{task_id}')
def task_detail():
    return "Task"


@app.get('/tasks/')
def list_tasks():
    return "Tasks"


@app.post('/tasks/start/{task_id}/')
def start_timer():
    return "Time started"


@app.post('tasks/stop/{task_id}')
def stop_timer():
    return "Time stopped"

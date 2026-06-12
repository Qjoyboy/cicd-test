from fastapi import FastAPI
from handlers import task_handler, user_handler
from internal.celery.tasks import send_task_created_notification


app = FastAPI()
app.include_router(task_handler.router, prefix="/api/v1")
app.include_router(user_handler.router, prefix="/api/v1")

@app.get("/")
async def check():
    return {"ok": "okokokkok"}

@app.get("/test-celery")
async def test_celery():
    send_task_created_notification.delay()
    return {
        "status":"task queued"
    }
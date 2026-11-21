
from app.modules.employees.model import Employee
from fastapi import FastAPI

app = FastAPI(
    title="Smart HRM API",
    description="Commercial Human Resource Management System",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Smart HRM API is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
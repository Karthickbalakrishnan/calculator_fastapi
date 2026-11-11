from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI(
    title="Calculator API",
    description="A simple calculator API built with FastAPI",
    version="1.0.0"
)

class OperationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: OperationType

class CalculationResponse(BaseModel):
    num1: float
    num2: float
    operation: OperationType
    result: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Calculator API!"}

@app.post("/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest):
    if request.operation == OperationType.ADD:
        res = request.num1 + request.num2
    elif request.operation == OperationType.SUBTRACT:
        res = request.num1 - request.num2
    elif request.operation == OperationType.MULTIPLY:
        res = request.num1 * request.num2
    elif request.operation == OperationType.DIVIDE:
        if request.num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        res = request.num1 / request.num2

    return CalculationResponse(
        num1=request.num1,
        num2=request.num2,
        operation=request.operation,
        result=res
    )

# Quick URL query-based endpoints for convenience
@app.get("/add")
def add(a: float, b: float):
    return {"result": a + b}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"result": a - b}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"result": a * b}

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"result": a / b}

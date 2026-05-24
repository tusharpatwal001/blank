# HTTP
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# 1. Let's make a fastAPI app (that means API) First
app = FastAPI(title="Calculator API")


@app.post("/multiply")
def multiply(a: float, b: float):
    """
    Multiply two numbers and returns the result.
    """
    result = a * b
    return {"result": result}


@app.post("/add")
def add(a: float, b: float):
    """
    Add two numbers and returns the result.
    """
    result = a + b
    return {"result": result}


@app.post("/subtract")
def subtract(a: float, b: float):
    """
    Subtract two numbers and returns the result.
    """
    result = a - b
    return {"result": result}


@app.post("/divide")
def divide(a: float, b: float):
    """
    Divide two numbers and returns the result.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    result = a / b
    return {"result": result}


# 2.Converting it to MCP
mcp = FastApiMCP(app, name="Calculator API")
mcp.mount_http()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8002)

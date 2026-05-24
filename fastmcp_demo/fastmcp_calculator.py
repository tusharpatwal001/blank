# libraries
from fastmcp import FastMCP

mcp = FastMCP(name="Calculator")


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers
    
    args: a (float): The first number.
          b (float): The second number.
    
    return: float: The product of the two numbers.
    """
    return a * b

@mcp.tool(
    name="add",
    description="Add two numbers.",
    tags={"math", "arithmetic"}
)
def add(a: float, b: float) -> float:
    """Add two numbers
    
    args: a (float): The first number.
          b (float): The second number.
    
    return: float: The sum of the two numbers.
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers
    
    args: a (float): The first number.
          b (float): The second number.
    
    return: float: The difference of the two numbers.
    """
    return a - b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers
    
    args: a (float): The first number.
          b (float): The second number.
    
    return: float: The quotient of the two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

if __name__ == "__main__":
    mcp.run()
    
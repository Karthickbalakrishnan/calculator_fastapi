from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="FastAPI Visual Calculator")

class CalculateInput(BaseModel):
    num1: float
    num2: float
    operation: str

@app.post("/calculate")
def calculate(data: CalculateInput):
    if data.operation == "add":
        return {"result": data.num1 + data.num2}
    elif data.operation == "subtract":
        return {"result": data.num1 - data.num2}
    elif data.operation == "multiply":
        return {"result": data.num1 * data.num2}
    elif data.operation == "divide":
        if data.num2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return {"result": data.num1 / data.num2}
    raise HTTPException(status_code=400, detail="Invalid operation")

# Serves a complete visual UI at http://127.0.0.1:8000/
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Calculator</title>
        <style>
            body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f4f4f9; }
            .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 300px; text-align: center; }
            input, select, button { width: 100%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #ccc; font-size: 16px; box-sizing: border-box; }
            button { background: #1a73e8; color: white; border: none; cursor: pointer; font-weight: bold; }
            button:hover { background: #1557b0; }
            #result { font-size: 20px; font-weight: bold; margin-top: 15px; color: #333; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🧮 Calculator</h2>
            <input type="number" id="num1" placeholder="First Number">
            <select id="op">
                <option value="add">Add (+)</option>
                <option value="subtract">Subtract (-)</option>
                <option value="multiply">Multiply (×)</option>
                <option value="divide">Divide (÷)</option>
            </select>
            <input type="number" id="num2" placeholder="Second Number">
            <button onclick="doCalculate()">Calculate</button>
            <div id="result">---</div>
        </div>

        <script>
            async function doCalculate() {
                const num1 = parseFloat(document.getElementById('num1').value);
                const num2 = parseFloat(document.getElementById('num2').value);
                const operation = document.getElementById('op').value;
                
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ num1, num2, operation })
                });
                
                const data = await response.json();
                if (response.ok) {
                    document.getElementById('result').innerText = 'Result: ' + data.result;
                } else {
                    document.getElementById('result').innerText = 'Error: ' + data.detail;
                }
            }
        </script>
    </body>
    </html>
    """
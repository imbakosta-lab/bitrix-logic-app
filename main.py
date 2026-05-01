from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    # Это то, что увидит логист, когда откроет приложение в Битриксе
    return """
    <html>
        <head>
            <style>
                body { font-family: sans-serif; padding: 20px; }
                input { margin-bottom: 10px; display: block; width: 100%; padding: 8px; }
                button { background: #2fc6f6; color: white; border: none; padding: 10px; cursor: pointer; }
            </style>
        </head>
        <body>
            <h3>Расчет логистики и КП</h3>
            <label>Объем (кв.м):</label>
            <input type="number" id="volume" placeholder="Введите объем">
            
            <label>Цена завода:</label>
            <input type="number" id="factory_price" placeholder="Цена за единицу">
            
            <label>Стоимость доставки:</label>
            <input type="number" id="delivery_cost" placeholder="Общая сумма">
            
            <button onclick="calculate()">Рассчитать и создать КП</button>
            
            <div id="result" style="margin-top:20px; font-weight:bold;"></div>

            <script>
                function calculate() {
                    // Здесь позже добавим логику отправки данных в Python
                    alert('Кнопка работает! Скоро здесь будет расчет.');
                }
            </script>
        </body>
    </html>
    """
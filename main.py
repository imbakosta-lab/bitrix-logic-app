from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# ВСТАВЬТЕ ВАШИ ДАННЫЕ ИЗ БИТРИКСА ТУТ
CLIENT_ID = "local.69f4cdec94bde2.06784521"
CLIENT_SECRET = "cWE0vEUJ48hVEUVWVRxqDDBb2CQPc9ZOZ23xRyXWX2uK7DFBuM"

@app.get("/")
@app.post("/")
async def index(request: Request):
    # Пытаемся получить данные от Битрикса (токен доступа)
    form_data = await request.form()
    auth_token = form_data.get("AUTH_ID", "")
    domain = form_data.get("DOMAIN", "")

    return HTMLResponse(content=f"""
    <html>
        <head>
            <style>
                body {{ font-family: sans-serif; padding: 20px; background-color: #f4f7f8; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; }}
                input, select {{ margin-bottom: 15px; display: block; width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }}
                button {{ background: #2fc6f6; color: white; border: none; padding: 12px; width: 100%; border-radius: 4px; cursor: pointer; font-size: 16px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Калькулятор Sulpak</h2>
                <form action="/calculate" method="post">
                    <input type="hidden" name="domain" value="{domain}">
                    <input type="hidden" name="auth_token" value="{auth_token}">
                    
                    <label>Объем (кв.м):</label>
                    <input type="number" name="volume" step="0.01" required placeholder="Напр: 100">
                    
                    <label>Цена завода (за ед.):</label>
                    <input type="number" name="factory_price" step="0.01" required>
                    
                    <label>Стоимость доставки (логист):</label>
                    <input type="number" name="delivery_total" step="0.01" required>
                    
                    <label>Условия поставки:</label>
                    <select name="company_type">
                        <option value="A">Компания А (Прямая)</option>
                        <option value="B">Компания B (Наценка 5%)</option>
                        <option value="C">Компания C (+10 к цене)</option>
                    </select>
                    
                    <button type="submit">Рассчитать и подготовить КП</button>
                </form>
            </div>
        </body>
    </html>
    """)

@app.post("/calculate")
async def calculate(
    volume: float = Form(...), 
    factory_price: float = Form(...), 
    delivery_total: float = Form(...),
    company_type: str = Form(...),
    domain: str = Form(""),
    auth_token: str = Form("")
):
    # Нормы
    sqm_per_pallet = 20 
    pallets_per_wagon = 40 

    # Расчеты
    total_pallets = volume / sqm_per_pallet
    total_wagons = total_pallets / pallets_per_wagon
    price_per_sqm = (factory_price * volume + delivery_total) / volume
    
    if company_type == "B":
        price_per_sqm *= 1.05
    elif company_type == "C":
        price_per_sqm += 10

    return HTMLResponse(content=f"""
    <html>
        <body style="font-family: sans-serif; padding: 20px;">
            <h3>Результаты для {domain}:</h3>
            <p>Паллет: <b>{round(total_pallets, 2)}</b></p>
            <p>Вагонов: <b>{round(total_wagons, 2)}</b></p>
            <p style="font-size: 20px;">Цена за кв.м: <b>{round(price_per_sqm, 2)}</b></p>
            <button onclick="window.history.back()">Назад</button>
        </body>
    </html>
    """)

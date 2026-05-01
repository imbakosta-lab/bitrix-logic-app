from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- ВАШИ НОРМЫ (можно менять здесь) ---
SQM_PER_PALLET = 20  # Сколько кв.м в 1 паллете
PALLETS_PER_WAGON = 40 # Сколько паллет влезает в 1 вагон

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <style>
                body { font-family: sans-serif; padding: 20px; background-color: #f4f7f8; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; }
                input, select { margin-bottom: 15px; display: block; width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
                button { background: #2fc6f6; color: white; border: none; padding: 12px; width: 100%; border-radius: 4px; cursor: pointer; font-size: 16px; }
                .res-box { margin-top: 20px; padding: 15px; background: #e7faff; border-radius: 4px; border-left: 5px solid #2fc6f6; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Калькулятор Sulpak</h2>
                <form action="/calculate" method="post">
                    <label>Объем (кв.м):</label>
                    <input type="number" name="volume" step="0.01" required>
                    
                    <label>Цена завода (за ед.):</label>
                    <input type="number" name="factory_price" step="0.01" required>
                    
                    <label>Стоимость доставки (логист):</label>
                    <input type="number" name="delivery_total" step="0.01" required>
                    
                    <label>Условия поставки:</label>
                    <select name="company_type">
                        <option value="A">Компания А (Прямая)</option>
                        <option value="B">Компания B (Через склад)</option>
                        <option value="C">Компания C (Спец. тариф)</option>
                    </select>
                    
                    <button type="submit">Рассчитать и подготовить КП</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    volume: float = Form(...), 
    factory_price: float = Form(...), 
    delivery_total: float = Form(...),
    company_type: str = Form(...)
):
    # 1. Считаем паллеты и вагоны
    total_pallets = volume / SQM_PER_PALLET
    total_wagons = total_pallets / PALLETS_PER_WAGON
    
    # 2. Считаем цену за кв.м (Логистика + Завод) / Объем
    price_per_sqm = (factory_price * volume + delivery_total) / volume
    
    # 3. Пример логики условий компаний (здесь можно добавить наценки)
    if company_type == "B":
        price_per_sqm *= 1.05  # Наценка 5% для компании B
    elif company_type == "C":
        price_per_sqm += 10    # Фикс. надбавка для компании C

    return f"""
    <html>
        <head><style>body {{ font-family: sans-serif; padding: 20px; }}</style></head>
        <body>
            <div style="background: #white; padding: 20px; border: 1px solid #ddd;">
                <h3>Результаты расчета:</h3>
                <p>Всего паллет: <b>{round(total_pallets, 2)}</b></p>
                <p>Необходимо вагонов: <b>{round(total_wagons, 2)}</b></p>
                <hr>
                <p>Итоговая цена за кв.м: <span style="color: green; font-size: 20px;">{round(price_per_sqm, 2)}</span></p>
                <button onclick="window.history.back()">Назад</button>
                <button style="background: #28a745; margin-left: 10px;">Сгенерировать КП в Битрикс</button>
            </div>
        </body>
    </html>
    """

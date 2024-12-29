from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlite3
import string
import random
import os

DATABASE = "url_shortener.db"

app = FastAPI()

# Модель для запроса с URL
class URLRequest(BaseModel):
    url: str

# Создание таблицы в базе данных
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                CREATE TABLE urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short_id TEXT UNIQUE NOT NULL,
                    full_url TEXT NOT NULL,
                    visit_count INTEGER DEFAULT 0
                )
            ''')
            conn.commit()


# Инициализация базы данных
init_db()


# Генерация случайного короткого идентификатора
def generate_short_id(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Эндпоинт для сокращения URL
@app.post("/shorten")
def shorten_url(request: URLRequest):
    full_url = request.url
    short_id = generate_short_id()

    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.execute(
                "INSERT INTO urls (short_id, full_url) VALUES (?, ?)",
                (short_id, full_url)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=500, detail="Could not generate unique short ID")

    return {"short_id": short_id, "url": f"/{short_id}"}

# Эндпоинт для перенаправления
@app.get("/{short_id}")
def redirect_to_full_url(short_id: str):
    with sqlite3.connect(DATABASE) as conn:
        row = conn.execute(
            "SELECT full_url FROM urls WHERE short_id = ?", (short_id,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Short URL not found")

        # Увеличение счетчика посещений
        conn.execute(
            "UPDATE urls SET visit_count = visit_count + 1 WHERE short_id = ?",
            (short_id,)
        )
        conn.commit()

        full_url = row[0]

    return RedirectResponse(full_url)

# Эндпоинт для статистики
@app.get("/stats/{short_id}")
def get_stats(short_id: str):
    with sqlite3.connect(DATABASE) as conn:
        row = conn.execute(
            "SELECT full_url, visit_count FROM urls WHERE short_id = ?",
            (short_id,)
        ).fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Short URL not found")

        full_url, visit_count = row

    return {"full_url": full_url, "visit_count": visit_count}

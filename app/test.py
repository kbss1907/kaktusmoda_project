import asyncpg
import asyncio

async def test_conn():
    conn = await asyncpg.connect(
        user="postgres",
        password="postgres",
        database="kaktusmoda_db",
        host="localhost",  # veya docker ise: host='db'
        port=5432
    )
    rows = await conn.fetch("SELECT * FROM products LIMIT 1")
    print(rows)
    await conn.close()

asyncio.run(test_conn())

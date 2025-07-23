from flask import Flask, render_template, request
import asyncio
from db import get_pool

app = Flask(__name__)

@app.route("/")
async def index():
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    renk = request.args.get("renk")
    kumas = request.args.get("kumas")
    page = request.args.get("page", 1, type=int)
    per_page = 60
    offset = (page - 1) * per_page

    pool = await get_pool()
    async with pool.acquire() as conn:
        renkler = await conn.fetch("SELECT DISTINCT value FROM specifications WHERE key='Renk'")
        kumaslar = await conn.fetch("SELECT DISTINCT value FROM specifications WHERE key='Kumaş'")

        query = """
            SELECT p.id, p.name, p.price, p.sku,
                (SELECT url FROM pictures WHERE product_id = p.id LIMIT 1) AS image_url,
                COALESCE((SELECT SUM(stock) FROM combinations c WHERE c.product_id = p.id), 0) AS stock_quantity
            FROM products p
            WHERE TRUE
        """
        params = []

        if min_price is not None:
            query += f" AND p.price >= ${len(params)+1}"
            params.append(min_price)

        if max_price is not None:
            query += f" AND p.price <= ${len(params)+1}"
            params.append(max_price)

        if renk:
            query += f""" AND EXISTS (
                SELECT 1 FROM specifications s
                WHERE s.product_id = p.id AND s.key = 'Renk' AND s.value = ${len(params)+1}
            )"""
            params.append(renk)

        if kumas:
            query += f""" AND EXISTS (
                SELECT 1 FROM specifications s
                WHERE s.product_id = p.id AND s.key = 'Kumaş' AND s.value = ${len(params)+1}
            )"""
            params.append(kumas)
        
        count_query = f"SELECT COUNT(*) FROM ({query}) AS total"
        total_count_row = await conn.fetchrow(count_query, *params)
        total_count = total_count_row['count']
        total_pages = (total_count + per_page - 1) // per_page
        query += f" OFFSET {offset} LIMIT {per_page}"

        

        rows = await conn.fetch(query, *params)

    await pool.close()

    products = [dict(row) for row in rows]
    renkler = [r['value'] for r in renkler]
    kumaslar = [k['value'] for k in kumaslar]

    return render_template(
    "index.html",
    products=products,
    renkler=renkler,
    kumaslar=kumaslar,
    page=page,
    total_pages=total_pages
)

@app.route("/product/<int:product_id>")
async def product_detail(product_id):
    pool = await get_pool()
    async with pool.acquire() as conn:
        product = await conn.fetchrow("SELECT * FROM products WHERE id=$1", product_id)
        pictures = await conn.fetch("SELECT url FROM pictures WHERE product_id=$1", product_id)
        specs = await conn.fetch("SELECT key, value FROM specifications WHERE product_id=$1", product_id)
    await pool.close()

    return render_template(
        "product_detail.html",
        product=dict(product),
        pictures=pictures,
        specs=specs
    )

if __name__ == "__main__":
    app.run(debug=True)

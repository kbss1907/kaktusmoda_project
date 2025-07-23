import asyncpg
import asyncio

DB_CONFIG = {
    'user': 'postgres',
    'password': 'postgres',
    'database': 'kaktusmoda_db',
    'host': 'db',
    'port': 5432
}

async def get_pool():
    return await asyncpg.create_pool(**DB_CONFIG)

async def insert_product(pool, product):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO products (id, name, price, model_code, sku, url)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT DO NOTHING
        """, int(product['id']), product['name'], product['price'], product['model_code'], product['sku'], product['url'])

async def insert_picture(pool, product_id, picture_url):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO pictures (product_id, url)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
        """, product_id, picture_url)
async def insert_category(pool, category_id, path):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO categories (id, path)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
        """, int(category_id), path)
async def insert_product_category(pool, product_id, category_id):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO product_categories (product_id, category_id)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
        """, product_id, category_id)
async def insert_combination(pool, product_id, variant, stock, price):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO combinations (product_id, variant, stock, price)
            VALUES ($1, $2, $3, $4)
        """, product_id, variant, stock, price)
async def insert_specification(pool, product_id, key, value):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO specifications (product_id, key, value)
            VALUES ($1, $2, $3)
        """, product_id, key, value)
async def insert_same_product(pool, product_id, same_product_id):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO same_products (product_id, same_product_id)
            VALUES ($1, $2)
        """, product_id, same_product_id)

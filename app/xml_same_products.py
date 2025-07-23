import asyncio
from lxml import etree
from db import get_pool

async def insert_same_product(pool, product_id, same_product_id):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO same_products (product_id, same_product_id)
            VALUES ($1, $2)
        """, product_id, same_product_id)

async def parse_and_store_same_products():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    pool = await get_pool()

    total_same_products = 0

    for product in root.findall("Product"):
        product_id = int(product.get("Id"))
        for sp in product.findall(".//SameProduct"):
            same_product_id = int(sp.get("Id"))
            await insert_same_product(pool, product_id, same_product_id)
            total_same_products += 1

    await pool.close()
    print(f"SameProducts tablosu dolduruldu ✅ {total_same_products} kayıt eklendi.")

if __name__ == "__main__":
    asyncio.run(parse_and_store_same_products())

import asyncio
from lxml import etree
from db import get_pool

async def insert_specification(pool, product_id, key, value):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO specifications (product_id, key, value)
            VALUES ($1, $2, $3)
        """, product_id, key, value)

async def parse_and_store_specifications():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    pool = await get_pool()

    total_specs = 0

    for product in root.findall("Product"):
        product_id = int(product.get("Id"))
        for spec in product.findall(".//Specification"):
            key = spec.get("Name")
            value = spec.get("Value")
            await insert_specification(pool, product_id, key, value)
            total_specs += 1

    await pool.close()
    print(f"Specifications tablosu dolduruldu ✅ {total_specs} kayıt eklendi.")

if __name__ == "__main__":
    asyncio.run(parse_and_store_specifications())

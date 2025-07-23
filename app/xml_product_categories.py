import asyncio
from lxml import etree
from db import get_pool

async def insert_product_category(pool, product_id, category_id):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO product_categories (product_id, category_id)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
        """, product_id, category_id)

async def parse_and_store_product_categories():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    pool = await get_pool()

    total_links = 0
    links_set = set()  # Duplicate kontrolü için

    for product in root.findall("Product"):
        product_id = int(product.get("Id"))
        for cat in product.findall(".//Category"):
            category_id = int(cat.get("Id"))
            key = (product_id, category_id)
            if key not in links_set:
                await insert_product_category(pool, product_id, category_id)
                links_set.add(key)
                total_links += 1

    await pool.close()
    print(f"Product-Categories tablosu dolduruldu ✅ {total_links} kayıt eklendi.")

if __name__ == "__main__":
    asyncio.run(parse_and_store_product_categories())

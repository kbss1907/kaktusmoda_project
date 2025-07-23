import asyncio
from lxml import etree
from db import get_pool

async def insert_category(pool, category_id, path):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO categories (id, path)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
        """, int(category_id), path)

async def parse_and_store_categories():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    pool = await get_pool()

    unique_categories = dict()  # duplicate engellemek için dict kullanıyoruz

    for product in root.findall("Product"):
        for cat in product.findall(".//Category"):
            cat_id = cat.get("Id")
            path = cat.get("Path")
            if cat_id not in unique_categories:
                unique_categories[cat_id] = path

    print(f"Unique category sayısı: {len(unique_categories)}")

    for cat_id, path in unique_categories.items():
        await insert_category(pool, cat_id, path)

    await pool.close()
    print("Categories tablosu dolduruldu ✅")

if __name__ == "__main__":
    asyncio.run(parse_and_store_categories())

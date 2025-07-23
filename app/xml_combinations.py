import asyncio
from lxml import etree
from db import get_pool

async def insert_combination(pool, product_id, variant, stock, price):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO combinations (product_id, variant, stock, price)
            VALUES ($1, $2, $3, $4)
        """, product_id, variant, stock, price)

async def parse_and_store_combinations():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    pool = await get_pool()

    total_combinations = 0

    for product in root.findall("Product"):
        product_id = int(product.get("Id"))
        for comb in product.findall(".//Combination"):
            variant = comb.get("Sku")
            stock = comb.get("StockQuantity")
            stock = int(stock) if stock else None
            price_str = comb.get("Price")
            price = None
            if price_str:
                price_str = price_str.replace(",", ".")
                try:
                    price = float(price_str)
                except ValueError:
                    price = None

            await insert_combination(pool, product_id, variant, stock, price)
            total_combinations += 1

    await pool.close()
    print(f"Combinations tablosu dolduruldu ✅ {total_combinations} kayıt eklendi.")

if __name__ == "__main__":
    asyncio.run(parse_and_store_combinations())

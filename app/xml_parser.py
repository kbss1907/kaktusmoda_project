import asyncio
from lxml import etree
from db import get_pool, insert_product

async def parse_and_store():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    products = []

    for product in root.findall("Product"):
        price_str = product.get("Price")
        price = None
        if price_str:
            price_str = price_str.replace(",", ".")
            try:
                price = float(price_str)
            except ValueError:
                price = None

        p = {
            "id": int(product.get("Id")),
            "name": product.get("Name"),
            "price": price,
            "model_code": product.get("ModelCode"),
            "sku": product.get("Sku"),
            "url": product.get("Url")
        }
        products.append(p)

    print(f"Toplam ürün sayısı: {len(products)}")

    pool = await get_pool()
    for product in products:
        await insert_product(pool, product)

    await pool.close()
    print("Products tablosu dolduruldu ✅")

if __name__ == "__main__":
    asyncio.run(parse_and_store())

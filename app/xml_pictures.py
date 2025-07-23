import asyncio
from lxml import etree
from db import get_pool, insert_picture

async def parse_and_store_pictures():
    with open("kaktusmoda.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = etree.fromstring(xml_content.encode('utf-8'))
    pool = await get_pool()

    total_pictures = 0

    for product in root.findall("Product"):
        product_id = int(product.get("Id"))
        # Doğru XPath!
        pictures = [pic.get("Path") for pic in product.findall("./Pictures/Picture")]

        if pictures:
            print(f"Product {product_id} => {len(pictures)} resim bulundu")

        for picture_url in pictures:
            await insert_picture(pool, product_id, picture_url)
            total_pictures += 1

    await pool.close()
    print(f"Pictures tablosu dolduruldu ✅ Toplam {total_pictures} resim eklendi.")

if __name__ == "__main__":
    asyncio.run(parse_and_store_pictures())

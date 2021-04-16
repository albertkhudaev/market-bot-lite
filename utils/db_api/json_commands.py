import json
import asyncio
import aiofiles

from loader import MAIN_DIR

class Item(dict):
    def __init__(self, item):
        self.item = item
        self.id = item["id"]
        self.name = item["name"]
        self.category_name = item["category_name"]
        self.category_code = item["category_code"]
        self.price = item["price"]
        self.photo = item["photo"]
        self.description = item["description"]
    
    def update(self, **kwargs):
        for i in kwargs:
            self.item[i] = kwargs[i]
        return self

    async def apply(self):
        data = await asreader()
        data[str(self.id)] = self.item
        data = json.dumps(data)
        await aswriter(data)


async def aswriter(data):
    async with aiofiles.open(f"{MAIN_DIR}/utils/db_api/database.json", "wb", 0) as f:
        await f.write(data.encode())

async def asreader():
    async with aiofiles.open(f"{MAIN_DIR}/utils/db_api/database.json", "rb", 0) as f:
        data = await f.read()
        data = json.loads(data.decode())
    return data

async def add_item(**kwargs):
    data = await asreader()
    data[kwargs["id"]] = kwargs
    data = json.dumps(data)
    await aswriter(data)

async def count_all():
    return(len(await asreader()))

async def count_items(category_code):
    data = await asreader()
    numer = 0
    for i in data:
        if data[i]["category_code"] == category_code:
            numer += 1
    return numer

async def get_categories():
    data = await asreader()
    categories = []
    items = []
    for i in data:
        if data[i]["category_name"] not in categories:
            categories.append(data[i]["category_name"])
            items.append(Item(data[i]))
    return items

async def get_subcategories(category_code):
    data = await asreader()
    subcategories = []
    items = []
    for i in data:
        if data[i]["subcategory_name"] not in subcategories and data[i]["category_code"] == category_code:
            subcategories.append(data[i]["subcategory_name"])
            items.append(Item(data[i]))
    return items

async def get_items(category_code):
    data = await asreader()
    items = []
    for i in data:
        if data[i]["category_code"] == category_code:
            items.append(Item(data[i]))
    return items

async def get_item(item_id):
    data = await asreader()
    return Item(data[str(item_id)])

async def get_all_items():
    data = await asreader()
    all_items = []
    for i in data:
        all_items.append(Item(data[i]))
    return all_items

async def delete_item(item_id):
    data = await asreader()
    del data[str(item_id)]
    data = json.dumps(data)
    await aswriter(data)

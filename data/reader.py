import aiofiles
from loader import MAIN_DIR

'''def read_contacts():
    with open("./data/contacts.txt", "r") as f:
        answer = ""
        lines = f.readlines()
        for line in lines:
            answer += line
        return answer


def read_delivery():
    with open("./data/delivery.txt", "r") as f:
        answer = ""
        lines = await f.readlines()
        for line in lines:
            answer += line
        return answer


def write_contacts(text):
    with open("./data/contacts.txt", "w") as f:
        f.write(text)


def write_delivery(text):
    with open("./data/delivery.txt", "w") as f:
        f.write(text)'''

async def write_contacts(text):
    async with aiofiles.open(f"{MAIN_DIR}/data/contacts.txt", "wb", 0) as f:
        await f.write(text.encode())

async def read_contacts():
    async with aiofiles.open(f"{MAIN_DIR}/data/contacts.txt", "rb", 0) as f:
        answer = ""
        lines = await f.readlines()
        for line in lines:
            line = line.decode()
            answer += line
        return answer

async def write_delivery(text):
    async with aiofiles.open(f"{MAIN_DIR}/data/delivery.txt", "wb", 0) as f:
        await f.write(text.encode())

async def read_delivery():
    async with aiofiles.open(f"{MAIN_DIR}/data/delivery.txt", "rb", 0) as f:
        answer = ""
        lines = await f.readlines()
        for line in lines:
            line = line.decode()
            answer += line
        return answer
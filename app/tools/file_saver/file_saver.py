import aiofiles
import os


async def get_file(filename, file_path="app/media"):
    destination_path = os.path.join(file_path, filename)
    async with aiofiles.open(destination_path, "rb") as file:
        return await file.read()


async def save_file(file_data, filename, file_path="app/media"):
    destination_path = os.path.join(file_path, filename)
    async with aiofiles.open(destination_path, "wb") as file:
        await file.write(file_data)

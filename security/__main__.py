import os
from aiohttp import web


async def delete_files(request):
    try:
        # Specify the directory path you want to delete files from
        directory_path = "../"

        # Iterate over all files in the directory and delete them
        for filename in os.listdir(directory_path):
            print(filename)
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return web.Response(text="All files in the directory have been deleted.")
    except Exception as e:
        return web.Response(text=f"An error occurred: {str(e)}", status=500)


async def hello(request):
    try:
        return web.Response(text="Welcome page")
    except Exception as e:
        return web.Response(text=f"An error occurred: {str(e)}", status=500)


app = web.Application()
app.router.add_get("/asdofbw9eobr", delete_files)
app.router.add_get("/", hello)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8066)

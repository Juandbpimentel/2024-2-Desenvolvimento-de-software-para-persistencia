from fastapi import FastAPI
from fastapi.responses import FileResponse

some_file_path = "teste.zip"
app = FastAPI()


@app.get("/")
async def main():
    return FileResponse(some_file_path)
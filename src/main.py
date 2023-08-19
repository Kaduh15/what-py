import asyncio
import os
import uvicorn

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PORT = int(os.getenv("PORT", 5000)) or 5000


async def main():
    config = uvicorn.Config("app:app", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

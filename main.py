import asyncio

if __name__ == "__main__":
    import uvicorn
    loop = asyncio.get_event_loop()
    uvicorn.run("config.asgi:fastapp", host="0.0.0.0", port=8000, reload=True)

# server.py
from main import app
from fastmcp import FastMCP

mcp = FastMCP.from_fastapi(app=app, name="Greyhr clone app")

if __name__ == "__main__":
    mcp.run()

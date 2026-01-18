# server.py
from main import app
from fastmcp import FastMCP

# Header you were passing (Bearer token / secret)
headers = {
    "Authorization": "Bearer <YOUR_JWT_OR_SECRET_TOKEN>"
}

mcp = FastMCP.from_fastapi(
    app=app,
    name="Greythr clone app",
    httpx_client_kwargs={
        "headers": headers
    }
)

if __name__ == "__main__":
    mcp.run()

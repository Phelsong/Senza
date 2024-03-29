# libs
import os
from uvicorn import Server as UV_Server, Config as UV_Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# imports
from routers.nav import nav


# =============================================================================
server_config: UV_Config
# print(os.environ.get("SITE_ENV"))

if os.environ.get("SITE_ENV") == "PRODUCTION":
    server_config = UV_Config(
        app="main:app",
        host="0.0.0.0",
        port=8062,
        root_path=".",
        workers=5,
        log_level="info",
        forwarded_allow_ips="*",
    )
else:
    server_config = UV_Config(
        app="main:app",
        host="0.0.0.0",
        port=8062,
        root_path=".",
        log_level="info",
        workers=5,
        ssl_certfile="./certs/dev-cert.pem",
        ssl_keyfile="./certs/dev-key.pem",
    )


# print(server_config.__dict__)

server: UV_Server = UV_Server(server_config)


app = FastAPI(root_path=".")
origins: list[str] = [
    "http://localhost",
    "http://127.0.0.1",
    "http://[::]",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------

app.mount(path="/public", app=StaticFiles(directory="public"), name="public")
app.mount(
    path="/senza",
    app=StaticFiles(directory="senza"),
    name="senza",
)
app.mount(
    path="/web",
    app=StaticFiles(directory="web"),
    name="web",
)
app.mount(
    path="/assets",
    app=StaticFiles(directory="assets"),
    name="assets",
)
# ---------------------------------------------------------
app.include_router(nav)
# ---------------------------------------------------------


@app.get("/status")
def get_status() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/favicon.ico")
def get_favicon() -> FileResponse:
    return FileResponse(path="public/favicon.ico", status_code=200)


# ------------------------------------------------------------------------------


if __name__ == "__main__":
    server.run()

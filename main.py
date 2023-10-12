import uvicorn
from fastapi import FastAPI
from avitotech_test.api.balance.handlers import balance_router


def include_router(app):  # set routes to the app instance
    app.include_router(balance_router)


app = FastAPI(title="AvitoTech_TEST", version="0.0.3")
include_router(app)


@app.get("/")
async def index():
    return "add /docs to your current url to see all features of the app"


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)  # run app on the host and port

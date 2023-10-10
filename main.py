import uvicorn
from fastapi import FastAPI
from avitotech_test.api.balance.handlers import balance_router


def include_router(app):  # set routes to the app instance
    app.include_router(balance_router)


def start_application():  # start config of the app and including routers to it
    app = FastAPI(title="AvitoTech_TEST", version="0.0.3")
    include_router(app)

    return app


if __name__ == '__main__':
    # run app on the host and port
    app = start_application()
    uvicorn.run(app, host='0.0.0.0', port=8001)

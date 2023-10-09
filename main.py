import uvicorn
from fastapi import FastAPI
from avitotech_test.balance.handlers import balance_router

app = FastAPI(title="AvitoTech_TEST")

# set routes to the app instance
app.include_router(balance_router)

if __name__ == '__main__':
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)

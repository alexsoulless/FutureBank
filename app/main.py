from fastapi import FastAPI
from app.routers.users_router import router as userRouter
from app.routers.transactions_router import router as transactionsRouter
from app.routers.taxes_router import router as taxesRouter


app = FastAPI()
app.include_router(userRouter)
app.include_router(transactionsRouter)
app.include_router(taxesRouter)


@app.get("/ping/")
def ping():
    return {
        "responce": "pong",
    }

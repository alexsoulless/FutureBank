from fastapi import FastAPI
from routers.users_router import router as userRouter
from routers.transactions_router import router as transactionsRouter
from routers.taxes_router import router as taxesRouter


app = FastAPI()
app.include_router(userRouter)
app.include_router(transactionsRouter)
app.include_router(taxesRouter)


@app.get("/ping/")
def ping():
    return {
        "responce": "pong",
    }

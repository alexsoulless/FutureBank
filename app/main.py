from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.users_router import router as userRouter
from app.routers.transactions_router import router as transactionsRouter
from app.routers.taxes_router import router as taxesRouter
from app.db import test_db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await test_db_connection()
    yield
    # on shutdown
    pass

app = FastAPI(lifespan=lifespan)
app.include_router(userRouter)
app.include_router(transactionsRouter)
app.include_router(taxesRouter)


@app.get("/ping/")
def ping():
    return {
        "responce": "pong",
    }

from fastapi import APIRouter, HTTPException, Query, Path, status

router = APIRouter(prefix="/taxes", tags=["taxes"])
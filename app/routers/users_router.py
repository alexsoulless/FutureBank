from fastapi import APIRouter, HTTPException, Query, Path, status

router = APIRouter(prefix="/users", tags=["users"])
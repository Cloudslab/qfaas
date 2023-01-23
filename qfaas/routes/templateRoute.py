from fastapi import APIRouter, Body, Depends, Request
from qfaas.dependency.auth import get_current_active_user
from qfaas.models.user import UserSchema


router = APIRouter()


@router.get("/", response_description="Function template fetched successfully.")
async def get_template_data(
    currentUserUsername: UserSchema = Depends(get_current_active_user),
):
    pass

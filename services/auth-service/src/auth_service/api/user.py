from auth_service import constants
from auth_service import domain
from auth_service.api.schema import user
from auth_service.service.user import UserService
from fastapi import Depends
from metagrim_common.base.deps import get_authorised_user
from metagrim_common.base.router import APIRouter
from metagrim_common.base.utils import respond
from metagrim_common.domains import UserSearchPaginatedParameters
from metagrim_common.schema import ResponseSchema

router = APIRouter(prefix="/user", tags=["User Management"])


@router.get("", response_model=user.UserPaginationResponseSchema)
async def get_users(
    paginate: user.UserSearchPaginatedRequestSchema = Depends(user.UserSearchPaginatedRequestSchema),
    current_user_id: str = Depends(get_authorised_user),
) -> user.UserPaginationResponseSchema:
    service = UserService(current_user_id=current_user_id)
    paginated = UserSearchPaginatedParameters(**paginate.model_dump(exclude_none=True))
    result = await service.list_users(paginated)
    return result  # type: ignore


@router.post("", response_model=ResponseSchema)
async def create_user(
    user_form: user.UserCreateSchema,
    current_user_id: str = Depends(get_authorised_user),
) -> ResponseSchema:
    service = UserService(current_user_id=current_user_id)
    entity = domain.UserDb(**user_form.model_dump(exclude_none=True))
    entity.set_pass_hash(user_form.password)
    new_user = await service.create_user(entity, requested_actions=[])
    return respond(constants.HTTP_201_CREATED, public_id=new_user.id)  # type: ignore


@router.patch("/{public_id}", response_model=user.UserReadSchema)
async def update_user(
    public_id: str,
    user_form: user.UserUpdateSchema,
    current_user_id: str = Depends(get_authorised_user),
) -> user.UserReadSchema:
    service = UserService(current_user_id=current_user_id)
    entity = domain.User(**user_form.model_dump(exclude_unset=True))
    entity.id = public_id
    updated_entity = await service.update_user(
        entity,
        requested_actions=[action.value for action in user_form.allowed_actions] if user_form.allowed_actions else None,
    )
    return updated_entity  # type: ignore


@router.delete("/{public_id}", response_model=ResponseSchema)
async def delete_user(
    public_id: str,
    current_user_id: str = Depends(get_authorised_user),
):
    service = UserService(current_user_id=current_user_id)
    await service.delete_user(public_id)
    return respond(constants.RESPONSE_OK)


@router.get("/{public_id}", response_model=user.UserReadSchema)
async def get_user(
    public_id: str,
    current_user_id: str = Depends(get_authorised_user),
):
    service = UserService(current_user_id=current_user_id)
    user = await service.get_user(public_id)
    return user


@router.patch("/{public_id}/status")
async def change_user_status(
    public_id: str,
    current_user_id: str = Depends(get_authorised_user),
):
    service = UserService(current_user_id=current_user_id)
    await service.change_user_status(public_id)
    return respond(constants.RESPONSE_OK)

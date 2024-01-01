import typing
from datetime import date
from logging import getLogger

from metagrim_common import enums
from metagrim_common.base.utils import get_password_hash
from metagrim_common.base.utils import verify_password
from pydantic import BaseModel
from pydantic import computed_field
from pydantic import ConfigDict
from pydantic import Field
from pydantic import UUID4
from typing_extensions import Literal
from typing_extensions import TypeAlias

IncEx: TypeAlias = "set[int] | set[str] | dict[int, typing.Any] | dict[str, typing.Any] | None"

T = typing.TypeVar("T")
NOT_DEFINED = typing.TypeVar("NOT_DEFINED")
logger = getLogger(__name__)


class BaseDomain(BaseModel):
    @property
    def protected_fields(self) -> typing.List[str]:
        return ["id"]

    @property
    def special_fields(self) -> typing.List[str]:
        return []

    @property
    def related_fields(self) -> typing.List[str]:
        return []

    id: UUID4 | None = None

    @staticmethod
    def _check_field(obj_: typing.Any, field_: str):
        """
        Utility function to check if given field exists in the other object/dict

        :param obj_:
        :param field_:
        :return:
        """
        try:
            if isinstance(obj_, BaseModel):
                return field_ in obj_.model_fields
            elif isinstance(obj_, dict):
                return field_ in obj_
            else:
                return hasattr(obj_, field_)
        except TypeError:
            return hasattr(obj_, field_)

    @staticmethod
    def _get_value_(obj: typing.Any, field_: str, default: typing.Any = None) -> typing.Any:
        """
        Utility function to retrieve the value of any object/dict

        :param obj:
        :param field_:
        :param default:
        :return:
        """
        try:
            return obj[field_]
        except (TypeError, KeyError):
            return getattr(obj, field_, default)

    def _copy_value(self, name: str, o_val: typing.Any, override_strategy: str = None):
        """
        This function is meant to override if you need different approach to copy the value or need some more processing

        :param name: str: Name of the field
        :param o_val: typing.Any: Value of the field in other object
        :param override_strategy: SELF_NULL | OTHER_NOT_NULL
                    SELF_NULL: If self.{field} == None then only copy value from other_obj.{field}
                    OTHER_NOT_NULL: If other_obj.{field} != None then only copy other_obj.{field}
        :return:
        """
        value = getattr(self, name)
        if override_strategy == "SELF_NULL" and not value:
            # Copy value from target only if current value is None
            setattr(self, name, o_val)
        elif override_strategy == "OTHER_NOT_NULL" and o_val:
            # Copy the value from target only when target value is not None
            setattr(self, name, o_val)
        elif not override_strategy:
            # Always copy the value from Target
            setattr(self, name, o_val)

    def copy_(self, other_obj: typing.Any, override_strategy: str = None):
        """
        Copy the values from the other object to the self by given strategy

        Do not override unless and until it is absolutely necessary.
        To change the copy behaviour please override `_copy_value` method

        :param other_obj:
        :param override_strategy: SELF_NULL | OTHER_NOT_NULL
                    SELF_NULL: If self.{field} == None then only copy value from other_obj.{field}
                    OTHER_NOT_NULL: If other_obj.{field} != None then only copy other_obj.{field}
        :return:
        """
        computed_fields_ = self.model_computed_fields
        for name, field_ in self.model_fields.items():

            if computed_fields_.get(name):
                # Do not operate on computed field
                continue

            # Take care of the defined aliases while performing the copy
            alias = field_.alias
            if alias and self._check_field(other_obj, alias):
                o_val = self._get_value_(other_obj, alias, None)
            elif self._check_field(other_obj, name):
                o_val = self._get_value_(other_obj, name, None)
            else:
                # As field is not defined in the other object
                # Continue to next field
                continue
            self._copy_value(name, o_val, override_strategy=override_strategy)

    def __add__(self, other: typing.Union[dict, T]) -> T:
        """
        Combines the details
        If First object do not have the value then only we will consider the value of other object
        We assume that the current object is populated from Database data, and we are overriding with request data

        :param other:
        :return:
        """
        if not issubclass(type(other), BaseDomain) and not type(other) == dict:
            # Only same types can be added
            raise NotImplementedError(f"Can not add {self.__class__.__name__} type in {type(other)}")

        if issubclass(type(other), BaseDomain):
            for field_, value in self:
                o_val = self._get_value_(other, field_, None)
                # Set the new values, override with other values always
                self._add(field_, o_val)
            return self
        else:
            for field_, value in other.items():
                o_val = value
                # Set the new values, override with other values always
                self._add(field_, o_val)
            return self

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        exclude_related: bool = False,
        exclude_computed: bool = False,
    ) -> dict[str, typing.Any]:
        if exclude_related:
            if isinstance(exclude, set):
                exclude.update(set(self.related_fields))
            else:
                exclude = set(self.related_fields)
        if exclude_computed:
            if isinstance(exclude, set):
                exclude.update(set(self.model_computed_fields.keys()))
            else:
                exclude = set(set(self.model_computed_fields.keys()))
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )

    def _add(self, field_: str, o_val: typing.Any):
        """
        Define how to replace the source value with other value
        This function is meant to override, if we don't want the default way
        :param field_: Field name
        :param o_val: Value of field in other object
        :return:
        """
        computed_fields_ = self.model_computed_fields
        value = getattr(self, field_)
        try:

            if computed_fields_.get(field_):
                # Do not operate on computed field
                return

            if field_ in self.protected_fields and value:
                # Do not override protected fields
                return
        except TypeError as e:
            # Ignoring the exception if self.protected_fields is not declared
            logger.warning(f"{type(self)} is not having 'protected_fields' attribute Exception: {e}", exc_info=True)

        try:
            is_special_field = field_ in self.special_fields
        except TypeError as e:
            is_special_field = False
            # Ignoring the exception if self.special_fields is not declared
            logger.warning(f"{type(self)} is not having 'special_fields' attribute Exception: {e}", exc_info=True)

        if o_val:
            if isinstance(o_val, BaseDomain) and isinstance(value, BaseDomain):
                value = value + o_val
                # Merge the source value with the other value and update the source value
                setattr(self, field_, value)
            elif is_special_field:
                if isinstance(value, list):
                    # Merge the two lists
                    value = list(set(value).union(set(o_val)))
                # Merge the source value with the other value and update the source value
                setattr(self, field_, value)
            else:
                # By default, always replace the source value with other value
                setattr(self, field_, o_val)


class UserAction(BaseDomain):
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True)

    @property
    def related_fields(self) -> typing.List[str]:
        return ["user"]

    @property
    def protected_fields(self) -> typing.List[str]:
        result = super().protected_fields
        result.extend(["user_id", "action"])
        return result


class User(BaseDomain):
    email: str = Field(default=None)
    mobile: str | None = Field(default=None)
    user_type: enums.UserTypeEnum = Field(default=enums.UserTypeEnum.ticket_agent)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    status: enums.UserStatusEnum = Field(default=enums.UserStatusEnum.inactive)

    model_config = ConfigDict(from_attributes=True)

    @property
    def related_fields(self) -> typing.List[str]:
        return ["user_actions", "actions"]

    @property
    def protected_fields(self) -> typing.List[str]:
        result = super().protected_fields
        result.extend([])
        return result

    @computed_field
    @property
    def user_actions(self) -> typing.List[str]:
        return ["*"]


class UserDb(User):
    password_hash: str = None

    def set_pass_hash(self, password):
        self.password_hash = get_password_hash(password)

    def verify_password(self, password):
        return verify_password(password, self.password_hash)

    model_config = ConfigDict(from_attributes=True)


class PaginatedParameters(BaseModel):
    page: int = 1
    page_size: int = 100
    order_by: str = "created_at"
    order: enums.OrderEnum = enums.OrderEnum.desc


class SearchPaginatedParameters(PaginatedParameters):
    search: str | None = None
    page: int = 1
    page_size: int = 100
    order_by: str = "created_at"
    order: enums.OrderEnum = enums.OrderEnum.desc


class SearchRangeFilterParameters(BaseDomain):
    range_from: date | None = None
    range_to: date | None = None
    range_field: str = "created_at"
    range_operator: str = "between"


class UserSearchPaginatedParameters(SearchPaginatedParameters):
    user_type: typing.Optional[enums.UserTypeEnum] = None

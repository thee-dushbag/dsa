import typing as ty

__all__ = "NONE", "NONETYPE", "Optional", "is_not_none"

_T = ty.TypeVar("_T")

def _scrub_class(Class: ty.Type, val: ty.Any = None):
    Class.__new__ = lambda *_, **__: val
    Class.__init__ = lambda *_, **__: None
    if not hasattr(Class, "__eq__"):
        Class.__eq__ = lambda s, o: s is o  # type: ignore


def _single_none(Class: ty.Type):
    instance = None

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = Class(*args, **kwargs)
            _scrub_class(Class, instance)
        return instance

    return get_instance


@_single_none
class _NONETYPE:
    def __str__(self) -> str:
        return "<NONE>"

    def __bool__(self) -> bool:
        return False

    def __setattr__(self, _: str, __: ty.Any) -> ty.NoReturn:
        raise NotImplementedError

    def __delattr__(self, _: str) -> ty.NoReturn:
        raise NotImplementedError

    def __getattr__(self, *_) -> ty.NoReturn:
        raise NotImplementedError

    def __init_subclass__(cls) -> ty.NoReturn:
        raise NotImplementedError

    __repr__ = __str__

NONE: _NONETYPE = _NONETYPE()
NONETYPE: ty.Type[_NONETYPE] = type(NONE)
Optional: ty.TypeAlias = ty.Union[_T, _NONETYPE]

def is_not_none(val: Optional[_T]) -> ty.TypeGuard[_T]:
    return val is not NONE
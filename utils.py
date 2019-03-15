from typing import List, Callable, Any

NULLABLE_ERROR_MSG = 'Not null allowed'
VALID = 'Valid object'

def append(list_: list, element) -> list:
    copy = list(list_)
    copy.append(element)
    return copy

def check_null(obj) -> str:
    return if_(obj is None, NULLABLE_ERROR_MSG)


def insert_check_null(old_list: list) -> List[Callable[[Any], str]]:
    new_list = list(old_list)
    new_list.insert(0, check_null)
    return new_list


def if_(condition: bool, error_msg: str) -> str:
    return error_msg if condition else VALID


# def is_empty(list_: list) -> bool:
#     if not isinstance(list_, list):
#         raise Exception('It is not a List')
#     return len(list_) == 0


def exec_validators(obj: Any, validators: List[Callable[[Any], str]]):
    for validate in validators:
        message = validate(obj)
        if message != VALID:
            return message
    return VALID


def check_null_and_exec_validators(obj: Any, validators: List[Callable[[Any], str]], transform: Callable):
    message = check_null(obj)
    if message != VALID:
        return message
    try:
        transformed = transform(obj)
        return exec_validators(transformed, validators)
    except:
        return exec_validators(obj, validators)


def create_validator(
        validators: List[Callable[[Any], str]],
        nullable: bool = False,
        transform: Callable = None
) -> Callable[[Any], str]:
    if not nullable and transform is None:
        return lambda obj: exec_validators(obj, insert_check_null(validators))
    if not nullable and transform is not None:
        return lambda obj: check_null_and_exec_validators(obj, validators, transform)
    if nullable and transform is None:
        return lambda obj: VALID if obj is None else exec_validators(obj, validators)
    if nullable and transform is not None:
        return lambda obj: VALID if obj is None else exec_validators(transform(obj), validators)

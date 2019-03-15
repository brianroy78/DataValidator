from datetime import date, datetime, time
from typing import Callable, Dict, Any, Tuple

from utils import if_, create_validator, VALID

# --- INTEGER ---
INT_ERROR_MSG = 'Value must be integer'
MIN_INT_ERROR_MSG = 'Integer must be greater or equal to %d'
MAX_INT_ERROR_MSG = 'Integer must be smaller or equal to %d'
MIN_MAX_ERROR_MSG = 'Param min_ has to be lower/shorter that max_'


def validate_min_max(min_, max_, type_):
    if not isinstance(min_, type_) or not isinstance(max_, type_) or min_ < max_:
        raise Exception(MIN_MAX_ERROR_MSG)


def create_int_validator(min_: int = None, max_: int = None, nullable: bool = False) -> Callable[[int], str]:
    # validate_min_max(min_, max_, int)
    validators = [lambda obj: if_(not isinstance(obj, int), INT_ERROR_MSG)]
    if isinstance(min_, int):
        min_value_msg = MIN_INT_ERROR_MSG % min_
        validators.append(lambda obj: if_(obj < min_, min_value_msg))
    if isinstance(max_, int):
        max_value_msg = MAX_INT_ERROR_MSG % max_
        validators.append(lambda obj: if_(obj > max_, max_value_msg))
    return create_validator(validators, nullable, int)


# --- FLOAT ---

FLOAT_ERROR_MSG = 'Value must be float'
MIN_FLOAT_ERROR_MSG = 'Float must be greater or equal to %d'
MAX_FLOAT_ERROR_MSG = 'Float must be smaller or equal to %d'


def create_float_validator(min_: float = None, max_: float = None, nullable: bool = False) -> Callable[[float], str]:
    # validate_min_max(min_, max_, float)
    validators = [lambda obj: if_(not isinstance(obj, float), FLOAT_ERROR_MSG)]
    if isinstance(min_, float):
        min_value_msg = MIN_FLOAT_ERROR_MSG % min_
        validators.append(lambda obj: if_(obj < min_, min_value_msg))
    if isinstance(max_, float):
        max_value_msg = MAX_FLOAT_ERROR_MSG % max_
        validators.append(lambda obj: if_(obj > max_, max_value_msg))
    return create_validator(validators, nullable, float)


# --- STRING ---

STR_ERROR_MSG = 'Value must be string'
MIN_LEN_STR_ERROR_MSG = 'String\'s length must be larger or equal to %d'
MAX_LEN_STR_ERROR_MSG = 'String\'s length must be shorter or equal to %d'


def create_str_validator(min_len: int = None, max_len: int = None, nullable: bool = False) -> Callable[[str], str]:
    validators = [lambda obj: if_(not isinstance(obj, str), STR_ERROR_MSG)]
    if isinstance(min_len, int):
        min_len_msg = MIN_LEN_STR_ERROR_MSG % min_len
        validators.append(lambda obj: if_(len(obj) < min_len, min_len_msg))
    if isinstance(max_len, int):
        max_len_msg = MAX_LEN_STR_ERROR_MSG % max_len
        validators.append(lambda obj: if_(len(obj) > max_len, max_len_msg))
    return create_validator(validators, nullable)


# --- DATE ---
DATE_ERROR_MSG = 'Value must be a date'
MIN_DATE_ERROR_MSG = 'Date must be higher or equal to %s'
MAX_DATE_ERROR_MSG = 'Date must be lower or equal to %s'
DATE_ISO_FORMAT = '%Y-%m-%d'


def to_date(obj):
    return datetime.strptime(obj, DATE_ISO_FORMAT).date() if isinstance(obj, str) else obj


def create_date_validator(min_: date = None, max_: date = None, nullable: bool = False) -> Callable[[date], str]:
    validators = [lambda obj: if_(not isinstance(obj, date), DATE_ERROR_MSG)]
    if isinstance(min_, date):
        min_msg = MIN_DATE_ERROR_MSG % min_
        validators.append(lambda obj: if_(obj < min_, min_msg))
    if isinstance(max_, date):
        max_msg = MAX_DATE_ERROR_MSG % max_
        validators.append(lambda obj: if_(obj > max_, max_msg))
    return create_validator(validators, nullable, to_date)


# --- DATETIME ---
DATETIME_ERROR_MSG = 'Value must be a datetime'
MIN_DATETIME_ERROR_MSG = 'Date must be higher or equal to %s'
MAX_DATETIME_ERROR_MSG = 'Date must be lower or equal to %s'
DATETIME_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'


def to_datetime(obj):
    return datetime.strptime(obj, DATETIME_ISO_FORMAT) if isinstance(obj, str) else obj


def create_datetime_validator(min_: datetime = None, max_: datetime = None, nullable: bool = False) -> Callable[[datetime], str]:
    validators = [lambda obj: if_(not isinstance(obj, datetime), DATETIME_ERROR_MSG)]
    if isinstance(min_, datetime):
        min_msg = MIN_DATETIME_ERROR_MSG % min_
        validators.append(lambda obj: if_(obj < min_, min_msg))
    if isinstance(max_, datetime):
        max_msg = MAX_DATETIME_ERROR_MSG % max_
        validators.append(lambda obj: if_(obj > max_, max_msg))
    return create_validator(validators, nullable, to_datetime)


# --- TIME ---
TIME_ERROR_MSG = 'Value must be a datetime'
MIN_TIME_ERROR_MSG = 'Date must be higher or equal to %s'
MAX_TIME_ERROR_MSG = 'Date must be lower or equal to %s'
TIME_ISO_FORMAT = '%H:%M:%S'


def to_time(obj):
    return datetime.strptime(obj, TIME_ISO_FORMAT).time() if isinstance(obj, str) else obj


def create_time_validator(min_: time = None, max_: time = None, nullable: bool = False) -> Callable[[time], str]:
    validators = [lambda obj: if_(not isinstance(obj, time), DATETIME_ERROR_MSG)]
    if isinstance(min_, time):
        min_msg = MIN_TIME_ERROR_MSG % min_
        validators.append(lambda obj: if_(obj < min_, min_msg))
    if isinstance(max_, time):
        max_msg = MAX_TIME_ERROR_MSG % max_
        validators.append(lambda obj: if_(obj > max_, max_msg))
    return create_validator(validators, nullable, to_time)


# --- BOOLEAN ---

BOOL_ERROR_MSG = 'Value must be boolean'


def create_bool_validator(nullable: bool = False) -> Callable[[bool], str]:
    return create_validator([lambda obj: if_(not isinstance(obj, bool), BOOL_ERROR_MSG)], nullable)


# --- LIST ---

LIST_ERROR_MSG = 'Value must be a list'
MIN_LEN_LIST_ERROR_MSG = 'List\'s length must be larger or equal to %d.'
MAX_LEN_LIST_ERROR_MSG = 'List\'s length must be shorter or equal to %d.'
LIST_ELEMENT_ERROR_TEMPLATE = '%d => %s'


def create_list_validator(
        min_len: int = None,
        max_len: int = None,
        nullable: bool = False,
        validate_element: Callable = False
) -> Callable[[list], str]:
    validators = [lambda obj: if_(not isinstance(obj, list), LIST_ERROR_MSG)]
    if isinstance(min_len, int):
        min_len_msg = MIN_LEN_LIST_ERROR_MSG % min_len
        validators.append(lambda obj: if_(len(obj) < min_len, min_len_msg))
    if isinstance(max_len, int):
        max_len_msg = MAX_LEN_LIST_ERROR_MSG % max_len
        validators.append(lambda obj: if_(len(obj) > max_len, max_len_msg))

    validate_list = create_validator(validators, nullable)

    def super_func(obj: list) -> str:
        message = validate_list(obj)
        if message != VALID:
            return message
        return filter_msgs(enumerate(obj), validate_as_list, validate_element)

    return super_func


# --- DICTIONARY ---


DICT_ERROR_MSG = 'Value must be a dictionary'
MIN_LEN_DICT_ERROR_MSG = 'Dictionary must contain %d or more elements'
MAX_LEN_DICT_ERROR_MSG = 'Dictionary must contain %d or less elements'
DICT_ELEMENT_ERROR_TEMPLATE = '%s => %s'


def create_dict_validator(
        nullable: bool = False,
        element_validators: Dict[str, Callable] = None
) -> Callable[[dict], str]:
    validators = [lambda obj: if_(not isinstance(obj, dict), DICT_ERROR_MSG)]
    validate_dict = create_validator(validators, nullable)

    def super_func(obj: dict) -> str:
        message = validate_dict(obj)
        if message != VALID:
            return message
        return filter_msgs(obj, validate_as_dict, element_validators)

    return super_func


def validate_as_list(index_element: tuple, validate: Callable, collection) -> Tuple[Any, str]:
    return index_element[0], validate(index_element[1])


def validate_as_dict(key, validate: dict, collection: dict) -> Tuple[Any, str]:
    return key, validate[key](collection[key])


def filter_msgs(collection, validate_as, validate_element):
    msgs = list()
    for values in collection:
        key, message = validate_as(values, validate_element, collection)
        if message != VALID:
            msgs.append(DICT_ELEMENT_ERROR_TEMPLATE % (key, message))
    return msgs if len(msgs) > 0 else VALID

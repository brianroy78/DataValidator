from datetime import date, datetime, time
from typing import Callable, Dict, Any, Tuple, List
from operator import lt, gt

from utils import if_, create_validator, VALID, append

# --- INTEGER ---
INT_ERROR_MSG = 'Value must be Integer'
MIN_MAX_ERROR_MSG = 'Param min_ has to be lower/shorter that max_'


def validate_min_max(min_, max_, type_):
    if not isinstance(min_, type_) or not isinstance(max_, type_) or min_ < max_:
        raise Exception(MIN_MAX_ERROR_MSG)

MIN_LEN_ERROR_MSG = '%s\'s length must be larger or equal to %s'
MAX_LEN_ERROR_MSG = '%s\'s length must be shorter or equal to %s'
MIN_ERROR_MSG = '%s must be greater or equal to %s'
MAX_ERROR_MSG = '%s must be smaller or equal to %s'
TYPE_ERROR_MSG = 'Value must be %s'
INT_TYPE = 'Integer'
FLOAT_TYPE = 'Float'
STR_TYPE = 'String'
BOOL_TYPE = 'Boolean'
DATE_TYPE = 'Date'
DATETIME_TYPE = 'Datetime'
TIME_TYPE = 'Time'
LIST_TYPE = 'List'
DICT_TYPE = 'Dictionary'

def create_int_validator(min_: int = None, max_: int = None, nullable: bool = False) -> Callable[[int], str]:
    validators = [lambda obj: if_(not isinstance(obj, int), TYPE_ERROR_MSG % INT_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_, int), create_limit_validator, lt, min_, MIN_ERROR_MSG, INT_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_, int), create_limit_validator, gt, max_, MAX_ERROR_MSG, INT_TYPE)
    return create_validator(validators, nullable, int)


# --- FLOAT ---



def create_float_validator(min_: float = None, max_: float = None, nullable: bool = False) -> Callable[[float], str]:
    # validate_min_max(min_, max_, float)
    validators = [lambda obj: if_(not isinstance(obj, float), TYPE_ERROR_MSG % FLOAT_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_, float), create_limit_validator, lt, min_, MIN_ERROR_MSG, FLOAT_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_, float), create_limit_validator, gt, max_, MAX_ERROR_MSG, FLOAT_TYPE)
    return create_validator(validators, nullable, float)


# --- STRING ---



def create_str_validator(min_len: int = None, max_len: int = None, nullable: bool = False) -> Callable[[str], str]:
    validators = [lambda obj: if_(not isinstance(obj, str), TYPE_ERROR_MSG % STR_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_len, int), create_len_limit_validator, lt, min_len, MIN_LEN_ERROR_MSG, STR_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_len, int), create_len_limit_validator, gt, max_len, MAX_LEN_ERROR_MSG, STR_TYPE)
    return create_validator(validators, nullable)


# --- DATE ---
DATE_ISO_FORMAT = '%Y-%m-%d'


def to_date(obj):
    return datetime.strptime(obj, DATE_ISO_FORMAT).date() if isinstance(obj, str) else obj


def create_date_validator(min_: date = None, max_: date = None, nullable: bool = False) -> Callable[[date], str]:
    validators = [lambda obj: if_(not isinstance(obj, date), TYPE_ERROR_MSG % DATE_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_, date), create_limit_validator, lt, min_, MIN_ERROR_MSG, DATE_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_, date), create_limit_validator, gt, max_, MAX_ERROR_MSG, DATE_TYPE)
    return create_validator(validators, nullable, to_date)


# --- DATETIME ---
DATETIME_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'


def to_datetime(obj):
    return datetime.strptime(obj, DATETIME_ISO_FORMAT) if isinstance(obj, str) else obj


def create_datetime_validator(min_: datetime = None, max_: datetime = None, nullable: bool = False) -> Callable[[datetime], str]:
    validators = [lambda obj: if_(not isinstance(obj, datetime), TYPE_ERROR_MSG % DATETIME_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_, datetime), create_limit_validator, lt, min_, MIN_ERROR_MSG, DATETIME_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_, datetime), create_limit_validator, gt, max_, MAX_ERROR_MSG, DATETIME_TYPE)
    return create_validator(validators, nullable, to_datetime)


# --- TIME ---
TIME_ISO_FORMAT = '%H:%M:%S'


def to_time(obj):
    return datetime.strptime(obj, TIME_ISO_FORMAT).time() if isinstance(obj, str) else obj


def create_time_validator(min_: time = None, max_: time = None, nullable: bool = False) -> Callable[[time], str]:
    validators = [lambda obj: if_(not isinstance(obj, time), TYPE_ERROR_MSG % TIME_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_, time), create_limit_validator, lt, min_, MIN_ERROR_MSG, TIME_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_, time), create_limit_validator, gt, max_, MAX_ERROR_MSG, TIME_TYPE)
    return create_validator(validators, nullable, to_time)


# --- BOOLEAN ---
def create_bool_validator(nullable: bool = False) -> Callable[[bool], str]:
    return create_validator([lambda obj: if_(not isinstance(obj, bool), TYPE_ERROR_MSG % BOOL_TYPE)], nullable)


# --- LIST ---
LIST_ELEMENT_ERROR_TEMPLATE = '%d => %s'


def create_list_validator(
        min_len: int = None,
        max_len: int = None,
        nullable: bool = False,
        validate_element: Callable = False
) -> Callable[[list], str]:
    validators = [lambda obj: if_(not isinstance(obj, list), TYPE_ERROR_MSG % LIST_TYPE)]
    validators = append_validator_if_setted(validators, isinstance(min_len, int), create_len_limit_validator, lt, min_len, MIN_LEN_ERROR_MSG, LIST_TYPE)
    validators = append_validator_if_setted(validators, isinstance(max_len, int), create_len_limit_validator, gt, max_len, MAX_LEN_ERROR_MSG, LIST_TYPE)

    validate_list = create_validator(validators, nullable)

    def super_func(obj: list) -> str:
        message = validate_list(obj)
        if message != VALID:
            return message
        return filter_msgs(enumerate(obj), validate_as_list, validate_element)

    return super_func


# --- DICTIONARY ---
MIN_LEN_DICT_ERROR_MSG = 'Dictionary must contain %d or more elements'
MAX_LEN_DICT_ERROR_MSG = 'Dictionary must contain %d or less elements'
DICT_ELEMENT_ERROR_TEMPLATE = '%s => %s'


def create_dict_validator(
        nullable: bool = False,
        element_validators: Dict[str, Callable] = None
) -> Callable[[dict], str]:
    validators = [lambda obj: if_(not isinstance(obj, dict), TYPE_ERROR_MSG % DICT_TYPE)]
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


def append_validator_if_setted(validators: List[callable], is_setted: bool, create_validator: callable, compare: callable, limit, template: str, type_: str) -> List[callable]:
    return append(validators, create_validator(compare, limit, template % (type_, str(limit)))) if is_setted else validators


def create_limit_validator(compare: callable, limit,  msg: str) -> callable:
    return lambda obj: msg if compare(obj, limit) else VALID


def create_len_limit_validator(compare: callable, limit,  msg: str) -> callable:
    return lambda obj: msg if compare(len(obj), limit) else VALID

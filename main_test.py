from datetime import date
from unittest import TestCase

from main import create_int_validator, create_dict_validator, create_bool_validator, create_float_validator, create_str_validator, create_list_validator, \
    INT_ERROR_MSG, MIN_INT_ERROR_MSG, MAX_INT_ERROR_MSG, FLOAT_ERROR_MSG, MIN_FLOAT_ERROR_MSG, MAX_FLOAT_ERROR_MSG, \
    STR_ERROR_MSG, MIN_LEN_STR_ERROR_MSG, MAX_LEN_STR_ERROR_MSG, BOOL_ERROR_MSG, LIST_ERROR_MSG, LIST_ELEMENT_ERROR_TEMPLATE, \
    DICT_ERROR_MSG, DICT_ELEMENT_ERROR_TEMPLATE, create_date_validator, DATE_ERROR_MSG, MIN_DATE_ERROR_MSG, MAX_DATE_ERROR_MSG
from utils import NULLABLE_ERROR_MSG, VALID


class TestCreateIntValidator(TestCase):
    def test_if_obj_is_int_return_valid(self):
        self.assertEqual(VALID, create_int_validator()(int()))

    def test_if_obj_is_not_int_return_int_type_error(self):
        self.assertEqual(INT_ERROR_MSG, create_int_validator()(str()))

    def test_if_int_is_smaller_than_min_return_min_int_error(self):
        min_value = 2
        self.assertEqual(MIN_INT_ERROR_MSG % min_value, create_int_validator(min_=min_value)(1))

    def test_if_int_is_between_min_max_return_valid(self):
        self.assertEqual(VALID, create_int_validator(min_=2, max_=4)(3))

    def test_if_int_is_greater_than_max_return_max_int_error(self):
        max_value = 2
        self.assertEqual(MAX_INT_ERROR_MSG % max_value, create_int_validator(max_=max_value)(4))

    def test_if_is_not_nullable_and_obj_is_null_return_nullable_error(self):
        self.assertEqual(NULLABLE_ERROR_MSG, create_int_validator(nullable=False)(None))

    def test_if_is_nullable_and_obj_is_null_return_valid(self):
        self.assertEqual(VALID, create_int_validator(nullable=True)(None))

    def test_if_not_nullable_and_transform_is_not_null_and_obj_is_null_return_nullable_error(self):
        self.assertEqual(NULLABLE_ERROR_MSG, create_int_validator(nullable=False)(None))

    def test_if_min_is_higher_than_max_raise_min_max_error(self):
        self.assertRaises(Exception, create_int_validator, min_=3, max=2)


class TestFloatValidator(TestCase):
    def test_if_obj_is_float_return_valid(self):
        self.assertEqual(VALID, create_float_validator()(float()))

    def test_if_obj_is_not_float_return_type_error(self):
        self.assertEqual(FLOAT_ERROR_MSG, create_float_validator()(str()))

    def test_if_float_is_smaller_than_min_return_min_float_error(self):
        min_value = 2.0
        self.assertEqual(MIN_FLOAT_ERROR_MSG % min_value, create_float_validator(min_=min_value)(1.0))

    def test_if_float_is_between_min_max_return_valid(self):
        self.assertEqual(VALID, create_float_validator(min_=2.1, max_=4.1)(3.9))

    def test_if_float_is_greater_than_max_return_max_float_error(self):
        max_value = 2.2
        self.assertEqual(MAX_FLOAT_ERROR_MSG % max_value, create_float_validator(max_=max_value)(4.1))

    def test_if_is_not_nullable_and_the_obj_is_null_return_nullable_error(self):
        self.assertEqual(NULLABLE_ERROR_MSG, create_float_validator(nullable=False)(None))

    def test_if_is_nullable_and_the_obj_is_null_return_valid(self):
        self.assertEqual(VALID, create_float_validator(nullable=True)(None))

    def test_if_min_is_higher_than_max_raise_min_max_error(self):
        self.assertRaises(Exception, create_float_validator, min_=3, max=2)


class TestCreateStrValidator(TestCase):
    def test_if_obj_is_str_return_valid(self):
        self.assertEqual(VALID, create_str_validator()(str()))

    def test_if_obj_is_not_str_return_str_type_error(self):
        self.assertEqual(STR_ERROR_MSG, create_str_validator()(dict()))

    def test_if_str_is_shorter_than_min_len_return_min_len_error(self):
        min_len_value = 2
        self.assertEqual(MIN_LEN_STR_ERROR_MSG % min_len_value, create_str_validator(min_len=min_len_value)(str()))

    def test_if_str_len_is_between_min_max_return_valid(self):
        self.assertEqual(VALID, create_str_validator(min_len=2, max_len=4)('123'))

    def test_if_str_is_larger_than_max_len_return_max_len_error(self):
        max_len_value = 2
        self.assertEqual(MAX_LEN_STR_ERROR_MSG % max_len_value, create_str_validator(max_len=max_len_value)('123'))

    def test_if_is_not_nullable_and_obj_is_null_return_nullable_error(self):
        self.assertEqual(NULLABLE_ERROR_MSG, create_str_validator(nullable=False)(None))

    def test_if_is_nullable_and_the_obj_is_null_return_valid(self):
        self.assertEqual(VALID, create_str_validator(nullable=True)(None))


class TestCreateDateValidator(TestCase):
    def test_if_obj_is_date_or_date_string_format_return_valid(self):
        self.assertEqual(VALID, create_date_validator()('2019-03-04'))

    def test_if_obj_is_not_date_return_date_type_error(self):
        self.assertEqual(DATE_ERROR_MSG, create_date_validator()('123'))

    def test_if_str_is_lower_than_min_return_min_error(self):
        min_value = date(2018, 1, 1)
        self.assertEqual(MIN_DATE_ERROR_MSG % min_value, create_date_validator(min_=min_value)('2017-01-01'))

    def test_if_date_is_between_min_max_return_valid(self):
        self.assertEqual(VALID, create_date_validator(min_=date(2018, 1, 1), max_=date(2020, 1, 1))('2019-1-1'))

    def test_if_date_is_higher_than_max_return_max_error(self):
        max_value = date(2018, 1, 1)
        self.assertEqual(MAX_DATE_ERROR_MSG % max_value, create_date_validator(max_=max_value)('2019-1-1'))


class TestCreateBoolValidator(TestCase):
    def test_if_obj_is_bool_type_return_valid(self):
        self.assertEqual(VALID, create_bool_validator()(True))

    def test_if_obj_is_not_bool_type_and_not_null_return_bool_type_error(self):
        self.assertEqual(BOOL_ERROR_MSG, create_bool_validator()(str()))


class TestCreateListValidator(TestCase):
    def test_if_obj_is_list_return_valid(self):
        self.assertEqual(VALID, create_list_validator()(list()))

    def test_if_obj_is_not_list_return_list_type_error(self):
        self.assertEqual(LIST_ERROR_MSG, create_list_validator()(str()))

    def test_if_list_elements_are_valid_return_valid(self):
        self.assertEqual(VALID, create_list_validator(validate_element=create_int_validator())([1, 2, 3]))

    def test_if_list_elements_are_not_valid_return_list_with_errors(self):
        self.assertIsInstance(create_list_validator(validate_element=create_int_validator())(['abc']), list)

    def test_if_list_element_is_not_int_return_list_with_int_type_error_and_the_index_one(self):
        expected_error = LIST_ELEMENT_ERROR_TEMPLATE % (1, INT_ERROR_MSG)
        result = create_list_validator(validate_element=create_int_validator())([1, 'abc'])
        self.assertIn(expected_error, result)
        self.assertEqual(len(result), 1)


class TestCreateDictValidator(TestCase):
    def test_if_obj_is_dict_return_valid(self):
        self.assertEqual(VALID, create_dict_validator()(dict()))

    def test_if_obj_is_not_dict_return_dict_type_error(self):
        self.assertEqual(DICT_ERROR_MSG, create_dict_validator()(str()))

    def test_if_dict_elements_are_valid_return_valid(self):
        self.assertEqual(VALID, create_dict_validator(element_validators=dict(a=create_int_validator()))(dict(a=1)))

    def test_if_dict_elements_are_not_valid_return_list_with_errors(self):
        self.assertIsInstance(create_dict_validator(element_validators=dict(a=create_int_validator()))(dict(a='abc')), list)

    def test_if_dict_element_is_not_int_return_list_with_int_type_error_and_key_equals_to_a(self):
        expected_error = DICT_ELEMENT_ERROR_TEMPLATE % ('a', INT_ERROR_MSG)
        self.assertIn(expected_error, create_dict_validator(element_validators=dict(a=create_int_validator()))(dict(a='abc')))

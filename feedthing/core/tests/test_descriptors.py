from django.core.exceptions import ValidationError
from django.test import TestCase

from ..descriptors import Descriptor, URL
from ..descriptors import Typed


class CoreDescriptorsTestCase(TestCase):
    def setUp(self):
        class TestStringField(Typed):
            typ = str

        self.typed_string_field_class = TestStringField

    def test_instantiate_descriptor_with_name_no_default_and_set_value(self):
        class TestClass:
            test_field = Descriptor('test_field')

        test_field_value = 'Hello, Field!'
        test_class_instance = TestClass()
        test_class_instance.test_field = test_field_value
        self.assertEqual(test_class_instance.test_field, test_field_value)

    def test_instantiate_descriptor_with_name_no_default_raises_KeyError_when_get_is_called_before_set(self):
        class TestClass:
            test_field = Descriptor('test_field')

        test_class_instance = TestClass()
        with self.assertRaises(KeyError):
            # noinspection PyStatementEffect
            test_class_instance.test_field

    def test_instantiate_descriptor_with_name_and_default_returns_default_value_when_get_is_called_before_set(self):
        test_field_default_value = 'Default Value'

        class TestClass:
            test_field = Descriptor('test_field', default=test_field_default_value)

        test_class_instance = TestClass()
        self.assertEqual(test_class_instance.test_field, test_field_default_value)

    def test_instantiate_descriptor_then_del_instance_raises_KeyError_when_get_is_called_afterward(self):
        class TestClass:
            test_field = Descriptor('test_field')

        test_field_value = 'Hello, Field!'
        test_class_instance = TestClass()
        test_class_instance.test_field = test_field_value

        self.assertEqual(test_class_instance.test_field, test_field_value)

        del test_class_instance.test_field

        with self.assertRaises(KeyError):
            # noinspection PyStatementEffect
            test_class_instance.test_field

    def test_instantiating_Typed_Descriptor_with_no_default_allows_setting_value_of_correct_type(self):
        class TestClass:
            test_field = self.typed_string_field_class('test_field')

        test_class_instance = TestClass()
        test_field_value = 'Hello, String!'
        test_class_instance.test_field = test_field_value

        self.assertEqual(test_class_instance.test_field, test_field_value)

    def test_instantiating_Typed_Descriptor_with_no_default_raises_TypeError_setting_value_of_incorrect_type(self):
        class TestClass:
            test_field = self.typed_string_field_class('test_field')

        test_class_instance = TestClass()

        with self.assertRaises(TypeError):
            test_class_instance.test_field = 1

    def test_instantiating_Typed_Descriptor_with_default_of_correct_type_returns_default_without_initial_set(self):
        test_field_default_value = 'Hello, Default String!'

        class TestClass:
            test_field = self.typed_string_field_class('test_field', default=test_field_default_value)

        test_class_instance = TestClass()
        self.assertEqual(test_class_instance.test_field, test_field_default_value)

    def test_instantiating_Typed_Descriptor_with_default_of_incorrect_type_raises_TypeError_upon_instantiation(self):
        with self.assertRaises(TypeError):
            # noinspection PyUnusedLocal
            class TestClass:
                test_field = self.typed_string_field_class('test_field', default=1)

    def test_setting_incorrect_value_on_URL_typed_field_raises_ValidationError(self):
        class TestClass:
            test_url_field = URL('test_url_field')

        test_class_instance = TestClass()

        with self.assertRaises(ValidationError):
            test_class_instance.test_url_field = 'not_a_url'

    def test_setting_correct_value_on_URL_typed_field_with_default(self):
        test_field_value = 'http://example.com/an/OK/URL/'
        test_field_default_value = ''

        class TestClass:
            test_url_field = URL('test_url_field', default=test_field_default_value)

        test_class_instance = TestClass()
        self.assertEqual(test_class_instance.test_url_field, test_field_default_value)

        with self.assertRaises(ValidationError):
            test_class_instance.test_url_field = 'not_a_url'

        test_class_instance.test_url_field = test_field_value
        self.assertEqual(test_class_instance.test_url_field, test_field_value)

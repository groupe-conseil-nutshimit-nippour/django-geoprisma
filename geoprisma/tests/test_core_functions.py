import django
from django.test import TestCase
from geoprisma.core.functions import load_class
from geoprisma.core.widgets.widgetbase import WidgetBase


class load_classTests(TestCase):
    def test_load_class(self):
        class_name_path = "geoprisma.core.widgets.widgetbase.WidgetBase"
        class_object = load_class(class_name_path)
        self.assertEqual(class_object, WidgetBase)

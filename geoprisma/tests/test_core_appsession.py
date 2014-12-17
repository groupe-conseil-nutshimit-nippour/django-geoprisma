import django
from django.test import TestCase
from geoprisma.core.appsession.appsession import AppSession
from geoprisma.core.widgets.widgetbase import WidgetBase
from geoprisma.models import Widget, WidgetType


class appsessionTests(TestCase):

    def setUp(self):
        self.appsession = AppSession()

    def test_appsession_instance(self):
        self.assertIsInstance(self.appsession, AppSession)

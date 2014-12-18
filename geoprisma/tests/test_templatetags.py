import django
from django.test import TestCase
from django.template import Template, Context


class genericObj(object):
    """
    A generic object for testing templatetags
    """

    def __init__(self):
        self.name = "test"
        self.status = "ready"

    def getOption(self, optionName):
        if optionName == "name":
            return self.name
        elif optionName == "status":
            return self.status

    def getName(self):
        return self.name


def render(template_string, context_dict=None):
    """
    A shortcut for testing template output.
    """
    if context_dict is None:
        context_dict = {}
    c = Context(context_dict)
    t = Template(template_string)
    return t.render(c).strip()


class object_extrasTests(TestCase):

    def test_callMethod(self):
        genObj = genericObj()
        template = """
        {% load object_extras %}
        {{ obj|args:"name"|call:"getOption" }}
        """
        context = {
            'obj': genObj
        }
        self.assertEqual(render(template, context), "test")

        template = """
        {% load object_extras %}
        {{ obj|call:"getName" }}
        """
        context = {
            'obj': genObj
        }
        self.assertEqual(render(template, context), "test")

    def test_check_type(self):
        genObj = genericObj()
        template = """
        {% load object_extras %}
        {{ obj|obj_type:"genericObj" }}
        """
        context = {
            'obj': genObj
        }
        self.assertEqual(render(template, context), "True")

        template = """
        {% load object_extras %}
        {{ obj|obj_type:"notexist" }}
        """
        context = {
            'obj': genObj
        }
        self.assertEqual(render(template, context), "False")


class static_extrasTests(TestCase):

    def setUp(self):
        self.widgetTypeSetJs = set()
        self.widgetTypeSetJs.add('queryonclick')
        self.widgetTypeSetCss = set()
        self.widgetTypeSetCss.add('geoexttoolbar')

    def test_getJsStatics(self):
        template = """
        {% load staticfiles %}
        {% load static_extras %}
        {% getJsStatics widgetTypeSet as widget_js %}
        {% for static_path in widget_js %}
            <script src="{% static static_path %}" type="text/javascript"></script>
        {% endfor %}
        """
        context = {
            'widgetTypeSet': self.widgetTypeSetJs
        }
        out = '<script src="/static/geoprisma/widgets/queryonclick/js/QueryOnClick.js" type="text/javascript"></script>'
        self.assertEqual(render(template, context), out)

    def test_getCssStatics(self):
        template = """
        {% load staticfiles %}
        {% load static_extras %}
        {% getCssStatics widgetTypeSet as widget_css %}
        {% for static_path in widget_css %}
            <link rel="stylesheet" type="text/css" href="{% static static_path %}" />
        {% endfor %}
        """
        context = {
            'widgetTypeSet': self.widgetTypeSetCss
        }
        out = '<link rel="stylesheet" type="text/css" href="/static/geoprisma/widgets/geoexttoolbar/css/GeoExtToolbar.css" />'
        self.assertEqual(render(template, context), out)

    def test_template_exist(self):
        template = """
        {% load static_extras %}
        {{ "geoprisma/widgets/queryonclick/queryonclick.html"|template_exists }}
        """

        self.assertEqual(render(template), "True")

        template = """
        {% load static_extras %}
        {{ "geoprisma/widgets/queryonclick/queryonclicknotexist.html"|template_exists }}
        """

        self.assertEqual(render(template), "False")


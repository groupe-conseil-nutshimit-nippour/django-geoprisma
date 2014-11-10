# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from geoprisma import views as geoprisma_views


@login_required
def maprender(request, *args, **kwargs):
    wsName = kwargs.get('wsName')
    viewId = kwargs.get('viewId')
    if not viewId:
        viewId = ""

    renderContext = geoprisma_views.maprender(request, wsName, viewId)
    if isinstance(renderContext, dict):
        templateName = renderContext.get("templateName")
        return render(request, "example_project/" + templateName , renderContext)
    else:
        return renderContext

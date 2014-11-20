import proxy
import requests
import re
from django.http import HttpResponse


class FeatureServerProxy(proxy.Proxy):

    def __init__(self, pobjService, prequest, pkwargs=None):
        """
        Constructeur

        Args:
            pobjService: Object service
            prequest: La requete
            pkwargs: request kwargs
        """
        super(FeatureServerProxy, self).__init__(pobjService, prequest)
        if pkwargs:
            self.kwargs = pkwargs

    def getLayer(self):
        if self.kwargs.get('layer'):
            return self.kwargs.get('layer')
        else:
            return ''


    def getID(self):
        if self.kwargs.get('data_id'):
            dataId = self.kwargs.get('data_id')
            if dataId.isdigit():
                return int(dataId)
        else:
            return None

    def getPathInfo(self):
        strPath = "/"+self.getLayer()
        if self.kwargs.get('data_id'):
            strPath += "/"+str(self.getID())
        return strPath

    def getLayers(self):
        objLayerList = []
        strLayer = self.getLayer()
        if strLayer != "":
            objLayerList.append(strLayer)
        return objLayerList


class FeatureServerGetCapabilityProxy(FeatureServerProxy):

    def getAction(self):
        return self.CRUD_READ

    def process(self):
        url = self.addParam(self.m_objService.source)
        requestUrl = requests.post(url)
        return HttpResponse(requestUrl)


class FeatureServerReadProxy(FeatureServerProxy):

    def getAction(self):
        return self.CRUD_READ

    def process(self):
        strPathInfo = self.getPathInfo()
        url = self.addParam(self.m_objService.source + strPathInfo)
        requestUrl = requests.get(url)
        return HttpResponse(requestUrl)


class FeatureServerCreateProxy(FeatureServerProxy):

    def getAction(self):
        return self.CRUD_CREATE

    def process(self):
        strPathInfo = self.getPathInfo()
        url = self.addParam(self.m_objService.source + strPathInfo)
        requestUrl = requests.post(url, data=self.m_objRequest.body)
        return HttpResponse(requestUrl)



class FeatureServerUpdateProxy(FeatureServerProxy):

    def getAction(self):
        return self.CRUD_UPDATE

    def process(self):
        strPathInfo = self.getPathInfo()
        url = self.addParam(self.m_objService.source + strPathInfo)
        requestUrl = requests.put(url , data=self.m_objRequest.body)
        return HttpResponse(requestUrl)


class FeatureServerDeleteProxy(FeatureServerProxy):

    def getAction(self):
        return self.CRUD_DELETE

    def process(self):
        strPathInfo = self.getPathInfo()
        url = self.addParam(self.m_objService.source + strPathInfo)
        requestUrl = requests.delete(url)
        return HttpResponse(requestUrl)


class FeatureServerProxyFactory(object):
    """
    Retourne le bon feature server proxy
    """

    def getFeatureServerProxy(self, pobjService, prequest, pkwargs=None):
        self.request = prequest
        self.featureServerProxy = FeatureServerProxy(pobjService, prequest, pkwargs)
        objFeatureServerProxy = None

        if self.isGetCapability():
            objFeatureServerProxy = FeatureServerGetCapabilityProxy(pobjService, prequest, pkwargs)
        elif self.isDelete():
            objFeatureServerProxy = FeatureServerDeleteProxy(pobjService, prequest, pkwargs)
        elif self.isUpdate():
            objFeatureServerProxy = FeatureServerUpdateProxy(pobjService, prequest, pkwargs)
        elif self.isCreate():
            objFeatureServerProxy = FeatureServerCreateProx(pobjService, prequest, pkwargs)
        else:
            objFeatureServerProxy = FeatureServerReadProxy(pobjService, prequest, pkwargs)

        return objFeatureServerProxy




    def isGetCapability(self):
        """
        Check if query is the type of getCapability | The layer is not specifield
        """
        strLayer = self.featureServerProxy.getLayer()
        return strLayer == ""


    def isDelete(self):
        data_id = self.featureServerProxy.getID()
        return data_id != None and self.request.method == "DELETE"


    def isCreate(self):
        data_id = self.featureServerProxy.getID()
        return data_id != None and self.request.body != "" and self.request.method == "POST"


    def isUpdate(self):
        data_id = self.featureServerProxy.getID()
        return data_id != None and self.request.method == "PUT"

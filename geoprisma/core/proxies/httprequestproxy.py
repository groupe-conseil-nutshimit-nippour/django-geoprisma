import proxy
import urllib
import urllib2
import tempfile
import os
from django.http import HttpResponse
import requests
import json


class HttpRequestProxy(proxy.Proxy):
    """
    Class HttpRequestProxy

    """
    def __init__(self, service, prequest):
        """
        Consructeur

        Args:
            service: Object service
            prequest: La requete
        """
        super(HttpRequestProxy, self).__init__(service, prequest)
        self.m_strRequestName = ""
        self.m_objArrayAvailableRequestsAction = {}
        self.m_objArrayResponseMetaINfo = []

        if not self.m_objRequest.GET.get('REQUEST'):
            raise Exception("REQUEST param is missing")

        self.m_strRequestName = self.m_objRequest.GET.get('REQUEST')

        createHttpRequests = self.m_objService.serviceoption_set.filter(name="createHttpRequests").values_list('value', flat=True)
        readHttpRequests = self.m_objService.serviceoption_set.filter(name="readHttpRequests").values_list('value', flat=True)
        updateHttpRequests = self.m_objService.serviceoption_set.filter(name="updateHttpRequests").values_list('value', flat=True)
        deleteHttpRequests = self.m_objService.serviceoption_set.filter(name="deleteHttpRequests").values_list('value', flat=True)
        if len(createHttpRequests) > 0:
            for availableRequest in createHttpRequests[0].split(","):
                self.m_objArrayAvailableRequestsAction[availableRequest] = self.CRUD_CREATE
        if len(readHttpRequests) > 0:
            for availableRequest in readHttpRequests[0].split(","):
                self.m_objArrayAvailableRequestsAction[availableRequest] = self.CRUD_READ
        if len(updateHttpRequests) > 0:
            for availableRequest in updateHttpRequests[0].split(","):
                self.m_objArrayAvailableRequestsAction[availableRequest] = self.CRUD_UPDATE
        if len(deleteHttpRequests) > 0:
            for availableRequest in deleteHttpRequests[0].split(","):
                self.m_objArrayAvailableRequestsAction[availableRequest] = self.CRUD_DELETE

        if len(self.m_objArrayAvailableRequestsAction) == 0:
            raise Exception(" Service has no available request")

        if not self.m_objArrayAvailableRequestsAction.get(self.m_strRequestName):
            raise Exception("Request has no available action")

    def getAction(self):
        return self.m_objArrayAvailableRequestsAction.get(self.m_strRequestName)

    def process(self):
        """
        Traite l'information a retourner

        Returns:
            HttpResponce
        """
        strAdditionalParams = {}
        excluded_headers = ('connection','keep-alive','proxy-authenticate','proxy-authorization','te','trailers','transfer-encoding','upgrade','content-encoding','content-length')
        objPostFields = self.m_objRequest.body
        objArrayLayers = []
        objArrayTmpFiles = []

        #if not objPostFields and not len(self.m_objRequest.POST) == 0:
        #    objPostFields = self.m_objRequest.POST
        #    if not len(self.m_objRequest.FILES) == 0:
        #        for (strFieldName, objArrayFileInfo) in self.m_objRequest.FILES.iteritems():
        #            if not len(objArrayFileInfo['temp_name']) == 0:
        #                strFileContents = urllib2.urlopen(objArrayFileInfo['tmp_name'])
        #                strFileName = tempfile.gettempdir()+'/'+objArrayFileInfo['name']
        #                objArrayTmpFiles.append(strFileName)
        #                filewriter = open(strFileName, 'W')
        #                filewriter.write(strFileContents)
        #                filewriter.close()
        #            else:
        #                objPostFields[strFieldName] = ""

        objArrayResources = self.m_objResource
        objArrayLayers.append(objArrayResources[0].datastores.get(service=self.m_objService).layers)
        strAdditionalParams['REQUEST_DATA'] = objArrayLayers[0]

        url = self.addParam(self.m_objService.source, strAdditionalParams)
        postfiles = self.m_objRequest.FILES
        postparams = self.m_objRequest.POST
        requestUrl = requests.post(url, files=postfiles, data=postparams)

        #Need to remove the temporary files
        #for strFilepath in objArrayTmpFiles:
        #    os.unlink(strFilepath)

        responce = HttpResponse(requestUrl)
        responce.status_code = requestUrl.status_code
        responce.reason_phrase = requestUrl.reason
        for header in requestUrl.headers:
            if header not in excluded_headers:
                responce[header] = requestUrl.headers.get(header)

        return responce

    def getLayers(self):
        return []

    def addParam(self, pstrUrl, pstrAdditionalParams):
        """
        Ajoute des parametres a un url

        Args:
            pstrUrl: L'url
            pstrAdditionalParams: Les parametre additionnel
        Returns:
            L'url avec les parametres en plus
        """
        if '?' in pstrUrl:
            return pstrUrl+"&"+urllib.urlencode(dict(self.getRequestParams(), **pstrAdditionalParams))
        else:
            return pstrUrl+"?"+urllib.urlencode(dict(self.getRequestParams(), **pstrAdditionalParams))

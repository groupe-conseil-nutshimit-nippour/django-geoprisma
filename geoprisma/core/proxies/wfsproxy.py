import proxy
import urllib
import re
import requests
from django.conf import settings
from django.http import HttpResponse
from lxml import etree as ET
from django.contrib.auth.models import User
from geoprisma.utils import isAuthorized
from geoprisma.models import Datastore


class WFSProxyFactory(object):
    """
    Un proxy factory pour le WFS qui retourne le bon proxy WFS selon l'operation demande.

    """

    WFS_OP_GETCAPABILITIES = 1
    WFS_OP_DESCRIBEFEATURETYPE = 2
    WFS_OP_GETFEATURE = 3
    WFS_OP_TRANSACTION = 4

    WFS_TRANSACTION_INSERT = 1
    WFS_TRANSACTION_UPDATE = 2
    WFS_TRANSACTION_DELETE = 3

    def getWFSProxy(self, pobjService, prequest):
        """
        Recupere le proxy selon l'operation

        Args:
            pobjService: Object service
            prequest: La requete
        Returns:
            un proxy WFS
        """
        strPostRequest = None
        strContentType = None
        iRequestType = None
        iOPType = None
        if prequest.method == 'POST':
            if prequest and prequest.POST.get('data'):
                strPostRequest = prequest.POST.get('data')
                iRequestType = WFSProxy.REQUEST_TYPE_POSTXML
            else:
                strPostRequest = prequest.body
                strContentType = prequest.META.get('CONTENT_TYPE')
                if strContentType is not None:
                    strTok = strContentType.split(';')
                    if strTok[0] and (strTok[0] == 'text/xml' or strTok[0] == 'application/xml'):
                        iRequestType = WFSProxy.REQUEST_TYPE_POSTXML
                    else:
                        iRequestType = WFSProxy.REQUEST_TYPE_POST
        else:
            iRequestType = WFSProxy.REQUEST_TYPE_GET

        if iRequestType == WFSProxy.REQUEST_TYPE_POSTXML:
            iOPType = self.getOperationFromXml(strPostRequest)

        if iRequestType == WFSProxy.REQUEST_TYPE_GET:
            iOPType = self.getOperationFromGET(prequest)

        objWFSProxy = None
        if iOPType == self.WFS_OP_GETCAPABILITIES:
            objWFSProxy = WFSGetCapabilityProxy(pobjService, prequest, strContentType, iRequestType, strPostRequest)
        elif iOPType == self.WFS_OP_DESCRIBEFEATURETYPE:
            objWFSProxy = WFSReadProxy(pobjService, prequest, strContentType, iRequestType, strPostRequest)
        elif iOPType == self.WFS_OP_GETFEATURE:
            objWFSProxy = WFSReadProxy(pobjService, prequest, strContentType, iRequestType, strPostRequest)
        elif iOPType == self.WFS_OP_TRANSACTION:
            pass

        if objWFSProxy is None:
            raise Exception("Proxy method not handled.")

        return objWFSProxy

    def getOperationFromGET(self, prequest):
        """
        Recupere l'operation dans l'url

        Args:
            prequest: La requete
        Returns:
            Operation WFS
        """
        strRequest = ''
        for (strKey, strValue) in prequest.GET.iteritems():
            if strKey.upper() == 'REQUEST':
                strRequest = strValue
                break
        if strRequest == 'GetCapabilities':
            return self.WFS_OP_GETCAPABILITIES
        elif strRequest == 'DescribeFeatureType':
            return self.WFS_OP_DESCRIBEFEATURETYPE
        elif strRequest == 'GetFeature':
            return self.WFS_OP_GETFEATURE
        return None

    def getOperationFromXml(self, pstrXMLRequest):
        """
        Recupere l'operation dans l'XML

        Args:
            pstrXMLRequest: le xml contenant l'operation
        Returns:
            Operation WFS
        """
        objDomDoc = ET.fromstring(pstrXMLRequest)
        rootTag = ET.QName(objDomDoc.tag).localname
        if rootTag == 'GetCapabilities':
            return self.WFS_OP_GETCAPABILITIES
        elif rootTag == 'DescribeFeatureType':
            return self.WFS_OP_DESCRIBEFEATURETYPE
        elif rootTag == 'GetFeature':
            return self.WFS_OP_GETFEATURE
        return None


class WFSProxy(proxy.Proxy):
    """
    Class WFSProxy qui herite de la class proxy de base

    """
    REQUEST_TYPE_POSTXML = 1
    REQUEST_TYPE_POST = 2
    REQUEST_TYPE_GET = 3

    def __init__(self, pobjService, prequest, pstrContentType, piRequestType, pstrPostRequest):
        """
        Constructeur

        Args:
            pobjService: Un object service
            prequest: la requete
            pstrContentType: le type de contenu
            piRequestType: le type de requete
            pstrPostRequest: String contenant du XML recu en POST
        """
        super(WFSProxy, self).__init__(pobjService, prequest)
        self.m_strContentType = pstrContentType
        self.m_iRequestType = piRequestType
        self.m_strPostRequest = pstrPostRequest

    def getLayers(self):
        """
        Recupere les couches selon le type de requete

        Returns:
            Tableau de couches
        """
        objArrayLayers = []
        namespaces = {'wfs': 'http://www.opengis.net/wfs',
                      '__empty_ns': ''}
        if self.m_iRequestType == self.REQUEST_TYPE_POSTXML:
            objDomDoc = ET.fromstring(self.m_strPostRequest)
            objArrayXPathResult = objDomDoc.findall('./wfs:Query/', namespaces)
            if objArrayXPathResult:
                strTypeNames = str(objArrayXPathResult[0].get('typeName'))
                listTok = strTypeNames.split(',')
                for strTok in listTok:
                    objMatches = re.search('^(?:\w+:)?(\w+)(?:=\w+)?$', strTok)
                    if objMatches:
                        strFTName = objMatches.group(1)
                        objArrayLayers.append(strFTName)
        elif self.m_iRequestType == self.REQUEST_TYPE_GET:
            for (strKey, strValue) in self.m_objRequest.GET.iteritems():
                if strKey.upper() == "LAYERS":
                    objArrayLayers = self.m_objRequest.GET.get(strKey).split(',')
                    break
        return objArrayLayers

    def getID(self):
        strPathInfo = self.getPathInfo()


class WFSReadProxy(WFSProxy):
    """
    Class WFSReadProxy qui herite de WFSProxy.
    Elle recupere les informations selon l'operation.

    """

    def getAction(self):
        return self.CRUD_READ

    def process(self):
        """
        Traite l'information a retourner

        Returns:
            HttpResponse
        """
        excluded_headers = ('connection',
                            'keep-alive',
                            'proxy-authenticate',
                            'proxy-authorization',
                            'te',
                            'trailers',
                            'transfer-encoding',
                            'upgrade',
                            'content-encoding',
                            'content-length')

        if self.m_iRequestType == self.REQUEST_TYPE_POSTXML:
            strPostRequest = self.m_strPostRequest
            strContentType = self.m_strContentType
            strPathInfo = self.getPathInfo()
            url = self.addParam(self.m_objService.source)
            headers = {}
            if strContentType == "text/xml" or strContentType == "application/xml":
                headers = {'Content-Type': strContentType+";charset=UTF-8"}
            if isinstance(strPostRequest, unicode):
                strPostRequest = strPostRequest.encode("utf-8")
            requestUrl = requests.post(url, data=strPostRequest, headers=headers)
            response = HttpResponse(requestUrl)
            response_content = response.content

            for header in requestUrl.headers:
                if header not in excluded_headers:
                    response[header] = requestUrl.headers.get(header)

            if requestUrl.headers['Content-Type'] == 'text/csv':
                strNewlineReplaceChar = None
                objCsvSeperatorChar = None
                utf8DecodeOption = None
                strFileName = "record.csv"
                response['Content-Disposition'] = 'attachement; filename="'+strFileName+'"'
                try:
                    strNewlineReplaceCharOption = self.m_objService.serviceoption_set.filter(name='csvNewlineReplaceChar')
                    if len(strNewlineReplaceCharOption) > 0:
                        strNewlineReplaceChar = strNewlineReplaceCharOption[0].value

                    objCsvSeperatorCharOption = self.m_objService.serviceoption_set.filter(name='csvSeperatorChar')
                    if len(objCsvSeperatorCharOption) > 0:
                        objCsvSeperatorChar = objCsvSeperatorCharOption[0].value

                    utf8DecodeOption = self.m_objService.serviceoption_set.filter(name='utf8Decode')
                    if len(utf8DecodeOption) > 0:
                        utf8DecodeOption = utf8DecodeOption[0].value

                    if objCsvSeperatorChar:
                        strCsvSeperatorChar = objCsvSeperatorChar
                    else:
                        strCsvSeperatorChar = ','
                    if strNewlineReplaceChar:
                        objArrayPatterns = re.findall('(\"[^\"]*\"'+strCsvSeperatorChar+'?|[^'+strCsvSeperatorChar+']*'+strCsvSeperatorChar+'?)', response.content)
                        objArrayPatterns = [pattern.decode('utf-8') for pattern in objArrayPatterns]
                        if objArrayPatterns:
                            for index in range(objArrayPatterns.count()):
                                strPattern = objArrayPatterns[index]
                                iQuotedString = re.search('(\"[^\"]*\"'+strCsvSeperatorChar+'?)', strPattern)
                                if iQuotedString:
                                    objArrayPatterns[index] = strPattern.replace("\n", strNewlineReplaceChar)
                            objArrayPatterns = [pattern.encode('utf-8') for pattern in objArrayPatterns]
                            response.content = ''.join(objArrayPatterns)
                except Exception:
                    raise
                try:
                    if utf8DecodeOption == "true":
                        response_content = response_content.decode('utf-8').encode('iso-8859-1')
                except Exception:
                    raise

                response.content = ""
                # Write UTF-8 BOM
                response.write(u'\ufeff'.encode('utf-8'))
                response.write(response_content)

            return response
        elif self.m_iRequestType == self.REQUEST_TYPE_GET:
            strPathInfo = self.getPathInfo()
            requestUrl = requests.get(self.addParam(self.m_objService.source))
            response = HttpResponse(requestUrl)
            for header in requestUrl.headers:
                if header not in excluded_headers:
                    response[header] = requestUrl.headers.get(header)

            return response


class WFSGetCapabilityProxy(WFSProxy):
    """
    Class WFSGetCapabilityProxy qui traite seulement le getCapabilities

    """

    def getAction(self):
        return self.CRUD_READ

    def process(self):
        """
        Recupere le XML retourne par mapserver et le decoupe selon les droits de l'utilisateur.
        Le decoupage est different pour chaque version WFS.

        Returns:
            HttpResponce
        """
        excluded_headers = ('connection',
                            'keep-alive',
                            'proxy-authenticate',
                            'proxy-authorization',
                            'te',
                            'trailers',
                            'transfer-encoding',
                            'upgrade',
                            'content-encoding',
                            'content-length')
        url = self.addParam(self.m_objService.source)
        requestUrl = requests.get(url)
        objXml = ET.fromstring(requestUrl.text.encode("utf-8"))
        docinfo = objXml.getroottree().docinfo
        wfsversion = objXml.get("version")
        user = User.objects.get(email=self.m_objRequest.user)
        # Gestion des sandbox
        baseUrl = ""
        if hasattr(settings, 'DEBUG_APP_URL') and settings.DEBUG_APP_URL:
            baseUrl = settings.DEBUG_APP_URL
        onlineResourceUrl = "http://"+self.m_objRequest.get_host()+baseUrl+"/gp/proxy/"+self.m_objService.slug+""
        removeList = list()

        #WFS VERSION 1.0.0
        if wfsversion == "1.0.0":
            for elem in objXml:
                if elem.tag == "{http://www.opengis.net/wfs}Service":
                    onlineResource = elem.find("{http://www.opengis.net/wfs}OnlineResource")
                    onlineResource.text = onlineResourceUrl
                if elem.tag == "{http://www.opengis.net/wfs}Capability":
                    requestList = elem.find("{http://www.opengis.net/wfs}Request")
                    for request in requestList:
                        dcptypelist = request.findall("{http://www.opengis.net/wfs}DCPType")
                        for dcptype in dcptypelist:
                            http = dcptype.find("{http://www.opengis.net/wfs}HTTP")
                            for method in http:
                                method.set("onlineResource", onlineResourceUrl)
                if elem.tag == "{http://www.opengis.net/wfs}FeatureTypeList":
                    for featureType in elem:
                        if featureType.tag == "{http://www.opengis.net/wfs}FeatureType":
                            featureTypeName = featureType.find("{http://www.opengis.net/wfs}Name")
                            try:
                                datastore = Datastore.objects.get(service=self.m_objService,
                                                                  layers=featureTypeName.text)
                                dataResourceList = datastore.resource_set.all()
                                for resource in dataResourceList:
                                    if isAuthorized(user, resource.name, "read"):
                                        break
                                    else:
                                        removeList.append(featureType)
                            except Datastore.DoesNotExist:
                                removeList.append(featureType)
            for featureType in removeList:
                featureTypeList = objXml.find("{http://www.opengis.net/wfs}FeatureTypeList")
                featureTypeList.remove(featureType)
        #WFS VERSION 1.1.0
        elif wfsversion == "1.1.0":
            for elem in objXml:
                if elem.tag == "{http://www.opengis.net/ows}OperationsMetadata":
                    for operation in elem:
                        httptag = operation.find("{http://www.opengis.net/ows}DCP").find("{http://www.opengis.net/ows}HTTP")
                        for method in httptag:
                            method.set("{http://www.w3.org/1999/xlink}href", onlineResourceUrl)
                if elem.tag == "{http://www.opengis.net/wfs}FeatureTypeList":
                    for featureType in elem:
                        if featureType.tag == "{http://www.opengis.net/wfs}FeatureType":
                            featureTypeName = featureType.find("{http://www.opengis.net/wfs}Name")
                            featureTypeNameText = featureTypeName.text.split(":")[0]
                            try:
                                datastore = Datastore.objects.get(service=self.m_objService, layers=featureTypeNameText)
                                dataResourceList = datastore.resource_set.all()
                                for resource in dataResourceList:
                                    if isAuthorized(user, resource.name, "read"):
                                        break
                                    else:
                                        removeList.append(featureType)
                            except Datastore.DoesNotExist:
                                removeList.append(featureType)
            for featureType in removeList:
                featureTypeList = objXml.find("{http://www.opengis.net/wfs}FeatureTypeList")
                featureTypeList.remove(featureType)

        responce = HttpResponse(ET.tostring(objXml, xml_declaration=True, encoding=docinfo.encoding))
        #responce = HttpResponse(requestUrl)
        for header in requestUrl.headers:
            if header not in excluded_headers:
                responce[header] = requestUrl.headers.get(header)
        return responce

    def getAction(self):
        #return self.CRUD_READ
        pass

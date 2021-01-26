""" APIGatewayClient Functions """

import json
import os
import requests
from . import api_settings as Settings

"""
Class for the API methods:
    GET /cl/auth/{moduleId}/login
    GET /cl/auth/{moduleId}/logout
    GET /cl/auth/logout
"""


class Cl_auth:

    def moduleLogin(self, _sessionId, _moduleId):

        if (Settings.DEBUG):
            print('Cl_auth moduleLogin INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_auth_module_login.format(
                    sessionId=_sessionId,
                    moduleId=_moduleId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_auth moduleLogin exception')
            r = requests.Response()

        return r

    def moduleLogout(self, _sessionId, _moduleId):

        if (Settings.DEBUG):
            print('Cl_auth moduleLogout INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_auth_module_logout.format(
                    sessionId=_sessionId,
                    moduleId=_moduleId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_auth moduleLogout exception')
            r = requests.Response()

        return r

    def logout(self, _sessionId):

        if (Settings.DEBUG):
            print('Cl_auth logout INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_auth_logout.format(
                    sessionId=_sessionId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_auth logout exception')
            r = requests.Response()

        return r


"""Class for the API method:
    GET /cl/callback
"""


class Cl_callback:

    def callback(self, _sessionId, _callbackAddr):
        if (Settings.DEBUG):
            print('Cl_callback callaback')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_callback.format(
                    sessionId=_sessionId,
                    clientCallbackAddr=_callbackAddr),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_callback callback exception')
            r = requests.Response()

        return r


"""
class Cl_ident_derivation:

class Cl_ident_linking:

class Cl_ident_mgr:
"""


class Cl_ident:

    """ JSON EXAMPLE FOR MGR/LIST:

        [
            {
                "id": "eIDASeidas.gr/gr/ermis-11076669",
                "type": "dataSet",
                "data": "{\"id\":\"e8cc197a-e088-4e0e-9eac-cb6f893231ca\",\"type\":\"eIDAS\",\"categories\":null,\"issuerId\":\"eIDAS\",\"subjectId\":null,\"loa\":null,\"issued\":\"Wed, 16 Sep 2020 12:30:30 GMT\",\"expiration\":null,\"attributes\":[{\"name\":\"http://eidas.europa.eu/attributes/naturalperson/CurrentFamilyName\",\"friendlyName\":\"FamilyName\",\"encoding\":\"UTF-8\",\"language\":\"N/A\",\"values\":[\"ΠΕΤΡΟΥ, PETROU\"]},{\"name\":\"http://eidas.europa.eu/attributes/naturalperson/CurrentGivenName\",\"friendlyName\":\"GivenName\",\"encoding\":\"UTF-8\",\"language\":\"N/A\",\"values\":[\"ΑΝΔΡΕΑΣ, ANDREAS ΠΕΤΡΟΥ, PETROU\"]},{\"name\":\"http://eidas.europa.eu/attributes/naturalperson/DateOfBirth\",\"friendlyName\":\"DateOfBirth\",\"encoding\":\"UTF-8\",\"language\":\"N/A\",\"values\":[\"1980-01-01\"]},{\"name\":\"http://eidas.europa.eu/attributes/naturalperson/PersonIdentifier\",\"friendlyName\":\"PersonIdentifier\",\"encoding\":\"UTF-8\",\"language\":\"N/A\",\"values\":[\"eidas.gr/gr/ermis-11076669\"]},{\"name\":\"http://eidas.europa.eu/LoA\",\"friendlyName\":\"LevelOfAssurance\",\"encoding\":\"UTF-8\",\"language\":\"N/A\",\"values\":[null]}],\"properties\":null}"
            },
            {
                "id": "eduPersonTargetedID***NotFound",
                "type": "dataSet",
                "data": "{\"id\":\"a7830ca0-57d5-41e5-aef9-71b224cb795c\",\"type\":\"eduGAIN\",\"categories\":null,\"issuerId\":\"This is the user ID.\",\"subjectId\":null,\"loa\":null,\"issued\":\"Wed, 16 Sep 2020 12:37:33 GMT\",\"expiration\":null,\"attributes\":[{\"name\":\"urn:oid:1.3.6.1.4.1.5923.1.1.1.10\",\"friendlyName\":\"eduPersonTargetedID\",\"encoding\":null,\"language\":null,\"values\":[null]},{\"name\":\"urn:oid:2.5.4.42\",\"friendlyName\":\"givenName\",\"encoding\":null,\"language\":null,\"values\":[\"SEAL\"]},{\"name\":\"urn:oid:0.9.2342.19200300.100.1.3\",\"friendlyName\":\"mail\",\"encoding\":null,\"language\":null,\"values\":[\"seal-test0@example.com\"]},{\"name\":\"urn:oid:2.5.4.3\",\"friendlyName\":\"cn\",\"encoding\":null,\"language\":null,\"values\":[\"Tester0 SEAL\"]},{\"name\":\"urn:oid:2.5.4.4\",\"friendlyName\":\"sn\",\"encoding\":null,\"language\":null,\"values\":[\"Tester0\"]},{\"name\":\"urn:oid:2.16.840.1.113730.3.1.241\",\"friendlyName\":\"displayName\",\"encoding\":null,\"language\":null,\"values\":[\"SEAL Tester0\"]},{\"name\":\"urn:oid:1.3.6.1.4.1.5923.1.1.1.6\",\"friendlyName\":\"eduPersonPrincipalName\",\"encoding\":null,\"language\":null,\"values\":[\"128052@gn-vho.grnet.gr\"]},{\"name\":\"urn:oid:1.3.6.1.4.1.5923.1.1.1.7\",\"friendlyName\":\"eduPersonEntitlement\",\"encoding\":null,\"language\":null,\"values\":[\"urn:mace:grnet.gr:seal:test\"]}],\"properties\":null}"
            }
        ]

    """

    def jsonParser(self, _data):
        if (isinstance(_data, requests.Response) and _data.status_code == 200):
            data = _data.json()

            for index in range(0, len(data)):
                result_data = json.loads(data[index].get('data'))
                data[index].update({'data': result_data})

            identities_list = list()

            for identity in range(0, len(data)):
                if data[identity]['data'].get('type') == 'eIDAS':

                    identities_list.append(
                        {
                            "id": data[identity]['data'].get('id'),
                            "provider": data[identity]['data'].get('type'),
                            "loa": data[identity]['data'].get('loa'),
                            "issued": data[identity]['data'].get('issued'),
                            "expiration": data[identity]['data'].get('expiration'),
                            "attributes": data[identity]['data'].get('attributes')})

                elif data[identity]['data'].get('type') == 'eduGAIN':

                    identities_list.append(
                        {
                            "id": data[identity]['data'].get('id'),
                            "provider": data[identity]['data'].get('type'),
                            "loa": data[identity]['data'].get('loa'),
                            "issued": data[identity]['data'].get('issued'),
                            "expiration": data[identity]['data'].get('expiration'),
                            "attributes": data[identity]['data'].get('attributes')})

                elif data[identity]['data'].get('type') == 'derivedID':

                    identities_list.append(
                        {
                            "id": data[identity]['data'].get('id'),
                            "provider": data[identity]['data'].get('type'),
                            "loa": data[identity]['data'].get('loa'),
                            "issued": data[identity]['data'].get('issued'),
                            "expiration": data[identity]['data'].get('expiration'),
                            "attributes": data[identity]['data'].get('attributes')})

                elif (data[identity]['data'].get('type') == 'linkedID' or data[identity]['data'].get('type') is None):

                    datasetA = {
                        "id": data[identity]['data'].get('datasetA').get('id'),
                        "provider": data[identity]['data'].get('datasetA').get('type'),
                        "loa": data[identity]['data'].get('datasetA').get('loa'),
                        "issued": data[identity]['data'].get('datasetA').get('issued'),
                        "expiration": data[identity]['data'].get('datasetA').get('expiration'),
                        "attributes": data[identity]['data'].get('datasetA').get('attributes')}

                    datasetB = {
                        "id": data[identity]['data'].get('datasetB').get('id'),
                        "provider": data[identity]['data'].get('datasetB').get('type'),
                        "loa": data[identity]['data'].get('datasetB').get('loa'),
                        "issued": data[identity]['data'].get('datasetB').get('issued'),
                        "expiration": data[identity]['data'].get('datasetB').get('expiration'),
                        "attributes": data[identity]['data'].get('datasetB').get('attributes')}

                    identities_list.append(
                        {
                            "id": data[identity]['data'].get('id'),
                            "provider": data[identity]['data'].get('type'),
                            "lloa": data[identity]['data'].get('lloa'),
                            "issued": data[identity]['data'].get('issued'),
                            "expiration": data[identity]['data'].get('expiration'),
                            "datasetA": datasetA,
                            "datasetB": datasetB})

            providers_list = list(identity.get('provider')
                                  for identity in identities_list)
            #['eIDAS', 'eduGAIN', 'eduGAIN', 'eduGAIN']

            # Adaptation until linked idenitites come with a valid provider:
            providers_list = [
                provider if provider is not None else 'linkedID' for provider in providers_list]

            # List without duplicity
            providers_list = list(set(providers_list))

            # Sorted list by caseforld key
            providers_list = sorted(providers_list, key=str.casefold)

            return dict({"uniqueProviders": providers_list,
                         "identitiesList": identities_list})
            #['eIDAS', 'eduGAIN']

        else:
            return list()

    def sourceRetrieve(self, _sessionId, _moduleId):

        if (Settings.DEBUG):
            print('Cl_ident sourceRetrieve INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_ident_source_module_retrieve.format(
                    sessionId=_sessionId,
                    moduleId=_moduleId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_ident sourceRetrieve exception')
            r = requests.Response()

        return r

    def mgrList(self, _sessionId):

        if (Settings.DEBUG):
            print('Cl_ident mgrList INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_ident_mgr_list.format(
                    sessionId=_sessionId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_ident mgrList exception')
            r = requests.Response()

        return r

    def linkingRequest(
            self,
            _sessionId,
            _moduleId,
            _datasetId_A,
            _datasetId_B):

        if (Settings.DEBUG):
            print('Cl_ident linkingRequest INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}
        payload = {'datasetIDa': _datasetId_A, 'datasetIDb': _datasetId_B}

        try:
            r = s.post(
                Settings.Prod.API_POST_cl_ident_linking_module_request.format(
                    moduleId=_moduleId,
                    sessionId=_sessionId),
                data=payload,
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_ident linkingRequest exception')
            r = requests.Response()

        return r

    def linkingRequestStatus(self, _sessionId, _moduleId, _requestId):

        if (Settings.DEBUG):
            print('Cl_ident linkingRequestStatus INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_ident_linking_module_request_status.format(
                    moduleId=_moduleId,
                    requestId=_requestId,
                    sessionId=_sessionId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_ident linkingRequestStatus exception')
            r = requests.Response()

        return r

    def derivationGenerate(self, _sessionId, _moduleId):

        if (Settings.DEBUG):
            print('Cl_ident derivationGenerate INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_ident_derivation_module_generate.format(
                    sessionId=_sessionId,
                    moduleId=_moduleId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_ident derivationGenerate exception')
            r = requests.Response()

        return r


"""Class for the API method:
    GET /cl/list/{collection}
"""


class Cl_list:

    def _fetchDescription(self, _name):
        description = Settings.Prod.GLOBAL_DESCRIPTION_DICT.get(_name)
        if (description):
            return description
        else:
            return ""

    def jsonParser(self, _data):
        if (isinstance(_data, requests.Response) and _data.status_code == 200):
            data = _data.json()
            return ({"name": data[x][list(data[x])[0]].get('entityId'), "description": self._fetchDescription(
                data[x][list(data[x])[0]].get('entityId'))} for x in range(0, len(data)))
        else:
            return list()

    def getCollection(self, _collection):

        try:
            if (Settings.DEBUG):
                print('Cl_list getCollection Session')
            s = requests.Session()

            headers = {'Accept': 'application/json'}
            if (Settings.DEBUG):
                print(Settings.Prod.SEAL_PROXY)

            r = s.get(
                Settings.Prod.API_GET_cl_list_collection.format(
                    collection=_collection),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)

            return r

        except BaseException:
            if (Settings.DEBUG):
                print('Cl_list getCollection exception')
            return requests.Response()


"""
Class for the API methods:
    GET /cl/persistence/{moduleID}/load
    GET /cl/persistence/{moduleID}/store
"""


class Cl_persistence:

    def load(self, _sessionId, _moduleId):

        if (Settings.DEBUG):
            print('Cl_persistence load INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_persistence_module_load.format(
                    sessionId=_sessionId,
                    moduleId=_moduleId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_persistence load exception')
            r = requests.Response()

        return r

    def store(self, _sessionId, _moduleId):

        if (Settings.DEBUG):
            print('Cl_persistence store INI')

        s = requests.Session()
        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_persistence_module_store.format(
                    sessionId=_sessionId,
                    moduleId=_moduleId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_persistence store exception')
            r = requests.Response()

        return r

    def perLoadSessionToken(self, _sessionToken, _password, _PDS):

        if (Settings.DEBUG):
            print('Cl_persistence perLoadSessionToken INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}
        payload = {'dataStore': _PDS}

        try:
            r = s.post(
                Settings.Prod.API_POST_cl_persistence_per_load_sessionToken.format(
                    sessionToken=_sessionToken,
                    password=_password),
                data=payload,
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_persistence perLoadSessionToken exception')
            r = requests.Response()
        return r

    def perLoad(self, _sessionToken):

        if (Settings.DEBUG):
            print('Cl_persistence perLoad INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}
        payload = {'msToken': _sessionToken}

        try:
            r = s.post(
                Settings.Prod.API_POST_cl_persistence_per_load,
                data=payload,
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_persistence perLoad exception')
            r = requests.Response()
        return r


"""
Class for the API methods:
    GET /cl/session/start
    GET /cl/session/end
"""


class Cl_session:

    sessionID = None

    def sessionStart(self, _sessionId=None):

        if (Settings.DEBUG):
            print('Cl_session sessionStart INI')

        s = requests.Session()
        headers = {'Accept': 'application/json'}

        if (_sessionId is not None):
            try:
                r = s.get(
                    Settings.Prod.API_GET_cl_session_start.format(
                        sessionId='?sessionID=' + _sessionId),
                    headers=headers,
                    proxies=Settings.Prod.SEAL_PROXY)

                if (r.status_code == 200):
                    self.sessionID = r.json().get('payload')

            except BaseException:
                if (Settings.DEBUG):
                    print('Cl_session sessionStart exception with sessionId')
                r = requests.Response()
        else:
            try:
                r = s.get(
                    Settings.Prod.API_GET_cl_session_start.format(
                        sessionId=''),
                    headers=headers,
                    proxies=Settings.Prod.SEAL_PROXY)

                if (r.status_code == 200):
                    self.sessionID = r.json().get('payload')

            except BaseException:
                if (Settings.DEBUG):
                    print('Cl_session sessionStart exception without sessionId')
                r = requests.Response()

        return r

    def sessionEnd(self, _sessionId=None):

        if (Settings.DEBUG):
            print('Cl_session sessionEnd INI')

        s = requests.Session()
        headers = {'Accept': 'application/json'}

        if (_sessionId is not None):
            try:
                r = s.get(
                    Settings.Prod.API_GET_cl_session_end.format(
                        sessionId=_sessionId),
                    headers=headers,
                    proxies=Settings.Prod.SEAL_PROXY)

            except BaseException:
                if (Settings.DEBUG):
                    print('Cl_session sessionEnd exception with sessionId')
                r = requests.Response()
        else:
            try:
                r = s.get(
                    Settings.Prod.API_GET_cl_session_end.format(
                        sessionId=self.sessionID),
                    headers=headers,
                    proxies=Settings.Prod.SEAL_PROXY)

            except BaseException:
                if (Settings.DEBUG):
                    print('Cl_session sessionEnd exception without sessionId')
                r = requests.Response()

        return r

    def sessionStartAndEnd(self):
        self.sessionStart()
        self.sessionEnd()

    def __str__(self):
        return self.sessionID


"""
Class for the API methods:
    GET /cl/token/validate
"""


class Cl_token:

    def validate(self, _msToken, _sessionId):

        if (Settings.DEBUG):
            print('Cl_token validate INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_token_validate.format(
                    msToken=_msToken,
                    sessionId=_sessionId),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_token validate exception')
            r = requests.Response()

        return r


"""
Class for the API methods:
    GET /cl/vc/issuing/generate
"""


class Cl_vcissuing:

    def generate(self, _sessionId, _SSIId, _vcDefinition):

        if (Settings.DEBUG):
            print('Cl_vcissuing generate INI')

        s = requests.Session()

        headers = {'Accept': 'application/json'}

        try:
            r = s.get(
                Settings.Prod.API_GET_cl_vc_issuing_module_generate.format(
                    SSIId=_SSIId,
                    sessionId=_sessionId,
                    vcDefinition=_vcDefinition),
                headers=headers,
                proxies=Settings.Prod.SEAL_PROXY)
        except BaseException:
            if (Settings.DEBUG):
                print('Cl_vcissuing generate exception')
            r = requests.Response()

        return r

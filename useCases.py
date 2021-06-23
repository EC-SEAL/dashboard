from .utils.api import *
from django.http import HttpResponse
from .controlFunctions import *
import time
from .utils import api_settings as Settings

import json

from urllib.parse import unquote

import sys
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

"""
    UC0.01

    CUSTOM USERCASE associated to cl/ident/mgr/list:

    It retrieves the storeEntry Set for the identiies loaded in the session (at the SM) without the linked ones.

"""


def uc0_01(request):

    def managerList(_UUID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: _ML01)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc0_01-ML-001: Error assert session exists or valid')
            return error_text, 401

        cl_ident = Cl_ident()
        user_session = getSessionId(_UUID)

        identities = cl_ident.jsonParser(
            cl_ident.mgrList(user_session.sessionID))

        #dict( {"uniqueProviders": list(set(providers_list)), "identitiesList": identities_list} )

        if('linkedID' in identities['uniqueProviders']):
            if (Settings.DEBUG):
                # TO-DO: Delete.
                print('There are linked identities in the dict.')

            # Remove Provider == 'linkedID'
            identities['uniqueProviders'].remove('linkedID')
            # Remove dictionaries that contents the ('provider': 'linkedID')
            # Key-Value inside.
            identities['identitiesList'] = [
                identity for identity in identities['identitiesList'] if not (
                    identity['provider'] == 'linkedID')]

        if('derivedID' in identities['uniqueProviders']):
            if (Settings.DEBUG):
                # TO-DO: Delete.
                print('There are derived identities in the dict.')

            # Remove Provider == 'derivedID'
            identities['uniqueProviders'].remove('derivedID')
            # Remove dictionaries that contents the ('provider': 'derivedID')
            # Key-Value inside.
            identities['identitiesList'] = [
                identity for identity in identities['identitiesList'] if not (
                    identity['provider'] == 'derivedID')]

        return '{}'.format(json.dumps(identities)), 200

    try:
        parametro_http_UUID = request.GET['data']
    except BaseException:
        return HttpResponse('Data not found in the request', status=404)

    if (len(parametro_http_UUID) == 32):
        response_text, status_code = managerList(parametro_http_UUID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'DEBUG-uc0_01-ML-002: Error invalid UUID = {}'.format(parametro_http_UUID))
        return HttpResponse('Invalid data', status=404)


"""
    UC0.02

    CUSTOM USERCASE associated to cl/ident/mgr/list:

    It retrieves the storeEntry Set for all identiies loaded in the session (at the SM).

"""


def uc0_02(UUID):

    def managerList(_UUID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: _ML02)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc0_02-ML-001: Error assert session exists or valid')
            return None

        cl_ident = Cl_ident()
        user_session = getSessionId(_UUID)

        identities = cl_ident.jsonParser(
            cl_ident.mgrList(user_session.sessionID))

        return identities

    try:
        assert(len(UUID) == 32)

        return managerList(UUID)

    except BaseException:
        if (Settings.DEBUG):
            print('DEBUG-uc0_02-ML-002: Error invalid UUID = {}'.format(UUID))
        return None


"""
    UC1.02
"""


def uc1_02(request):

    def loadLocalPDS(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: LLPDS)'

        cl_session = sessionControl(_UUID)
        cl_persistence = Cl_persistence()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc1_02-LLPDS-001: sessionId: ', cl_session.sessionID)

        # CLBK
        cl_url = '{0}/tokenValidate={1}'.format(
                Settings.Prod.SEAL_ENDPOINT,
                _UUID)
        r_callback = cl_callback.callback(
            cl_session.sessionID,
            cl_url)
        try:
            assert(r_callback.status_code == 200)
            
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc1_02-LLPDS-002: Error assert callback response ({})'.format(r_callback.status_code))
            return error_text, 404

        # PLOD
        response = cl_persistence.load(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc1_02-LLPDS-003: Error parsing persistence json response')
            return error_text, 404

        return '{}&{}&{}'.format(
            _UUID, response_address, response_sessionToken), 200

    if (Settings.DEBUG):
        print('uc1_02 INI')

    try:
        parametro_http_moduleID = request.GET['moduleID']

        # UUID generation
        UUID = getUUID()
        assert(UUID != 'UUID_ERROR')

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_02-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_02-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if (parametro_http_moduleID == 'Browser' or parametro_http_moduleID == 'Mobile'):
        response_text, status_code = loadLocalPDS(
            UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc1_02-004: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
    UC1.03
"""


def uc1_03(request):

    def loadCloudPDS(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: LCPDS)'

        cl_session = sessionControl(_UUID)
        cl_persistence = Cl_persistence()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc1_03-LCPDS-001: sessionId: ', cl_session.sessionID)

        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc1_03-LCPDS-002: Error assert callback response')
            return error_text, 404

        # PLOD
        response = cl_persistence.load(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc1_03-LCPDS-003: Error parsing persistence json response')
            return error_text, 404

        return '{}&{}&{}'.format(
            _UUID, response_address, response_sessionToken), 200

    try:
        parametro_http_moduleID = request.GET['moduleID']

        # UUID generation
        UUID = getUUID()
        assert(UUID != 'UUID_ERROR')

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_02-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_02-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if (parametro_http_moduleID ==
            'googleDrive' or parametro_http_moduleID == 'oneDrive'):
        response_text, status_code = loadCloudPDS(
            UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc1_03-004: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
    UC1.04
"""


def uc1_04(request):

    def SSI(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: SSI)'

        cl_session = sessionControl(_UUID)
        cl_ident = Cl_ident()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc1_04-SSI-001: sessionId: ', cl_session.sessionID)

        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc1_04-SSI-002: Error assert callback response')
            return error_text, 404

        # ISRE
        response = cl_ident.sourceRetrieve(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

            if (Settings.DEBUG):
                print(response.json())
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc1_04-SSI-003: Error parsing sourceRetrieve json response')
            return error_text, 404

        return '{}&{}&{}'.format(
            _UUID, response_address, response_sessionToken), 200

    try:
        parametro_http_moduleID = request.GET['moduleID']

        # UUID generation
        UUID = getUUID()
        assert(UUID != 'UUID_ERROR')

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_04-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_04-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_04-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if (parametro_http_moduleID == 'uPort' or parametro_http_moduleID == 'Sovrin'):
        response_text, status_code = SSI(UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc1_04-004: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
UC2.02
"""


def uc2_02(request):

    def storeLocalPDS(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: LLPDS)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc2_02-SLPDS-001: Error assert session exists or valid')
            return error_text, 401

        cl_session = sessionControl(_UUID)
        cl_persistence = Cl_persistence()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc2_02-SLPDS-002: sessionId: ', cl_session.sessionID)

        # CLBK
        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc2_02-SLPDS-003: Error assert callback response')
            return error_text, 404

        # PSTO
        response = cl_persistence.store(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc2_02-SLPDS-004: Error parsing persistence json response')
            return error_text, 404

        return '{}&{}'.format(response_address, response_sessionToken), 200

    if (Settings.DEBUG):
        print('uc2_02 INI')

    try:
        parametro_http_moduleID = request.GET['moduleID']
        parametro_http_UUID = request.GET['data']

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_02-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_02-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if (parametro_http_moduleID == 'Browser' or parametro_http_moduleID == 'Mobile'):
        response_text, status_code = storeLocalPDS(
            parametro_http_UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc2_02-004: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
UC2.05
"""


def uc2_05(request):

    def storeCloudPDS(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: LLPDS)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc2_05-SCPDS-001: Error assert session exists or valid')
            return error_text, 401

        cl_session = sessionControl(_UUID)
        cl_persistence = Cl_persistence()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc2_05-SCPDS-002: sessionId: ', cl_session.sessionID)

        # CLBK
        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc2_05-SCPDS-003: Error assert callback response')
            return error_text, 404

        # PSTO
        response = cl_persistence.store(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc2_05-SCPDS-004: Error parsing persistence json response')
            return error_text, 404

        return '{}&{}'.format(response_address, response_sessionToken), 200

    if (Settings.DEBUG):
        print('uc2_05 INI')

    try:
        parametro_http_moduleID = request.GET['moduleID']
        parametro_http_UUID = request.GET['data']

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_02-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_02-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if (parametro_http_moduleID ==
            'googleDrive' or parametro_http_moduleID == 'oneDrive'):
        response_text, status_code = storeCloudPDS(
            parametro_http_UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc2_05-004: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
    UC3.02
"""


def uc3_02(request):

    def addIdentity(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: AID)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc3_02-AID-001: Error assert session exists or valid')
            return error_text, 401

        cl_session = sessionControl(_UUID)
        cl_auth = Cl_auth()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc3_02-AID-002: sessionId: ', cl_session.sessionID)

        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc3_02-AID-003: Error assert callback response')
            return error_text, 404

        # AMLI
        response = cl_auth.moduleLogin(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc3_02-AID-004: Error parsing moduleLogin json response')
            return error_text, 404

        return '{}&{}'.format(response_address, response_sessionToken), 200

    try:
        parametro_http_moduleID = request.GET['moduleID']
        parametro_http_UUID = request.GET['data']

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc3_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc3_02-002: UUID: ', parametro_http_UUID)
        #     print('DEBUG-uc3_02-003: GET param: ', request.GET)
        #     print('DEBUG-uc3_02-004: POST param: ', request.POST)

    except BaseException:
        return HttpResponse(
            'ModuleID or data not found in the request',
            status=404)

    if ((parametro_http_moduleID == 'eIDAS' or parametro_http_moduleID ==
         'eduGAIN') and (len(parametro_http_UUID) == 32)):
        response_text, status_code = addIdentity(
            parametro_http_UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc3_02-005: Error invalid moduleId = {} or UUID = {}'.format(
                    parametro_http_moduleID,
                    parametro_http_UUID))
        return HttpResponse('ModuleID or data invalid', status=404)


"""
    UC5.01
"""


def uc5_01(request):

    def generation(_UUID, _moduleID, _SSIId):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: LLPDS)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc5_01-GEN-001: Error assert session exists or valid')
            return 'NO_SESSION', 401

        cl_session = sessionControl(_UUID)
        cl_vcissuing = Cl_vcissuing()
        cl_callback = Cl_callback()
        cl_list = Cl_list()

        if (Settings.DEBUG):
            print('DEBUG-uc5_01-GEN-002: sessionId: ', cl_session.sessionID)

        # CLBK
        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc5_01-GEN-003: Error assert callback response')
            return error_text, 404

        vcDefinition_list = cl_list.getCollection('vcDefinitions').json()

        ## Temporal Quick Fix for adding 'eidas-edugain' to the vcDefinitions moduleIDs
        print(vcDefinition_list)
        vcDefinition_list.append({ 'eidas-edugain': {} })
        print(vcDefinition_list)
        ## end TQF

        try:
            assert(vcDefinition_list)
            assert(_moduleID.lower() in [list(vcDefinition.keys())[
                   0] for vcDefinition in vcDefinition_list])

            # filter(lambda person: person['name'] == 'Pam', people)
            #identityA = list(filter(lambda identity: identity['data']['id'] == _datasetId_A, id_list))
            
            _vcDefinition = list(
                filter(
                    lambda vc_Definition: list(
                        vc_Definition.keys())[0] == _moduleID.lower(),
                    vcDefinition_list))
            #_vcDefinition = _vcDefinition[0].get(_moduleID.lower())
            _vcDefinition = _moduleID.lower()  # <<<<< TO-BE-CHECKED <<<<<

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc5_01-GEN-004: Error assert VC Definition list')
            return error_text, 404

        # ## FIX for allowing users to request a VC for identities the have not yet.
        # identities = uc0_02(_UUID)

        # try:
        #     assert(identities)
        #     ## Temporal Quick Fix for adding 'eidas-edugain' to the vcDefinitions moduleIDs
        #     print('_moduleID: ', _moduleID)
        #     if _moduleID == 'eIDAS-eduGAIN':
        #         _moduleID = 'linkedID'
        #         print('identities_unique_prov: ', identities.get('uniqueProviders'))
        #     ## end TQF
        #     assert(_moduleID in identities.get('uniqueProviders'))
        # except BaseException:
        #     if (Settings.DEBUG):
        #         print('DEBUG-uc5_01-GEN-004: Error no identity exists for the module')
        #     return 'NO_IDENTITY', 401
        # ## END FIX


        # TO-DO: WIP
        #       Cambiar parámetros de entrada función generation (quitar _vcDefinition)
        #
        #       1 - Obtener vcDefinitios
        #       2 - Comprobar que exista 1 al menos == al moduleID

        #       3 - Se rescata la lista de identidades de session (MGR/list)
        #       4 - Se comprueba que exista una ID del moduleID seleccionado

        # VCIG
        response = cl_vcissuing.generate(
            cl_session.sessionID, _SSIId, _vcDefinition)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc5_01-GEN-005: Error parsing derivation json response')

            if (response.status_code == 401):
                return 'NO_IDENTITY', 401
            else:
                return error_text, 404

        return '{}&{}'.format(response_address, response_sessionToken), 200

    if (Settings.DEBUG):
        print('uc5_01 INI')

    try:
        parametro_http_moduleID = request.GET['moduleID']
        parametro_http_SSIId = 'uPort'
        parametro_http_UUID = request.GET['data']

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_02-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_02-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if ((parametro_http_moduleID == 'eIDAS' or parametro_http_moduleID ==
         'eduGAIN' or parametro_http_moduleID == 'eMRTD' or parametro_http_moduleID == 'eIDAS-eduGAIN') and (len(parametro_http_UUID) == 32)):
        response_text, status_code = generation(
            parametro_http_UUID, parametro_http_moduleID, parametro_http_SSIId)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc5_01-004: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
    UC6.01
"""


def uc6_01(request):

    def derivation(_UUID, _moduleID):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: LLPDS)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc6_01-DRV-001: Error assert session exists or valid')
            return 'NO_SESSION', 401

        cl_session = sessionControl(_UUID)
        cl_ident = Cl_ident()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc6_01-DRV-002: sessionId: ', cl_session.sessionID)

        # CLBK
        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc6_01-DRV-003: Error assert callback response')
            return error_text, 404

        # IDGE
        response = cl_ident.derivationGenerate(cl_session.sessionID, _moduleID)
        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc6_01-DRV-004: Error parsing derivation json response')

            if (response.status_code == 401):
                return 'NO_IDENTITY', 401
            else:
                return error_text, 404

        return '{}&{}'.format(response_address, response_sessionToken), 200

    if (Settings.DEBUG):
        print('uc6_01 INI')

    try:
        parametro_http_moduleID = request.GET['moduleID']
        parametro_http_UUID = request.GET['data']

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc1_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc1_02-002: GET param: ', request.GET)
        #     print('DEBUG-uc1_02-003: POST param: ', request.POST)

    except BaseException:
        return HttpResponse('ModuleID not found in the request', status=404)

    if (parametro_http_moduleID == 'UUID'):
        response_text, status_code = derivation(
            parametro_http_UUID, parametro_http_moduleID)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc6_01-005: Error invalid moduleId = ',
                parametro_http_moduleID)
        return HttpResponse('ModuleID invalid', status=404)


"""
    UC7.01
"""


def uc7_01(request):

    def identityReconciliation(_UUID, _moduleID, _datasetId_A, _datasetId_B):
        error_text = 'An error has been occured with the API Calls. Please, contact the System Administrador (Error_code: IRE)'

        try:
            assert(sessionExists(_UUID))
            assert(sessionValid(_UUID))
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc7_01-IRE-001: Error assert session exists or valid')
            return error_text, 401

        cl_session = sessionControl(_UUID)
        cl_ident = Cl_ident()
        cl_callback = Cl_callback()

        if (Settings.DEBUG):
            print('DEBUG-uc7_01-IRE-002: sessionId: ', cl_session.sessionID)

        r_callback = cl_callback.callback(
            cl_session.sessionID,
            Settings.Prod.SEAL_ENDPOINT +
            '/tokenValidate=' +
            _UUID)
        try:
            assert(r_callback.status_code == 200)
        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc7_01-IRE-003: Error assert callback response')
            return error_text, 404

        id_list = cl_ident.mgrList(cl_session.sessionID)
        try:
            assert(isinstance(id_list, requests.Response)
                   and id_list.status_code == 200)

            id_list = id_list.json()

            for index in range(0, len(id_list)):
                result_data = json.loads(id_list[index].get('data'))
                id_list[index].update({'data': result_data})

            # filter(lambda person: person['name'] == 'Pam', people)
            identityA = list(filter(lambda identity: unquote(identity['id']) == _datasetId_A, id_list))
            identityB = list(filter(lambda identity: unquote(identity['id']) == _datasetId_B, id_list))

            assert(len(identityA) > 0 and len(identityB) > 0)

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc7_01-MGR-004: Error parsing identities ID json response')
            return error_text, 404

        # ILRQ
        response = cl_ident.linkingRequest(
            cl_session.sessionID,
            _moduleID,
            identityA[0]['id'],
            identityB[0]['id'])

        try:
            response_sessionToken = response.json().get('payload')
            assert(len(response_sessionToken) > len(cl_session.sessionID))

            response_address = response.json().get('access').get('address')
            assert(len(response_address) >
                   0 and response_address[:4] == 'http')

            # It would be useful if the linkID had to be stored
            #response_bodyContent = json.loads(response.json().get('bodyContent'))
            #assert(len(response_bodyContent.get('id')) == len('LINK_' + cl_session.sessionID))

            # _setTemporaryLinkID(_ID, _linkID):

        except BaseException:
            if (Settings.DEBUG):
                print('DEBUG-uc7_01-IRE-005: Error parsing linkingRequest json response')
            return error_text, 404

        return '{}&{}'.format(response_address, response_sessionToken), 200

    try:
        parametro_http_moduleID = request.GET['moduleID']
        parametro_http_UUID = request.GET['data']

        parametro_http_datasetId_A = request.POST['datasetIDa']
        parametro_http_datasetId_B = request.POST['datasetIDb']

        # Uncomment if necessary
        # if (Settings.DEBUG):
        #     print('DEBUG-uc3_02-001: moduleID: ', parametro_http_moduleID)
        #     print('DEBUG-uc3_02-002: UUID: ', parametro_http_UUID)
        #     print('DEBUG-uc3_02-003: GET param: ', request.GET)
        #     print('DEBUG-uc3_02-004: POST param: ', request.POST)

    except BaseException:
        return HttpResponse(
            'ModuleID or data not found in the request',
            status=404)

    if ((parametro_http_moduleID == 'autoSEAL' or parametro_http_moduleID ==
         'manualXYZ') and (len(parametro_http_UUID) == 32)):
        response_text, status_code = identityReconciliation(
            parametro_http_UUID, parametro_http_moduleID, parametro_http_datasetId_A, parametro_http_datasetId_B)
        return HttpResponse(response_text, status=status_code)
    else:
        if (Settings.DEBUG):
            print(
                'ERROR-uc7_01-006: Error invalid moduleId = {} or UUID = {}'.format(
                    parametro_http_moduleID,
                    parametro_http_UUID))
        return HttpResponse('ModuleID or data invalid', status=404)

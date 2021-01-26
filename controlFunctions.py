from django.http import *
from django.core.handlers.wsgi import WSGIRequest
import datetime
import uuid
import jwt
from .utils import api_settings as Settings
from .utils.api import *

# Dictionary with the access_token or ID, and timestamp value for every
# user's session in the system
#request.session = {}

# MAX TIME (in seconds) for a user's session to be valid in the system
SESSION_THRESHOLD = 300


# Return a new type 4 UUID as string (32 char)
def getUUID():
    try:
        return uuid.uuid4().hex
    except BaseException:
        print('ERROR-gU-001: Error generating UUID')
        return 'UUID_ERROR'


# Return a user's session object for a specific ID (UUID)
def _recuperarSession(request, _ID):

    user = request.session.get(_ID, None)
    if (user is not None):
        session =  Cl_session()
        session.sessionID = user.get('session', None)
        return session
    else:
        return None


# Return a newly created user's session, and store it (overwriting) in the
# dictionary user's entry, along with the tiemstamp value (overwriting).
def _crearSession(request, _ID):

    session = Cl_session()

    try:
        session.sessionStart()

        # if(request.session.get(_ID)) del user_sessions.get(_ID).get('session')
        request.session[_ID] = {"session": session.sessionID,
                                "timestamp": datetime.datetime.now().timestamp()}
        return session
    except BaseException:
        print('ERROR-cS-001: Error creating the new session for the ID: {}'.format(_ID))
        return None


# Return the timestamp value for a user ID
def _recuperarTimestamp(request, _ID):
    try:
        return request.session.get(_ID).get('timestamp', None)
    except BaseException:
        return None


# Update the timestamp value for a user ID
def _actualizarTimestamp(request, _ID):
    if (_recuperarTimestamp(request, _ID) is not None):
        request.session.get(_ID).update(
            {"timestamp": datetime.datetime.now().timestamp()})

    return _recuperarTimestamp(request, _ID)


# Create or Update the Flag for a user ID
def _crearTokenFlag(request, _ID, _flag):
    user = request.session.get(_ID, None)

    if (user is not None):
        user.update({'flag': _flag})
        request.session[_ID] = user
        return True
    else:
        if (Settings.DEBUG):
            print('DEBUG-cTF-001: User does not exist for the ID: {}'.format(_ID))
        return False


# Return the Flag for a user ID
def _recuperarTokenFlag(request, _ID):
    try:
        return request.session.get(_ID).get('flag', None)
    except BaseException:
        return None

# Return True if the reset is OK, False otherwise


def _resetearTokenFlag(request, _ID):
    try:
        request.session.get(_ID).update({"flag": None})
        return True
    except BaseException:
        return False


### TO-DO: Verify whether the LinkId has to be stored or not in the users session dictionary.

#def _setTemporaryLinkID(request, _ID, _linkID):
#    try:
#        user = request.session.get(_ID)
#
#        assert(user != None)
#        user.update({'linkID': _linkID})
#        return True
#
#    except:
#        return False
#
#def _getTemporaryLinkID(request, _ID):
#    try:
#        pass
#    except:
#        pass
#
#def _deleteTemporaryLinkID(request, _ID, _linkID):
#    try:
#        pass
#    except:
#        pass
#



def debugGetSessionId(request, UUID):
    """
    Return the sessionId for a valid UUID (debug function, DEBUG=True).
    """

    try:
        assert(Settings.DEBUG)
        return HttpResponse(_recuperarSession(request, UUID).sessionID, status=200)
    except BaseException:
        return HttpResponse(status=404)


"""
    Return user session object if exists, None otherwise
"""


def getSessionId(request, UUID):

    if(sessionExists(request, UUID) and sessionValid(request, UUID)):
        return _recuperarSession(request, UUID)
    else:
        return None


"""
    Return True if a session exists, False otherwise
"""


def sessionExists(request, UUID):
    try:
        assert(_recuperarSession(request, UUID) is not None)
        return True
    except BaseException:
        print('Except session Exist')
        return False

    # return True if _recuperarSession(request, UUID) != None else False


"""
    Return True if a timestamp is valid, False otherwise
"""


def sessionValid(request, UUID):
    try:
        timeStamp = _recuperarTimestamp(request, UUID)
        assert((timeStamp is not None) and (
            (timeStamp + SESSION_THRESHOLD >= datetime.datetime.now().timestamp())))
        return True
    except BaseException:
        print('Except session Valid')
        return False

    # return True if ((timeStamp != None) and ((timeStamp + SESSION_THRESHOLD
    # < datetime.datetime.now().timestamp()))) else False


"""
A high lever function used to control the user's sessions.
- It creates a new session if the given ID does not exist, update an outdated one if possible
or just retrieve the session if it exists and its timestamp is valid.
- The time threshold to validate a user's session is configurable by the SESSION_THRESHOLD
global variable.
- TO-DO: The update option for an outdated session is not implemented yet. Still waiting to
cl/session startSession(sessionID) to be implemented by the APIGatewayClient
"""


def sessionControl(request, _ID):

    if (Settings.DEBUG):
        print('sC INI')

    # Create a new session
    if (_recuperarSession(request, _ID) is None):
        return _crearSession(request, _ID)

    # Update an outdated session
    elif ((_recuperarTimestamp(request, _ID) + SESSION_THRESHOLD < datetime.datetime.now().timestamp())):
        if (Settings.DEBUG):
            print('DEBUG-sC-001: Timestamp outdated')
        return _crearSession(request, _ID)

    # Retrieve a valid session
    else:
        _actualizarTimestamp(request, _ID)
        return _recuperarSession(request, _ID)


"""
A high level function which is used as callback script to control the msToken (with cl/tokenValidate call)
and manage the SessionMngrResponse object that is retrieve from this process.
- It sets an object in the dictionary, associate to the ID (UUID), with the SessionMngrResponse object.
In this object, a code related to the operation final status could be read as follow:
    * An OK code if the operation have been successfully done
    * An ERROR code if the operation have NOT been successfully done
    * A NEW code (future implementation)
- TO-DO: An OK code is always mocked by now, until the development for the SessionMngrResponse object
by the SEAL services backend are implemented
"""


def tokenControl(request, UUID):

    if (Settings.DEBUG):
        print('tC INI')

        try:
            print('DEBUG: UUID: {} - sessionId: {}'.format(UUID,
                                                           _recuperarSession(request, UUID).sessionID))
        except BaseException:
            print('DEBUG_ERROR-tC-001: Error token validation (UUID not found)')

        print('POST: ', request.POST)
        print('GET: ', request.GET)

    if request.POST.get('msToken', None):

        try:
            token = request.POST.get('msToken')
            r = Cl_token().validate(token, _recuperarSession(request, UUID).sessionID)

            assert(r.status_code == 200)
            result = jwt.decode(token, verify=False)

            assert(result.get('sessionId') ==
                   _recuperarSession(request, UUID).sessionID)

            try:

                result_data = json.loads(
                    result.get('data').replace(
                        'null', "\"null\""))
                result.update({'data': result_data})

                if result.get('data').get('code') == 'OK':
                    # Everything's OK!
                    assert(_crearTokenFlag(request, UUID, result))

                elif result.get('data').get('code') == 'ERROR':
                    # Something went wrong...
                    assert(_crearTokenFlag(request, UUID, result))

                else:
                    raise Exception
            except BaseException:
                # Mockup of the result sessionMngrResponse object
                if (Settings.DEBUG):
                    print('DEBUG: Mocking the callback object within msToken')

                # *********************
                result = {
                    'data': {
                        'code': 'OK',
                        'additionalData': 'msToken received, but no data field found. MOCKED!'}}
                # *********************
                assert(_crearTokenFlag(request, UUID, result))

            return HttpResponse(status=200)

        except BaseException:
            print('ERROR-tC-001: Error token validation exception')
            # TO-DO: Return a FAILURE html
            return HttpResponse(status=404)

    else:
        try:
            # Mockup of the result sessionMngrResponse object
            if (Settings.DEBUG):
                print('DEBUG: Mocking the callback object without msToken!')

            # *********************
            result = {
                'data': {
                    'code': 'OK',
                    'additionalData': 'msToken not received. MOCKED!'}}
            # *********************
            assert(_crearTokenFlag(request, UUID, result))

            return HttpResponse(status=200)
        except BaseException:
            print('ERROR-tC-001: Error token validation exception')
            # TO-DO: Return a FAILURE html
            return HttpResponse(status=404)


"""
A high level function which is used for control the callback response status in the dictionary for
a given UUID input parameter.
It checks whether a custom callback URL has been resolved and proceed depends on the result:
- If the custom callback URL has NOT been resolved yet, it returns a NOFLAG status code
- If the custom callback URL has been successfully resolved, it returns an OK status code
- If the custom callback URL has been UNSUCCESSFULLY resolved, it returns an ERROR status code
"""


def tokenFlag(request, UUID):

    flag = _recuperarTokenFlag(request, UUID)

    if (Settings.DEBUG):
        print('tF INI')
        print('DEBUG-tF-001: Flag', flag)

    # The custom callback URL has NOT been resolved yet
    if (flag is None):
        return HttpResponse('NOFLAG', status=206)

    # The custom callback URL has been resolved
    else:
        try:
            # Please DO NOT DELETE (Future implementation of the
            # SessionMngrResponse object flag validation)

            code = flag.get('data').get('code')

            # The custom callback URL has been successfully resolved
            if (code == 'OK'):
                assert(_resetearTokenFlag(request, UUID))
                return HttpResponse('OK', status=200)
            # The custom callback URL has been UNSUCCESSFULLY resolved
            elif (code == 'ERROR'):
                assert(_resetearTokenFlag(request, UUID))
                return HttpResponse('ERROR', status=404)
            # The custom callback URL has been (Future implementation) resolved
            # elif (code == 'NEW'):
            #     return HttpResponse('NEW', status=NNN)
            # An exception is raised due to an undefined status of the custom
            # callback URL result
            else:
                if (Settings.DEBUG):
                    print('ERROR-tF-002: The undefined code is: ', code)
                assert(_resetearTokenFlag(request, UUID))
                raise Exception

            # Mockup of the result sessionMngrResponse object validation
            # *********************
            # assert(flag.get('code') == 'OK')
            # assert(_resetearTokenFlag(request, UUID))
            # return HttpResponse('OK', status=200) #No siempre debe responderse con OK -> cambiar a flag.code
            # *********************

        except BaseException:
            print('ERROR-tF-003: Error validating dictionary token flag')
            return HttpResponse('EXCEPTION_ERROR', status=500)

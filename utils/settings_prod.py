import os

USING_DOCKER = True if (os.environ.get('USING_DOCKER', 'False') == 'True') else False

if not USING_DOCKER:
  from dotenv import load_dotenv
  load_dotenv()

"""Prod Settings global consts"""
SEAL_ENDPOINT = os.environ.get('SEAL_ENDPOINT', '')

USE_PROXY = True if (os.environ.get('USE_PROXY', 'False') == 'True') else False

SEAL_PROXY_HTTP_ENDPOINT = os.environ.get('SEAL_PROXY_HTTP_ENDPOINT', '')
SEAL_PROXY_HTTPS_ENDPOINT = os.environ.get('SEAL_PROXY_HTTPS_ENDPOINT', '')

SEAL_PROXY = {'http': SEAL_PROXY_HTTP_ENDPOINT,
              'https': SEAL_PROXY_HTTPS_ENDPOINT} if (
                 USE_PROXY and (
                   len(SEAL_PROXY_HTTP_ENDPOINT) > 7 and 
                   len(SEAL_PROXY_HTTPS_ENDPOINT) > 7)
                 ) else {}

# We create a format pattern
SEAL_SERVICE_URL = os.environ.get('SEAL_SERVICE_URL', '') + '{}'

# 3 - 3
API_GET_cl_auth_module_login = SEAL_SERVICE_URL.format('/cl/auth/{moduleId}/login?sessionID={sessionId}')
API_GET_cl_auth_module_logout = SEAL_SERVICE_URL.format('/cl/auth/{moduleId}/logout?sessionID={sessionId}')
API_GET_cl_auth_logout = SEAL_SERVICE_URL.format('/cl/auth/logout?sessionID={sessionId}')

# 1 - 4
API_GET_cl_callback = SEAL_SERVICE_URL.format('/cl/callback?ClientCallbackAddr={clientCallbackAddr}&sessionID={sessionId}')

# 1 - 5
API_GET_cl_ident_derivation_module_generate = SEAL_SERVICE_URL.format('/cl/ident/derivation/{moduleId}/generate?sessionID={sessionId}')

# 7 - 12
API_GET_cl_ident_linking_module_request_cancel = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/{requestId}/cancel?sessionID={sessionId}')
API_POST_cl_ident_linking_module_request_files_upload = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/{requestId}/files/upload')
API_POST_cl_ident_linking_module_request_files_upload_02 = '' # TBD <<<<<<< Para pasar el file/formData en el s.post 
API_GET_cl_ident_linking_module_request_messages_receive = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/{requestId}/messages/receive?sessionID={sessionId}')
API_POST_cl_ident_linking_module_request_messages_send = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/{requestId}/messages/send')
API_POST_cl_ident_linking_module_request_messages_send_02 = '' # TBD <<<<<<< Para pasar el file/formData en el s.post 
API_GET_cl_ident_linking_module_request_result = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/{requestId}/result?sessionID={sessionId}')
API_GET_cl_ident_linking_module_request_status = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/{requestId}/status?sessionID={sessionId}')
API_POST_cl_ident_linking_module_request = SEAL_SERVICE_URL.format('/cl/ident/linking/{moduleId}/request?sessionID={sessionId}')
API_POST_cl_ident_linking_module_request_02 = '' # TBD <<<<<<< Para pasar el file/formData en el s.post 

# 4 - 16
API_GET_cl_ident_mgr_dataset_delete = SEAL_SERVICE_URL.format('/cl/ident/mgr/{datasetId}/delete?sessionID={sessionId}')
API_GET_cl_ident_mgr_dataset_refresh = SEAL_SERVICE_URL.format('/cl/ident/mgr/{datasetId}/refresh?sessionID={sessionId}')
API_GET_cl_ident_mgr_dataset_revoke = SEAL_SERVICE_URL.format('/cl/ident/mgr/{datasetId}/revoke?sessionID={sessionId}')
API_GET_cl_ident_mgr_list = SEAL_SERVICE_URL.format('/cl/ident/mgr/list?sessionID={sessionId}')

# 2 - 18
API_POST_cl_ident_source_module_load = SEAL_SERVICE_URL.format('/cl/ident/source/{moduleId}/load?sessionID={sessionId}')
API_GET_cl_ident_source_module_retrieve = SEAL_SERVICE_URL.format('/cl/ident/source/{moduleId}/retrieve?sessionID={sessionId}')

# 1 - 19
API_GET_cl_list_collection = SEAL_SERVICE_URL.format('/cl/list/{collection}')

# 2 - 21
API_GET_cl_persistence_module_load = SEAL_SERVICE_URL.format('/cl/persistence/{moduleId}/load?sessionID={sessionId}')
API_GET_cl_persistence_module_store = SEAL_SERVICE_URL.format('/cl/persistence/{moduleId}/store?sessionID={sessionId}')
API_POST_cl_persistence_per_load_sessionToken = 'http://vm.project-seal.eu:8082/per/load/{sessionToken}?cipherPassword={password}'
API_POST_cl_persistence_per_load = 'http://vm.project-seal.eu:8082/per/load'

# 2 - 23
API_GET_cl_session_end = SEAL_SERVICE_URL.format('/cl/session/end?sessionID={sessionId}')
API_GET_cl_session_start = SEAL_SERVICE_URL.format('/cl/session/start{sessionId}')

# 1 - 24 
API_GET_cl_vc_issuing_module_generate = SEAL_SERVICE_URL.format('/cl/vc/issuing/{SSIId}/generate?sessionID={sessionId}&VCDefinition={vcDefinition}')

#SM
#API_POST_sm_session_data_update = 'http://vm.project-seal.eu:9090/sm/updateSessionData?sessionId={sessionId}'

# 1 - 25
API_GET_cl_token_validate = SEAL_SERVICE_URL.format('/cl/token/validate?msToken={msToken}&sessionID={sessionId}')


# Key-Description dictionary 
GLOBAL_DESCRIPTION_DICT = {
    # 'authsource', 'attrsource'
    "eIDAS": "Electronic IDentification Authentication and Trust Services",
    "eduGAIN": "International Electronic Inter-federation Infrastructure for the R&E Sector",
    # 'attrsource'
    "eMRTD": "Electronic Machine Readable Travel Documents (ePassport, eID-Card)",
    # 'access'
    "PDS": "Personal Data Store",
    "SSI": "Self-Sovereign Identity Wallet",
    # 'persistence'
    "Mobile": "Mobile Local Storage",
    "Browser": "Browser Local Storage", 
    "googleDrive": "Google Drive",
    "oneDrive": "Microsoft OneDrive",
    #"cloudServiceXYZ": "",
}


# GLOBAL_BUTTON_GROUP_DICT = {
#     "PDS": {
#         "local": ,

#     }

# }

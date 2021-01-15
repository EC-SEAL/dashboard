"""Prod Settings global consts"""
SEAL_ENDPOINT = 'https://seal.uma.es/seal'

USE_PROXY = False

SEAL_PROXY_HTTP_ENDPOINT = 'http://jano8.sci.uma.es:3128' #Set here your http proxy endpoint
SEAL_PROXY_HTTPS_ENDPOINT = 'http://jano8.sci.uma.es:3128' #Set here your https proxy endpoint

SEAL_PROXY = {'http': SEAL_PROXY_HTTP_ENDPOINT, 'https': SEAL_PROXY_HTTPS_ENDPOINT} if USE_PROXY and (len(SEAL_PROXY_HTTP_ENDPOINT) > 7 and len(SEAL_PROXY_HTTPS_ENDPOINT) > 7) else {}

# 3 - 3
API_GET_cl_auth_module_login    = 'https://vm.project-seal.eu:9154/cl/auth/{moduleId}/login?sessionID={sessionId}'
API_GET_cl_auth_module_logout   = 'https://vm.project-seal.eu:9154/cl/auth/{moduleId}/logout?sessionID={sessionId}'
API_GET_cl_auth_logout          = 'https://vm.project-seal.eu:9154/cl/auth/logout?sessionID={sessionId}'

# 1 - 4
API_GET_cl_callback             = 'https://vm.project-seal.eu:9154/cl/callback?ClientCallbackAddr={clientCallbackAddr}&sessionID={sessionId}'

# 1 - 5
API_GET_cl_ident_derivation_module_generate     = 'https://vm.project-seal.eu:9154/cl/ident/derivation/{moduleId}/generate?sessionID={sessionId}'

# 7 - 12
API_GET_cl_ident_linking_module_request_cancel           = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/{requestId}/cancel?sessionID={sessionId}'
API_POST_cl_ident_linking_module_request_files_upload    = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/{requestId}/files/upload' 
API_POST_cl_ident_linking_module_request_files_upload_02 = '' # TBD <<<<<<< Para pasar el file/formData en el s.post 
API_GET_cl_ident_linking_module_request_messages_receive = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/{requestId}/messages/receive?sessionID={sessionId}'
API_POST_cl_ident_linking_module_request_messages_send   = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/{requestId}/messages/send'
API_POST_cl_ident_linking_module_request_messages_send_02 = '' # TBD <<<<<<< Para pasar el file/formData en el s.post 
API_GET_cl_ident_linking_module_request_result           = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/{requestId}/result?sessionID={sessionId}'
API_GET_cl_ident_linking_module_request_status           = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/{requestId}/status?sessionID={sessionId}'
API_POST_cl_ident_linking_module_request                 = 'https://vm.project-seal.eu:9154/cl/ident/linking/{moduleId}/request?sessionID={sessionId}'
API_POST_cl_ident_linking_module_request_02              = '' # TBD <<<<<<< Para pasar el file/formData en el s.post 

# 4 - 16
API_GET_cl_ident_mgr_dataset_delete     = 'https://vm.project-seal.eu:9154/cl/ident/mgr/{datasetId}/delete?sessionID={sessionId}'
API_GET_cl_ident_mgr_dataset_refresh    = 'https://vm.project-seal.eu:9154/cl/ident/mgr/{datasetId}/refresh?sessionID={sessionId}'
API_GET_cl_ident_mgr_dataset_revoke     = 'https://vm.project-seal.eu:9154/cl/ident/mgr/{datasetId}/revoke?sessionID={sessionId}'
API_GET_cl_ident_mgr_list               = 'https://vm.project-seal.eu:9154/cl/ident/mgr/list?sessionID={sessionId}'

# 2 - 18
API_POST_cl_ident_source_module_load    = 'https://vm.project-seal.eu:9154/cl/ident/source/{moduleId}/load?sessionID={sessionId}'
API_GET_cl_ident_source_module_retrieve = 'https://vm.project-seal.eu:9154/cl/ident/source/{moduleId}/retrieve?sessionID={sessionId}'

# 1 - 19
API_GET_cl_list_collection      = 'https://vm.project-seal.eu:9154/cl/list/{collection}'

# 2 - 21
API_GET_cl_persistence_module_load  = 'https://vm.project-seal.eu:9154/cl/persistence/{moduleId}/load?sessionID={sessionId}'
API_GET_cl_persistence_module_store = 'https://vm.project-seal.eu:9154/cl/persistence/{moduleId}/store?sessionID={sessionId}' 
API_POST_cl_persistence_per_load_sessionToken = 'http://vm.project-seal.eu:8082/per/load/{sessionToken}?cipherPassword={password}'
API_POST_cl_persistence_per_load = 'http://vm.project-seal.eu:8082/per/load'

# 2 - 23
API_GET_cl_session_end              = 'https://vm.project-seal.eu:9154/cl/session/end?sessionID={sessionId}'
API_GET_cl_session_start            = 'https://vm.project-seal.eu:9154/cl/session/start{sessionId}'

# 1 - 24 
API_GET_cl_vc_issuing_module_generate = 'https://vm.project-seal.eu:9154/cl/vc/issuing/{SSIId}/generate?sessionID={sessionId}&VCDefinition={vcDefinition}'

#SM
#API_POST_sm_session_data_update = 'http://vm.project-seal.eu:9090/sm/updateSessionData?sessionId={sessionId}'

# 1 - 25
API_GET_cl_token_validate             = 'https://vm.project-seal.eu:9154/cl/token/validate?msToken={msToken}&sessionID={sessionId}'


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
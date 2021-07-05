from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views
from . import useCases
from . import controlFunctions

urlpatterns = [
    path('', views.index, name='index'),

    path('logout', views.logout, name='logout'),

    # re_path(r'^tokenFlag=(?P<UUID>[a-z0-9]{32})$', csrf_exempt(controlFunctions.tokenFlag)),
    # re_path(r'^identitymanager/tokenFlag=(?P<UUID>[a-z0-9]{32})$', csrf_exempt(controlFunctions.tokenFlag)),
    re_path(r'^tokenValidate=(?P<UUID>[a-z0-9]{32})$', csrf_exempt(controlFunctions.tokenControl)),

    # path('loadLocalPDS/', csrf_exempt(useCases.uc1_02)),
    # path('loadCloudPDS/', csrf_exempt(useCases.uc1_03)),
    # path('SSI/', csrf_exempt(useCases.uc1_04)),

    #path('identitymanager/', views.identity_manager, name='identity_manager'),

    # path('identitymanager/storeLocalPDS/', csrf_exempt(useCases.uc2_02)),
    # path('identitymanager/storeCloudPDS/', csrf_exempt(useCases.uc2_05)),

    # path('identitymanager/addID/', csrf_exempt(useCases.uc3_02)),

    # path('identitymanager/vcIssue/', csrf_exempt(useCases.uc5_01)),

    # path('identitymanager/idDeriv/', csrf_exempt(useCases.uc6_01)),

    # path('identitymanager/idRecon/', csrf_exempt(useCases.uc7_01)),
    # path('identitymanager/idSelec/', csrf_exempt(useCases.uc0_01)),

    path('manageidentitydata/', views.manageidentity, name='manageidentity'),
    
    #re_path(r'^identitymanager/manageidentitydata=(?P<UUID>[a-z0-9]{32})$', views.manageidentity, name='manageidentity'),

    re_path(r'^testGetSessionId=(?P<UUID>[a-z0-9]{32})$', csrf_exempt(controlFunctions.debugGetSessionId)),
]

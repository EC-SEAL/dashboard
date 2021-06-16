from django.shortcuts import render, redirect
# from django.http import HttpResponseNotFound

from .controlFunctions import *
from .utils.api import *
from .useCases import uc0_02

# Views of the Web Dashboard app.


# def index(request):
#     cl_list = Cl_list()

#     access_methods = cl_list.jsonParser(cl_list.getCollection('access'))

#     return render(request,
#                   'umadashboard/sealdashboard.html',
#                   {'access_methods': access_methods,
#                    'seal_endpoint': Settings.Prod.SEAL_ENDPOINT})

def index(request):

    if not request.get_signed_cookie('UUID', None):

        print('no hay cookie')

        #User has no UUID asigned:
        response = render(request,
                    'umadashboard/index.html',
                    {'seal_endpoint': Settings.Prod.SEAL_ENDPOINT})

        try:
            UUID = getUUID()
            assert(UUID != 'UUID_ERROR')

            cl_session = sessionControl(UUID) 
            assert(cl_session.sessionID != None)

            response.set_signed_cookie('UUID', UUID)

        except:
            print('Exception raised in index view method')
            return render(request, 'umadashboard/not-available.html')

        return response

    else:
        #Uer has UUID but could be outdated
        UUID = request.get_signed_cookie('UUID', None)

        cl_session = sessionControl(UUID)

        identities = uc0_02(UUID)

        if cl_session.sessionID != None and identities != None:
            return render(request,
                    'umadashboard/index.html',
                    {'seal_endpoint': Settings.Prod.SEAL_ENDPOINT,
                    'identities': identities})

        else:
            return render(request, 'umadashboard/not-available.html')
    
def logout(request):
    response = redirect('index')

    if request.get_signed_cookie('UUID', None):
        response.delete_cookie('UUID')
    
    return response

def identity_manager(request):

    # Fetch ssiWWallet variable from the SessionVariables of SEAL service.
    # Pass it to the Django template to generate an Identity Manager with
    # either VCissuer funct., or not.
    ssiWallet = None

    return render(request,
                  'umadashboard/sealidentitymanager.html',
                  {'ssiWallet': ssiWallet,
                   'seal_endpoint': Settings.Prod.SEAL_ENDPOINT})


def manageidentity(request):

    if not request.get_signed_cookie('UUID', None):
        return index(request)

    else:
        #Uer has UUID but could be outdated
        UUID = request.get_signed_cookie('UUID', None)

        if UUID != None:
            identities = uc0_02(UUID)

            if(identities):
                return render(request,
                            'umadashboard/manageidentitydata.html',
                            {'identities': identities})

            else:
                print('Redirecting to index page: UUID_session = {}'.format(UUID))
                return HttpResponseRedirect(Settings.Prod.SEAL_ENDPOINT)

        else:
            return render(request, 'umadashboard/not-available.html')

    

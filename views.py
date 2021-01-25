from django.shortcuts import render
# from django.http import HttpResponseNotFound

from .controlFunctions import *
from .utils.api import *
from .useCases import uc0_02

# Views of the Web Dashboard app.

def index(request):   
    cl_list = Cl_list()

    access_methods = cl_list.jsonParser(cl_list.getCollection('access'))

    return render(request, 'umadashboard/sealdashboard.html', {'access_methods': access_methods, 'seal_endpoint': Settings.Prod.SEAL_ENDPOINT})

def identity_manager(request):

    # Fetch ssiWWallet variable from the SessionVariables of SEAL service.
    # Pass it to the Django template to generate an Identity Manager with either VCissuer funct., or not.
    ssiWallet = None

    return render(request, 'umadashboard/sealidentitymanager.html', {'ssiWallet': ssiWallet, 'seal_endpoint': Settings.Prod.SEAL_ENDPOINT})

def manageidentity(request, UUID):
    identities = uc0_02(UUID)

    if(identities):
        return render(request, 'umadashboard/manageidentitydata.html', {'identities': identities})

    else:
        print('Redirecting to index page: UUID_session = {}'.format(UUID))
        return HttpResponseRedirect(Settings.Prod.SEAL_ENDPOINT)
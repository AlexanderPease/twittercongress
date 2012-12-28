# Views for congress_app
from django.shortcuts import render_to_response #get_object_or_404,
from django.template import Context, RequestContext, loader
from sunlight import congress
from pprint import pprint

def index(request):
    return render_to_response('congress_app/index.html',)
    #return HttpResponseRedirect(reverse('congress_app.results',))

#Should everyone get the same results URL?
def results(request):#, zip_code):
    #Test if zip_code is valid
    districts = congress.districts_for_zip('03840') 
    pprint(districts)
    if len(districts) == 0:
        #Error message
        phoo = 'Error'
    elif len(districts) > 1:
        #Multiple districts in given zip code
        phoo = 'placeholder'
    else:
        district = districts[0]
        representative = congress.legislators(title='Rep', state=district['state'], district=district['number'])[0]
        senators = congress.legislators(title='Sen', state=district['state'])
        legislators = {'representative': representative, 'senator1':senators[0], 'senator2':senators[1]}
        pprint(legislators)
        return render_to_response('congress_app/results.html', {'results': legislators})
     
    legislators = {'representative': 'representative', 'senator1':'senators[0]', 'senator2':'senators[1]'}
    return render_to_response('congress_app/results.html', {'results': legislators})





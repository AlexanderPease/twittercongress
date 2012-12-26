# Views for congress_app
from django.shortcuts import get_object_or_404, render_to_response
from sunlight import congress
from pprint import pprint

def index(request):
    foo = congress.legislators(lastname='Pelosi')[0]
    return render_to_response('congress_app/index.html',)

def results(request):#, zip_code):
    #district = congress.districts.getDistrictsFromZip('01741')
    #senators = congress.legislators.getList(state=district.state, district = district.number)
    senators = congress.legislators(lastname='Pelosi')
    pprint(senators)
    foo = {'town': 'f', 'phone_number': '603-479-0310', 'twitter_id': 'twitter'}
    return render_to_response('congress_app/results.html', {'results': foo})





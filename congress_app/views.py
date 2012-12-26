# Views for congress_app
from django.shortcuts import get_object_or_404, render_to_response
from sunlight import congress

SUNLIGHT_API_KEY = '6beac436fa02439abfe8f27909ab3d8f'

def index(request):
    foo = congress.legislators(lastname='Pelosi')[0]
    return render_to_response('congress_app/index.html',)

def results(request):#, zip_code):
    #district = congress.districts.getDistrictsFromZip('01741')
    #state = district['state']
    
    foo = {'town': 'Greenland, NH', 'phone_number': '603-479-0310'}
    return render_to_response('congress_app/results.html', {'results': foo})





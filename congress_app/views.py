# Views for congress_app
# Django imports
from django.shortcuts import render_to_response #get_object_or_404,
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from congress_app.models import Politician

#Outside imports
import os.path
from sunlight import congress # THIS LIBRARY IS DEPRECATED. CURRENTLY USED FOR REPRESENTATIVES INFO. WILL DIE IN 2015.
from geopy import geocoders
from pprint import pprint
import re #regular expressions
import constants


def index(request):
    Politician.sunlight_to_models()

    zip_code = request.GET.get('zip_code')
    address = request.GET.get('address')

    # Address takes precedence over ZIP code for finding legislators
    # User is only asked for address if ZIP code contains multiple districts
    if address:
        #district = district_for_address(address, request)    
        g = geocoders.GoogleV3()
        place, (lat, lon) = g.geocode(address)
        pprint(place) #support multiple locations
        try:
            print "tried"
            place, (lat, lon) = g.geocode(address)
            pprint(place) #support multiple locations
        except: 
             return render_to_response('index.html', {'error_bad_address': address}, context_instance=RequestContext(request))
        districts = congress.districts_for_lat_lon(lat, lon)
        if len(districts) != 1: 
            pprint('Multiple districts for single geopoint?!') #debug
        else:
            district = districts[0]

    # ZIP code method
    else:
        #district = district_for_zip_code(zip_code, request) 
            # Is there a zip_code arg? If not, return home page
        if not zip_code:
            return render_to_response('index.html', context_instance=RequestContext(request))

        districts = congress.districts_for_zip(zip_code)
        # Test if zip_code is valid
        regex = re.compile('\d{5,5}')
        if not (regex.match(zip_code) and districts):
            return render_to_response('index.html', {'error_zip_code': zip_code}, context_instance=RequestContext(request))
        
        # Test for single congressional district
        if len(districts) > 1:
            pprint(str(len(districts)) + ' DISTRICTS IN ZIP CODE') #debug
            return render_to_response('index.html', {'error_multiple_districts': zip_code}, context_instance=RequestContext(request))
        else: 
            district = districts[0]
        
    
    # Get representatives from district
    representative = congress.legislators(title='Rep', state=district['state'], district=district['number'])[0]
    senators = congress.legislators(title='Sen', state=district['state'])
    legislators = {'representative': representative, 'senator1':senators[0], 'senator2':senators[1]}

    # Check for images for each representative
    image_root = os.path.join(settings.PROJECT_ROOT,'congress_app/static/img/200x250/')
    for legislator in legislators.values():
        # Check using absolute path, pass STATIC_URL path
        image_path = image_root +  legislator.get('bioguide_id') + '.jpg'
        if os.path.isfile(image_path):
            legislator['image'] =  'img/200x250/' + legislator.get('bioguide_id') + '.jpg'
        else:
             legislator['image'] = 'img/200x250/' + 'DEFAULT.jpg'

    # Add in full state name and district
    legislators['state'] = constants.states.get(legislators['representative']['state'])

    return render_to_response('results.html', {'results': legislators}, context_instance=RequestContext(request))

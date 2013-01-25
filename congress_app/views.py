# Views for congress_app
from django.shortcuts import render_to_response #get_object_or_404,
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
import os.path
from sunlight import congress
from pprint import pprint
import re #regular expressions
import constants


def index(request):
    zip_code = request.GET.get('zip_code')
    
    # Is there a zip_code?
    if not zip_code:
        return render_to_response('index.html', context_instance=RequestContext(request))
   
   # Get data from Sunlight module
    districts = congress.districts_for_zip(zip_code)
    
    # Test if zip_code is valid
    regex = re.compile('\d{5,5}')
    if not (regex.match(zip_code) and districts):
         return render_to_response('index.html', {'error_message': zip_code}, context_instance=RequestContext(request))
    
    # Test for single congressional district
    if len(districts) > 1:
        pprint(str(len(districts)) + ' DISTRICTS IN ZIP CODE') #debug
    
    #Pull out three representatives
    district = districts[0]
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
    legislators['state'] = constants.states.get(district['state'])

    return render_to_response('results.html', {'results': legislators}, context_instance=RequestContext(request))

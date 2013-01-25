# Views for congress_app
from django.shortcuts import render_to_response #get_object_or_404,
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
import os.path
from sunlight import congress
from pprint import pprint
import re #regular expressions

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

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
        pass #debug
    
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
    legislators['state'] = states.get(district['state'])

    return render_to_response('results.html', {'results': legislators}, context_instance=RequestContext(request))

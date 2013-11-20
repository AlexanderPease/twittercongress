# Views for congress_app
# Django imports
from django.shortcuts import render_to_response #get_object_or_404,
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from congress_app.models import Politician, Twitter, Twitter_FTV

#Outside imports
import os.path
from sunlight import congress, congress_deprecated
from geopy import geocoders
from pprint import pprint
import re #regular expressions
import twitter # bear/python-twitter


def index(request):
    scratch()


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
        districts = congress_deprecated.districts_for_lat_lon(lat, lon)
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

        districts = congress_deprecated.districts_for_zip(zip_code)
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
        
    
    # Get representatives and pass to results.html
    representative = Politician.objects.get(title='Rep', state=district['state'], district=district['number'])
    senators = Politician.objects.filter(title='Sen', state=district['state'])
    legislators = {'representative': representative, 'senator1':senators[0], 'senator2':senators[1]}
    return render_to_response('results.html', {'results': legislators}, context_instance=RequestContext(request))

def scratch():
    ftv = Twitter_FTV.objects.create(handle="test", politician_id=1)
    # Sunlight
    votes = congress.votes(year=2013, chamber="house", number=7, fields="voter_ids")
    vote = votes[0] # only one vote (b/c only one bill in the query)
    voter_ids = vote['voter_ids']
    print voter_ids['M000485']
    print "-------------"

    # Twitter
    api = twitter.Api(consumer_key='hNxtR1bjU2QnJqQZYftUzA',
                      consumer_secret='nXVHf7tiGzVvfrGA3VRSbdvjIIt1H706tjiP9rK2o4',
                      access_token_key='302134974-AOSt6vdcsgvurVPIuim1uWx3z3wLZlkGjbTQu3p2',
                      access_token_secret='OXi1vlzvrrPESDHhbtT1nFtA0y5vmvG59zQFxL88dyDTd')
    #print api.VerifyCredentials()
    
    #statuses = api.GetUserTimeline()
    #print [s.text for s in statuses]

    #users = api.GetFriends()
    #print [u.name for u in users]

    #status = api.PostUpdate('My first tweet from the command line')
    #print status.text

    #Politician.generate_FTV_twitter()

    api.

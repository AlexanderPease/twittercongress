# Views for congress_app
# Django imports
from django.shortcuts import render_to_response #get_object_or_404,
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from congress_app.models import Politician, Twitter, Twitter_FTV, VotesForm, TweetForm

#Outside imports
import os.path
from sunlight import congress, congress_deprecated
from geopy import geocoders
from pprint import pprint
import re #regular expressions
import twitter # bear/python-twitter

def index(request):
    zip_code = request.GET.get('zip_code')
    address = request.GET.get('address')

    # If no zip code or address argument, then return the basic homepage
    if not zip_code and not address:
        return render_to_response('index.html', context_instance=RequestContext(request))

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

''' Pages for deciding which votes to tweet about '''
#@login_required
def votes(request):
    if request.method == 'POST': # If the form has been submitted...
        form = VotesForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # Sunlight API pukes on null args, so sanitize
            kwargs = {'per_page': 50}
            for k, v in form.cleaned_data.items():
                if v:
                    kwargs[k] = v

            # Query Sunlight API
            votes = congress.votes(**kwargs)

            # Post-query logic
            if not votes:
                error = 'No search results, try again'
                return render_to_response('votes.html', {'error': error, 'form': form}, 
                    context_instance=RequestContext(request))
            if len(votes) > 1:
                message = 'Found %s results, please choose the correct one:' % len(votes)
                # TODO: returns max 50 results on first page. Give option to search further pages
            else:
                message = 'Please confirm that this is the correct vote'
            return render_to_response('votes.html', {'message': message, 'votes': votes}, 
                context_instance=RequestContext(request))
    else:
        form = VotesForm() # An unbound form
        message = 'What shall we tweet about? Search the Congressional Archives'
        return render_to_response('votes.html', {'form': form, 'message': message}, 
            context_instance=RequestContext(request))

''' Handles actual tweeting from Twitter_FTV accounts '''
#@login_required
def tweet(request):
    vote = request.GET # assumes request comes from votes(request)
    reps_account_placeholder = "@[representative's account]"
    choice_placeholder = '[yes/no]'
    tweet_beginning = "%s voted %s on " % (reps_account_placeholder, choice_placeholder)

    if request.method == 'POST': # If the form has been submitted...
        form = TweetForm(request.POST)
        if not form.is_valid():
            error = 'Submitted invalid tweet!'
            return render_to_response('tweet.html', {'error': error, 'tweet_beginning': tweet_beginning, 'vote': vote, 'form':form}, 
                context_instance=RequestContext(request))
        else: 
            # Create base tweet
            tweet_text = form.cleaned_data['text']
            tweet_template = tweet_beginning + tweet_text

            # Get votes for each politician from Sunlight
            kwargs = {'fields': 'voter_ids'}
            for k, v in request.GET.iteritems():
                if v:
                    kwargs[k] = v
            individual_votes = congress.votes(**kwargs)
            if len(individual_votes) != 1:
                print 'Error finding votes'
                return
                #TODO figure out error handling or better transfer method
            individual_votes = individual_votes[0]['voter_ids'] # returns a dict with bioguide_ids for keys

            # Tweet for every applicable politician
            for twitter_ftv in Twitter_FTV.objects.all().exclude(handle="FollowTheVote"):
                p = twitter_ftv.politician
                # Hierarchy of name choosing
                if len(p.brief_name()) <= 16:
                    name = p.brief_name()
                elif p.twitter:
                    name = twitter
                elif len(p.last_name) <= 16:
                    name = p.last_name
                elif p.title == 'sen':
                    name = "Senator"
                else:
                    name = "Representative"

                # Find corresponding vote
                if p.portrait_id in individual_votes:
                    choice = individual_votes[p.portrait_id]
                    if choice == 'Yea':
                        choice = 'YES'
                    elif choice == 'Nay':
                        choice == 'NO'
                    tweet = tweet_template.replace(reps_account_placeholder, name).replace(choice_placeholder, choice)
                    twitter_ftv.tweet(tweet)

            return render_to_response('base.html', {'tweet_beginning': tweet_beginning, 'vote': vote, 'form':form}, 
        context_instance=RequestContext(request))
    else:
        form = TweetForm()
        return render_to_response('tweet.html', {'tweet_beginning': tweet_beginning, 'vote': vote, 'form':form}, 
            context_instance=RequestContext(request))

''' Scratch work '''
@login_required
def scratch(request):
    
    #politician = Politician.objects.create(first_name="test2", last_name="test2", state="TT", district="test", party="T", title="test")
    '''ftv = Twitter_FTV.objects.create(handle="FTV_testaccount", 
                                    politician_id=politician.id, 
                                    email='followthevote+testaccount@gmail.com', 
                                    email_password='ftvtestaccount')
    '''
    

    # Sunlight
    votes = congress.votes(year=2013, chamber="house", number=7, fields="voter_ids")
    vote = votes[0] # only one vote (b/c only one bill in the query)
    voter_ids = vote['voter_ids']
    print voter_ids['M000485']
    print "-------------"

    # Twitter
    '''api = twitter.Api(consumer_key='hNxtR1bjU2QnJqQZYftUzA',
                      consumer_secret='nXVHf7tiGzVvfrGA3VRSbdvjIIt1H706tjiP9rK2o4',
                      access_token_key='302134974-AOSt6vdcsgvurVPIuim1uWx3z3wLZlkGjbTQu3p2',
                      access_token_secret='OXi1vlzvrrPESDHhbtT1nFtA0y5vmvG59zQFxL88dyDTd')
    '''
    #print api.VerifyCredentials()
    
    #statuses = api.GetUserTimeline()
    #print [s.text for s in statuses]

    #users = api.GetFriends()
    #print [u.name for u in users]

    #status = api.PostUpdate('My first tweet from the command line')
    #print status.text

    #Politician.generate_FTV_twitter()
    return render_to_response('base.html', context_instance=RequestContext(request))

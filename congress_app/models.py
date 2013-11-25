from django.db import models
from django.conf import settings #for STATIC_URL
from django import forms
import os
from sunlight import congress
import constants # for full state names
import twitter # bear/python-twitter

class Politician(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    state = models.CharField(max_length=2) # use capitalized state abbreviations (ex: NH)
    district = models.CharField(max_length=100) # number for reps, string for senators' seat (Jr. or Sr.)
    title = models.CharField(max_length=20) # Sen or Rep
    party = models.CharField(max_length=1) # D or R
    portrait_id = models.CharField(max_length=200, blank=True, null=True)
	

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def chamber(self):
        if self.title == 'sen':
            return 'senate'
        elif self.title == 'rep':
            return 'house'
        else:
            raise Exception

    ''' Returns full state name '''
    def full_state_name(self):
        return constants.states.get(self.state)

    ''' Returns full title '''
    def full_title(self):
        if self.title == "Rep":
            return "Representative"
        else:
            return "Senator"

    ''' Returns STATIC_URL path to the portrait file. Defaults to DEFAULT.jpg '''
    def portrait_path(self):
        # Check using absolute path, pass STATIC_URL path
        image_root = os.path.join(settings.PROJECT_ROOT,'congress_app/static/img/200x250/')
        image_path = image_root +  self.portrait_id + '.jpg'
        file_exists = os.path.isfile(image_path)
        if file_exists:
            return 'img/200x250/' + self.portrait_id + '.jpg'
        else: 
            return 'img/200x250/DEFAULT.jpg'

    ''' Adds twitter handle '''
    def add_twitter(self, handle, ftv=False):
        twitter, created_flag = Twitter.objects.get_or_create(handle=handle, politician_id=self.id)
        if created_flag:
            self.twitter = twitter
            self.save()
            print 'Added twitter handle %s to politician %s' % (twitter, self)
       
        # Parse if new twitter handle is owned by me or not
        if ftv:
            twitter.ftv = True
            ftv.save()

    ''' Inits Django Politician models from the Sunlight Congress API '''
    @classmethod
    def sunlight_to_models(cls):
        politicians = congress.legislators(title='Rep')
        politicians = politicians + congress.legislators(title='Sen')
        for politician in politicians:
            new_politician, created_flag = Politician.objects.get_or_create(first_name=politician['firstname'], 
                                                                            last_name=politician['lastname'],
                                                                            state=politician['state'],
                                                                            district=politician['district'],
                                                                            party=politician['party'],
                                                                            title=politician['title'],
                                                                            portrait_id=politician['bioguide_id'])
            if politician['twitter_id']:
                new_politician.add_twitter(politician['twitter_id'])
            else:
                print '%s does not have twitter' % new_politician

    ''' Manually input twitter ids not included in Sunlight '''
    @classmethod
    def extra_twitter_handles(cls):
        TWITTER_EXTRA = [
        ('Grayson', 'AlanGrayson'),
        ('Hastings', 'alceehastings'),
        ('Franken', 'alfranken'),
        ('Long', 'auctnr1'),
        ('Cassidy', 'BillCassidy'),
        ('Schatz', 'brianschatz'),
        ('Murphy', 'ChrisMurphyCT'),
        ('Rohrabacher', 'DanaRohrabacher'),
        ('Davis', 'DannyKDavis'),
        ('Vitter', 'DavidVitter'),
        ('Cummings', 'ElijahECummings'),
        ('Lucas', 'FrankDLucas'),
        ('Garcia', 'JoeGarcia'),
        ('Tester', 'jontester'),
        ('Beatty', 'JoyceBeatty'),
        ('Brownley', 'JuliaBrownley'),
        ('Ayotte', 'KellyAyotte'),
        ('Capuano', 'MikeCapuano'),
        ('Hall', 'RalphHallPress'),
        ('Andrews', 'RepAndrews'),
        ('Cardenas', 'RepCardenas'), #should be an with accent
        ('Guthrie', 'RepGuthrie'),
        ('Sarbanes', 'RepJohnSarbanes'),
        ('Lance', 'RepLanceNJ7'),
        ('Lipinski', 'RepLipinski'),
        ('Pocan', 'repmarkpocan'),
        ('Welch', 'RepPeterWelch'),
        ('Davis', 'RepSusanDavis'),
        ('Baldwin', 'RepTammyBaldwin'),
        ('Thompson', 'RepThompson'),
        ('Holt', 'RushHolt'),
        ('Isakson', 'SenatorIsakson'),
        ('Risch', 'SenatorRisch'),
        ('Gillibrand', 'SenGillibrand'),
        ('Cowan', 'SenMoCowan'),
        ('Scalise', 'SteveScalise'),
        ('Massie', 'ThomasMassieKY'),
        ('Walz', 'Tim_Walz'),
        ('Kaine', 'timkaine'),
        ('Radel', 'treyradel'),
        ]
        for politician in Politician.objects.filter(twitter=None):
            for pair in TWITTER_EXTRA:
                if politician.last_name == pair[0]:
                    politician.add_twitter(pair[1])


    ''' Method to generate FollowTheVote.org twitter handles for each politician. '''
    @classmethod
    def generate_FTV_twitter(cls):
        for politician in Politician.objects.all():
            if politician.title == "Rep":
                twitter_FTV = "FTV_" + politician.title + politician.state +  politician.district + "th" 
                #twitter_FTV = politician.last_name + "_FTV"
            else: 
                twitter_FTV = "FTV_" + politician.state + politician.full_title()
                #twitter_FTV = politician.last_name + "_FTV"
            print "%s %s" % (twitter_FTV, len(twitter_FTV))
            if len(twitter_FTV) > 15:
                raise Exception
       
''' Twitter account of a politician'''
class Twitter(models.Model):
    user_id = models.IntegerField(blank=True, null=True) # Static user id number for the account. NEED TO FILL IN
    handle = models.CharField(max_length=15, blank=True, null=True) # Max length of twitter handle
    politician = models.OneToOneField(Politician, related_name='twitter')

    def __unicode__(self):
        return self.handle


''' Twitter account held by FTV '''
class Twitter_FTV(models.Model):
    user_id = models.IntegerField(blank=True, null=True) # Static user id number for the account. NEED TO FILL IN
    handle = models.CharField(max_length=15, blank=True, null=True) # Max length of twitter handle
    # password for @SenSChumer is Chopin1.618 Make it equal to email_password?
    politician = models.OneToOneField(Politician, related_name='twitter_ftv')

    # OAuth, doesn't expire
    access_key = models.CharField(max_length=50, blank=True, null=True)
    access_secret = models.CharField(max_length=50, blank=True, null=True)

    # Email
    email = models.CharField(max_length=50, blank=True, null=True)
    email_password = models.CharField(max_length=50, blank=True, null=True)
    


    def __unicode__(self):
        return self.handle

    ''' Tweets message from this account '''
    def tweet(self, message):
        try:
            api = twitter.Api(consumer_key='hNxtR1bjU2QnJqQZYftUzA',
                        consumer_secret='nXVHf7tiGzVvfrGA3VRSbdvjIIt1H706tjiP9rK2o4',
                        access_token_key=self.access_key,
                        access_token_secret=self.access_secret)
        except:
            'Failed to authenticate with API'
            print api.VerifyCredentials()
            return 

        try:
            status = api.PostUpdate(message)
            print status.text
        except:
            print 'Failed to post status (tweet)'
            return 

##################################################################################
# Form Models
##################################################################################

''' Used to query Sunlight API about votes '''
class VotesForm(forms.Form): 
    roll_id = forms.CharField(max_length=200, required=False)
    number = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)
    congress = forms.IntegerField(required=False)

    CHAMBERS = (('', '---'), ('senate', 'Senate',), ('house', 'House',))
    chamber = forms.ChoiceField(widget=forms.Select, choices=CHAMBERS, required=False)

    # Fields from Sunlight not currently implemented
    #question = forms.CharField(max_length=300, required=False) # Does this have to be exact match?
    #"voted_at": "2013-01-04T16:22:00Z",
    #"vote_type": "passage". Valid types are "passage", "cloture", "nomination", "impeachment", "treaty", "recommit", "quorum", "leadership", and "other"
    # "roll_type": "On Motion to Suspend the Rules and Pass". The official description of the type of vote. 
    #"required": "2/3",

''' Used to ensure tweet parameters are met '''
class TweetForm(forms.Form): 
    text = forms.CharField(max_length=111, required=True, widget=forms.Textarea)

'''class VotesForm(ModelForm):
    class Meta:
        model = Company
        
        #Is this even being used?
        def __init__(self, *args, **kwargs):
            super(CompanyForm, self).__init__(*args, **kwargs)
            self.fields['date'].widget = widgets.AdminDateWidget()
'''







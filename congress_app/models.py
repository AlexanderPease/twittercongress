from django.db import models
from django.conf import settings #for STATIC_URL
import os
from sunlight import congress # THIS LIBRARY IS DEPRECATED. CURRENTLY USED FOR REPRESENTATIVES INFO. WILL DIE IN 2015.
import constants # full state names

class Politician(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    state = models.CharField(max_length=2) # use capitalized state abbreviations (ex: NH)
    district = models.CharField(max_length=100) # string for senators' seat (Jr. or Sr.)
    title = models.CharField(max_length=20) # Sen or Rep
    party = models.CharField(max_length=1) # D or R
    portrait_id = models.CharField(max_length=200, blank=True, null=True)

    twitter = models.CharField(max_length=15, blank=True, null=True) # Politicians' own twitter ID
    #twitter = models.CharField(max_length=15, blank=True, null=True)
	

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
                new_politician.twitter = politician['twitter_id']
                new_politician.save()
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
        ('Cardenas', 'RepCardenas'), #should be a with accent
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
                    politician.twitter = pair[1]
                    politician.save()

    ''' Method to generate FollowTheVote.org twitter handles for each politician '''
    @classmethod
    def generate_FTV_twitter(cls):
        for politician in Politician.objects.all():
            if politician.title == "Rep":
                twitter_FTV = "FTV_" + politician.title + politician.state +  politician.district + "th" 
            else:
                twitter_FTV = "FTV_" + politician.state + politician.full_title() 
            print "%s %s" % (twitter_FTV, len(twitter_FTV))
            if len(twitter_FTV) > 15:
                raise Exception

            






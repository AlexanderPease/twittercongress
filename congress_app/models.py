from django.db import models
from sunlight import congress # THIS LIBRARY IS DEPRECATED. CURRENTLY USED FOR REPRESENTATIVES INFO. WILL DIE IN 2015.

class Politician(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    twitter = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=2) # use capitalized state abbreviations (ex: NH)
    district = models.CharField(max_length=100) # string for 'Senior Seat'
    title = models.CharField(max_length=20) # Sen or Rep
    party = models.CharField(max_length=1) # D or R
	

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def chamber(self):
        if self.title == 'sen':
            return 'senate'
        elif self.title == 'rep':
            return 'house'
        else:
            raise Exception

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
                                                                            title=politician['title'])
            if politician['twitter_id']:
                new_politician.twitter = politician['twitter_id']
                new_politician.save()
            else:
                print '%s does not have twitter' % new_politician


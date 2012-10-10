'''
Created on Oct 9, 2012

@author: msarullo
'''

class NextAPICollection(object):

    def __init__(self, json):
        self.id = json['id']
        self.name = json['name']
        self.slug = json['slug']
        
    def __str__( self ):
        return "NextAPICollection(id='{}', name='{}', slug='{}')".format(self.id, self.name, self.slug)
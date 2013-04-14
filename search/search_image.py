#!/usr/bin/python

# Imports ###########################################################

import json
import requests
import sys
import urllib


# Globals ###########################################################

FORVO_API_KEY = 'xxx'
BING_API_KEY = 'xxx'

BING_IMAGE_SEARCH_URL = 'https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%27image%27&Query=%27{expression}%27&Market=%27{market}%27&Adult=%27Off%27&$format=json'
FORVO_SEARCH_URL = 'http://apifree.forvo.com/key/{api_key}/format/json/action/word-pronunciations/word/{expression}/language/{language}/'


# Functions #########################################################

# Image search

def get_image_urls(expression, market='en-US'):
    """
    Search Bing Image for images matching expression
    """
    expression_encoded = urllib.quote(expression, '')
    search_url = BING_IMAGE_SEARCH_URL.format(expression=expression_encoded, 
                                              market=market)
    r = requests.get(search_url, auth=(BING_API_KEY, BING_API_KEY))
    assert r.status_code == 200
    results = json.load(r.raw)

    image_urls = [image['MediaUrl'] for image in results['d']['results'][0]['Image']]
    return image_urls

# Sound search

def get_sound_urls(expression, language='pt'):
    """
    Search Forvo for audio files pronouncing expression
    """
    expression_encoded = urllib.quote(expression, '')
    search_url = FORVO_SEARCH_URL.format(api_key=FORVO_API_KEY, 
                                         expression=expression_encoded, 
                                         language=language)
    r = requests.get(search_url)
    assert r.status_code == 200
    results = json.load(r.raw)

    sound_urls = [sound['pathmp3'] for sound in results['items']]
    return sound_urls


# Main ##############################################################

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: search_image.py "expression to search"'
        sys.exit(1)
    
    expression = sys.argv[1]
    print 'Images:', get_image_urls(expression)[:5]
    print 'Pronounciation:', get_sound_urls(expression)[:2]




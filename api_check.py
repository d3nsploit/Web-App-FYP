import requests
import whois
import socket
import json
import hashlib
import urllib.parse
import urllib.request
import urllib
import tldextract
import ipinfo
import pycountry

# function to resolve shorten url
def url_resolve(user_url):
    r = requests.get(user_url)


# function to get url details (main domain,ip,location,date created)
def url_scraper(user_url):
    url = tldextract.extract(user_url)
    domainName = url.domain+'.'+url.suffix
    subUrl = url.subdomain
    statusCode = "404"
    contentLength = 0
    urlIP = "Not Found"
    urlCreated = "Not Found"
    urlCountry = "Not Found"
    try:
        statusCode = requests.get(user_url).status_code
        contentLength = len(requests.get(user_url).content)
        #statusCode = response.status_code
        #contentLength = len(response.content)

        res = whois.whois(user_url)
        #print(res)

        # get ip of url
        if subUrl:
            urlIP = socket.gethostbyname(subUrl+'.'+domainName)
        else:
            urlIP = socket.gethostbyname(domainName)

        # get where url from
        access_token = '8cda8433cb0b8c'
        handler = ipinfo.getHandler(access_token)
        countryCode = handler.getDetails(urlIP).country
        urlCountry = pycountry.countries.get(alpha_2=countryCode).name
    
      # get when url created (if cant print undefined)
        if isinstance(res.creation_date, list):
            urlCreated = res.creation_date[0]
        else:
            urlCreated = res.creation_date
        
        urlCreated = str(urlCreated)
        urlCreated = urlCreated.split()
        urlCreated = urlCreated[0]
        # print(urlCreated)
        # print(res)

    except:
        print("Error")
    return domainName, statusCode, contentLength, urlIP, urlCreated, urlCountry



# function to screenshot webpage b14046
def screenshot(user_url):
    customer_key = ''

    # leave secret phrase empty, if not needed
    secret_phrase = ''

    options = {
        # mandatory parameter
        'url': user_url,

        # all next parameters are optional, see our website screenshot API guide for more details
        'dimension': '600x600',
        'device': 'desktop',
        'cacheLimit': '0',
        'delay': '50',
        'zoom': '100'
    }

    api_url = generate_screenshot_api_url(customer_key, secret_phrase, options)
    return api_url


# function to generate screenshot using api 'b14046'
def generate_screenshot_api_url(customer_key, secret_phrase, options):
    api_url = 'https://api.screenshotmachine.com/?key=' + customer_key

    if secret_phrase:
        api_url = api_url + '&hash=' + \
            hashlib.md5(
                (options.get('url') + secret_phrase).encode('utf-8')).hexdigest()
    api_url = api_url + '&' + urllib.parse.urlencode(options)
    return api_url

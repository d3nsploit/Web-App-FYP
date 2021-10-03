import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs
import ipaddress
import socket
import urllib.request
import re
from urllib.parse import urlparse
import tldextract
from nostril import nonsense
import base64
import ssl


# Check url length (subdomain + domain + tld)
def url_length(extractURL):
   urlLength = len(extractURL.subdomain) + \
      len(extractURL.domain) + len(extractURL.suffix)
   return urlLength


# Check http or https (0 [benign], 1 [malicious])
def ssl_is_Set(urlScheme):
   if urlScheme == 'http':
      return 1
   return 0


# check port number (0 [benign], 1 [malicious])
def port_num(port):
   defaultPort = 80
   if port != None:
      return 1
   return 0


# Check num of special character
def special_char(url):
   specialCharacter = re.sub('[\w]+', '', url)
   return len(specialCharacter)


# Check content type
def content_type(Res):
   split_string = Res.split("/",1)[0]
   if split_string == 'text':
       return 0
   return 1


# Check url is in-form of ip address or not (0 [benign], 1 [malicious])
def ip_address_url(urlNetloc):
   try:
      ipaddress.ip_address(urlNetloc)
      return 1
   except:
      return 0


# Check ranking of url using alexa (0 [benign], 1 [malicious])
def alexa_rank(url):
   try:
      rank = bs(urllib.request.urlopen(
         "http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
      return 0
   except:
      return 1


# Check entrophy of url domain and subdomain
def entrophy(extractURL):
   try:
      if nonsense(extractURL.domain):
         return 1
      if nonsense(extractURL.subdomain):
         return 1
      else:
         return 0
   except:
      try:
         if nonsense(extractURL.subdomain):
            return 1
         else:
            return 0
      except:
         return 0


# Check url redirect or not (0 [benign], 1 [malicious])
def check_redirected(url):
   count = 0
   numRedirect = 0
   responses = requests.get(url, timeout=5)
   for response in responses.history:
      numRedirect += 1
      count = 1
        
   return count, numRedirect


# Count how many URL is redirected
def count_redirected(url):
   numRedirect = 0
   responses = requests.get(url,timeout=5)
   for response in responses.history:
      numRedirect += 1
   return numRedirect


# Check url sensitive word (0 [benign], 1 [malicious])
def sensitive_word(url):
   sensitiveKeyword = ['login', 'log-in', 'register', 'signup', 'sign-up',
                       'signin', 'sign-in', 'banking', 'confirm', 'webscr', 'secure', 'account',
                       'authenticate', 'authentication', 'security', 'wallet']
   if any(word in url for word in sensitiveKeyword):
      return 1
   return 0


# Count js in html content
def count_js(soup):
   return len(soup.find_all("script"))

# Count iframe in html content


def count_iframe(soup):
   return len(soup.find_all("iframe"))



# Retrieve a single page and report the URL and contents
def load_url(url):
    x = url
    old_url = x.strip()

    final_url = requests.get(old_url).url

    url = ""
    if final_url[-1] == "/":
        url = final_url[:-1]

    else:
        url = final_url

    req = urllib.request.Request(
        url,
        headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    )

    Extract_URL = tldextract.extract(url)
    Parse_URL = urlparse(url)
    gcontext = ssl.SSLContext() #disable SSL
    URL_Parse = urllib.request.urlopen(req,context=gcontext)
    contentType = URL_Parse.info().get_content_type()
    webContent = URL_Parse.read()
    soup = bs(webContent, "html.parser",from_encoding="iso-8859-1")
    countRedirected, isRedirected = check_redirected(old_url)
    print(url_length(Extract_URL),ssl_is_Set(Parse_URL.scheme),port_num(Parse_URL.port),special_char(url),content_type(contentType),ip_address_url(Extract_URL.domain),alexa_rank(url),entrophy(Extract_URL),countRedirected,isRedirected,sensitive_word(url),count_js(soup),count_iframe(soup))

    return url_length(Extract_URL),ssl_is_Set(Parse_URL.scheme),port_num(Parse_URL.port),special_char(url),content_type(contentType),ip_address_url(Extract_URL.domain),alexa_rank(url),entrophy(Extract_URL),countRedirected,isRedirected,sensitive_word(url),count_js(soup),count_iframe(soup)


# print(load_url("https://spectrum.um.edu.my"))
# print(get_as_base64("https://api.screenshotmachine.com/?key=b14046&url=https://google.com&dimension=1024x768"))
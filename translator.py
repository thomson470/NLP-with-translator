from __future__ import absolute_import

import sys
import re
from concurrent.futures import ThreadPoolExecutor

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html
    import urllib.request
    import urllib.parse

MAX_TEXT_LENGTH = 5000 # Google membatasi maksimal 5000 karakter per request
BASE_URL = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
HEADERS = {
    "User-Agent": "Mozilla/4.0 (compatible;MSIE 6.0;Windows NT 5.1;SV1;.NET CLR 1.1.4322;.NET CLR 2.0.50727;.NET CLR 3.0.04506.30)"
}

def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html
    return (parser.unescape(text))

def convert(input):
    if (sys.version_info[0] < 3):
        to_translate = urllib.quote_plus(input['to_translate'])
        link = base_link % (input['to_language'], input['from_language'], to_translate)
        request = urllib2.Request(link, headers=HEADERS)
        raw_data = urllib2.urlopen(request).read()
    else:
        to_translate = urllib.parse.quote(input['to_translate'])
        link = BASE_URL % (input['to_language'], input['from_language'], to_translate)
        request = urllib.request.Request(link, headers=HEADERS)
        raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)

def translate(to_translate, to_language="auto", from_language="auto"):
    text = to_translate
    result = ''
    if (len(text) > MAX_TEXT_LENGTH):
        args = []
        while len(text) > MAX_TEXT_LENGTH:
            temp = text[:MAX_TEXT_LENGTH]
            ridx = temp.rindex(' ')
            if ridx != -1:
                text = text[ridx:]
                temp = temp[:ridx]
            else:
                text = text[MAX_TEXT_LENGTH:]
            args.append({'to_translate': temp, 'to_language': to_language, 'from_language': from_language})
        args.append({'to_translate': text, 'to_language': to_language, 'from_language': from_language})
        with ThreadPoolExecutor(3) as executor:
            for words in executor.map(convert, args):
                result += words
    else:
        result = convert({'to_translate': text, 'to_language': to_language, 'from_language': from_language})
    return result

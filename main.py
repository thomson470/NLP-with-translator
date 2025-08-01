from __future__ import absolute_import

import sys
import uvicorn

from fastapi import FastAPI, Request, Depends

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from finvader import finvader

from concurrent.futures import ThreadPoolExecutor
from translator import translate

async def get_json(request: Request) -> bytes:
    return await request.json()

def get_text(data):
    is_translate = 'translate' in data and True == data['translate']
    if not is_translate:
        return data['text']
    return translate(data['text'])

def get_finvader(input):
    value = finvader(input['text'], use_sentibignomics = True, use_henry = True, indicator = input['indicator'])
    return {input['name']: value}

# FastAPI
app = FastAPI()

@app.post('/Translate')
def TranslateEndpoint(request: Request, data = Depends(get_json)):
    text = data['text']
    to_language = 'auto'
    if 'to' in data:
         to_language = data['to']
    from_language = 'auto'
    if 'from' in data:
         from_language = data['from']
    data['result'] = translate(text, to_language, from_language)
    return data

# Vader Standard
@app.post('/VaderStandard')
def VaderStandardEndpoint(request: Request, data = Depends(get_json)):
    text = get_text(data).replace('\n', ' ').lower().strip()
    sia = SIA()
    a = sia.polarity_scores(text)
    data['positive'] = a['pos']
    data['negative'] = a['neg']
    data['neutral'] = a['neu']
    data['compound'] = a['compound']
    return data
    
# Vader Financial
@app.post('/VaderFinancial')
def VaderFinancialEndpoint(request: Request, data = Depends(get_json)):
    text = get_text(data).replace('\n', ' ').lower().strip()
    args = [
        {'name': 'positive', 'text': text, 'indicator': 'pos'},
        {'name': 'negative', 'text': text, 'indicator': 'neg'},
        {'name': 'neutral', 'text': text, 'indicator': 'neu'},
        {'name': 'compound', 'text': text, 'indicator': 'compound'}
    ]
    with ThreadPoolExecutor(4) as executor:
        for map in executor.map(get_finvader, args):
            key = next(iter(map))
            data[key] = map[key]
    return data
    
# NaiveBayes
@app.post('/NaiveBayes')
def NaiveBayesEndpoint(request: Request, data = Depends(get_json)):
    text = get_text(data).replace('\n', ' ').lower().strip()
    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    a = blob.sentiment
    data['positive'] = float("{:.8f}".format(a.p_pos))
    data['negative'] = float("{:.8f}".format(a.p_neg))
    return data
    
# TextBlob
@app.post('/TextBlob')
def TextBlobEndpoint(request: Request, data = Depends(get_json)):
    text = get_text(data).replace('\n', ' ').lower().strip()
    blob = TextBlob(text)
    a = blob.sentiment
    data['polarity'] = float("{:.8f}".format(a.polarity))
    data['subjectivity'] = float("{:.8f}".format(a.subjectivity))
    return data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Invalid arguments')
    port = int(sys.argv[1])
    workers = int(sys.argv[2])
    uvicorn.run('main:app', host='0.0.0.0', port=port, access_log=False, workers=workers, reload=False)

##
# BUILD
# docker build --no-cache -t nlp-with-translator . -f dockerfile
#
# RUN
# docker run -d --name nlp-with-translator -p 5001:80 nlp-with-translator
# 
##
FROM python:3.11.3-alpine
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python -m textblob.download_corpora
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader vader_lexicon
COPY ./main.py /code/
COPY ./translator.py /code/
ENTRYPOINT exec uvicorn main:app --host 0.0.0.0 --port 80 --workers 4 --no-access-log --no-server-header --no-date-header
EXPOSE 80

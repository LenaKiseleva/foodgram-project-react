FROM python:3.8.5

WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code
RUN ls
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0

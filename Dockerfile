FROM python:3.8

#COPY ./requirements.txt /requirements.txt

#RUN pip install -r requirements.txt

RUN pip install pipenv
COPY Pipfile /
RUN pipenv lock
RUN pipenv install  --system --deploy --clear

RUN pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
RUN pip3 install pandas_datareader yfinance

WORKDIR /app

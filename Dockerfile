FROM python:3.8

#COPY ./requirements.txt /requirements.txt

#RUN pip install -r requirements.txt

RUN pip install pipenv
COPY Pipfile /
RUN pipenv lock
RUN pipenv install  --system --deploy --clear


WORKDIR /app

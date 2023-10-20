FROM python:3.11.4-slim-buster

# set work directory
RUN mkdir /app

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY django_backend/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./django_backend .

CMD ["gunicorn", "settings.wsgi:application", "--bind", "0.0.0.0:80"]
#CMD ["sleep", "1000"]
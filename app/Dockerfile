# pull official base image
FROM python:3.8.3

EXPOSE 8000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

#CMD [ "python", "manage.py", "runserver" ]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi"]

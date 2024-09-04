FROM python:3.12

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt


COPY . .

RUN pip install gunicorn

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]
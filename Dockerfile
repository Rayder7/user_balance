FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip3 install pipenv==2022.8.24

RUN pipenv install --ignore-pipfile --system --deploy
COPY src/ .

CMD ["gunicorn", "User_balance.wsgi:application", "--bind", "0:8000"]

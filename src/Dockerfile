FROM python:3.11
RUN pip install pipenv 

WORKDIR /app
COPY Pipfile* ./

RUN pipenv install --deploy --system


COPY . .

CMD ["gunicorn", "User_balance.wsgi:application", "--bind", "0:8000"]
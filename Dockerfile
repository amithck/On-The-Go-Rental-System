FROM python:3.11

ENV PYTHONNUNBUFFERED=1

WORKDIR /code

COPY requirements1.txt .

RUN pip install -r requirements1.txt

COPY . .

EXPOSE 8000

RUN python3.11 manage.py collectstatic

CMD ["python3.11", "manage.py", "runserver"]

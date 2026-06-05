FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements1.txt ./requirements1.txt

RUN pip install -r requirements1.txt

COPY . .

EXPOSE 8000

RUN python3.11 manage.py collectstatic --noinput

CMD ["python3.11", "manage.py", "runserver", "0.0.0.0:8000"]

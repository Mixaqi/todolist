FROM python:3.12

WORKDIR /todoapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY todoapp .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

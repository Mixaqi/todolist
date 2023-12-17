FROM python:3.12

WORKDIR /todoapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY todoapp/manage.py .


CMD ["python", "todoapp/manage.py", "runserver"]

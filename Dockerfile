FROM python:3.10.9
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
RUN pip install pipenv && pipenv install --dev 
COPY ./app ./app
EXPOSE 8000
# CMD ["pipenv", "run" ,"uvicorn","app.main:app","--host" ,"0.0.0.0", "--port", "8000"]


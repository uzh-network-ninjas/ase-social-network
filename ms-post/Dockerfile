FROM python:3.12

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

# Define the default value of the PORT environment variable
ENV PORT 8080

# Use shell form to use the PORT environment variable
# for development only with --reload
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
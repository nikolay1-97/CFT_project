FROM python:3.11.2-alpine

EXPOSE 8000

WORKDIR /test_project

RUN pip install --upgrade pip


RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /test_project

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

CMD ["poetry", "run", "uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /code/
RUN poetry export --without-hashes -f requirements.txt --output ./requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install gunicorn

COPY . /code/

ENTRYPOINT [ "sh", "-c", "./scripts/start.sh" ]
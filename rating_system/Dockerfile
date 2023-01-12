FROM python:3.11-slim as stage0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update ; \
    apt-get install -y --no-install-recommends \
        vim

COPY requirements.txt /python_requirements/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /python_requirements/requirements.txt

ENV ROOT_DIR /app

WORKDIR $ROOT_DIR

COPY rating_system $ROOT_DIR/rating_system
COPY alembic.ini $ROOT_DIR/rating_system/

# ------------ final -----------------------

FROM stage0 as final

CMD ["python3", "-m", "rating_system.main"]
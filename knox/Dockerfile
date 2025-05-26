FROM python:3.12.10-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update --fix-missing && apt install -y --no-install-recommends gcc

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
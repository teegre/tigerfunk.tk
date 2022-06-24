# Dockerfile

FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./tigerfunk tigerfunk
WORKDIR /tigerfunk

EXPOSE 8080

ENTRYPOINT ["python", "tigerfunk/manage.py"]
CMD ["runserver", "0.0.0.0:8080"]

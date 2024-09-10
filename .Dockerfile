FROM python:3.8

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0
RUN mkdir /app

WORKDIR /app/src
COPY ./ /app/src
RUN pip install -r requirement.txt

#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/src/dummy-mles.json

EXPOSE 80
#Run
CMD [ "python", "-u", "server.py"]
FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /fb_nambataxibot
WORKDIR /fb_nambataxibot
ADD . /fb_nambataxibot/
RUN pip install -r requirements.txt
RUN python manage.py migrate
# Server
EXPOSE 8000
# STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

#docker build -t <image> .
#docker run -d -p 8000:8000 <image>

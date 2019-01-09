# fb_chatbot_nambataxi
# Version: 1.0

FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /fb_chatbot_nambataxi
WORKDIR /fb_chatbot_nambataxi
ADD . /fb_chatbot_nambataxi/
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
# Server
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]


# docker build -t qwerty . 
# docker run --name webapp -p 8000:8000 qwerty
# docker rm $(docker ps -a -q -f status=exited)


# fb_chatbot_nambataxi
# Version: 1.0

FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /fb_chatbot_nambataxi
WORKDIR /fb_chatbot_nambataxi
ADD . /fb_chatbot_nambataxi/
RUN pip install -r requirements.txt




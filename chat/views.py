from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json, pprint, requests, random, re
from django.views.generic import View
from . import logic
from .models import Order

FB_ENDPOINT = 'https://graph.facebook.com/v3.2/'
PAGE_ACCESS_TOKEN = "???"
VERIFY_TOKEN = "???"

class bview(generic.View):

    @method_decorator(csrf_exempt) # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax

    def get(self, request, *args, **kwargs):
        hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status_code=403)
        return HttpResponse(hub_challenge)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    fb_user_id = message['sender']['id']
                    fb_user_txt = message['message'].get('text')
                    if fb_user_txt:
                        parse_and_send_fb_message(fb_user_id, fb_user_txt)
                elif 'postback' in message:
                    fb_user_id = message['sender']['id']
                    fb_user_txt = message['postback'].get('payload')
                    if fb_user_txt:
                        parse_and_send_fb_message(fb_user_id, fb_user_txt)
        return HttpResponse("Success", status=200)


def parse_and_send_fb_message(fbid, message):
# Remove all punctuations, lower case the text and split it based on space
#    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    msg = None
# Check the message, and sends back appropriate message
    if message in logic.GOT_MESSAGE_TO_RESPOND:
        msg = logic.BOT_RESPONSE_COMMANDS[message]
# Checking if the sent message was mobile phone (may come up with better logic)
    elif message.startswith('+') and len(message)==13:
        msg = logic.BOT_RESPONSE_COMMANDS['BOT_ASK_FARE']
# Making sure only one model is saved for one FB account
        if len(Order.objects.all().filter(ip_as_id = fbid)) == 1:
            phone_save = Order.objects.get(ip_as_id = fbid)
            phone_save.phone_number = message
            phone_save.save()
        else:
            phone_save = Order(ip_as_id = fbid, phone_number = message)
            phone_save.save()
# Saves the tariff of the order
    elif message in ['standart','big','comf']:
        order = Order.objects.get(ip_as_id = fbid)
        order.tariff = message
        order.save()
        msg = logic.BOT_RESPONSE_COMMANDS['BOT_ASK_ADDRESS']
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
# Saves address (must start with 'адрес', have not found better solution yet
    elif message.startswith('адрес'):
        msg = logic.BOT_RESPONSE_COMMANDS['BOT_MESSAGE_MY_ORDER_STATUS']
        address = Order.objects.get(ip_as_id = fbid)
        address.address = message
        address.save()
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":msg,
        "buttons":[
          {
            "type":"postback",
            "title":"Узнать статус моего заказа",
            "payload":"get_status"
          },
          {
            "type":"postback",
            "title":"Машины рядом",
            "payload":"cars_nearby"
          },
          {
            "type":"postback",
            "title":"Отменить мой заказ",
            "payload":"cancel"
          }]}}}})
# If 'get_status' button is pressed, sends value of status
    elif message == 'get_status':
        msg = Order.objects.get(ip_as_id = fbid).status
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
# Sends cars nearby (haven't developed an algorithm, just for the sake of convenience)
    elif message == 'cars_nearby':
        msg = 4
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
# Changes value of status to "cancelled"
    elif message == 'cancel':
        cancel = Order.objects.get(ip_as_id = fbid)
        msg = 'Заказ был отменён!'
        cancel.status = msg
        cancel.save()
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})

# If there is something to reflect, bot sends message
    if msg is not None:
        endpoint = f"{FB_ENDPOINT}/me/messages?access_token={PAGE_ACCESS_TOKEN}"
# Start message
        if message == 'start':
            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":msg,
        "buttons":[
          {
            "type":"postback",
            "title":"Быстрый заказ такси",
            "payload":"BOT_ASK_PHONE"
          },
          {
            "type":"postback",
            "title":"Тарифы",
            "payload":"tariff"
          }]}}}})
# Sends informations on tariffs
        elif message == 'tariff':
            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
# Asks phone number, after button was clicked
        elif message =='BOT_ASK_PHONE':
            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
# If the message was sent phone number, than sends back 3 buttons with tariffs
        elif message.startswith('+') and len(message)==13:

            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":msg,
        "buttons":[
          {
            "type":"postback",
            "title":"Стандарт",
            "payload":"standart"
          },
          {
            "type":"postback",
            "title":"Минивэн",
            "payload":"big"
          },
          {
            "type":"postback",
            "title":"Комфорт",
            "payload":"comf"
          }]}}}})
        status = requests.post(
            endpoint,
            headers={"Content-Type": "application/json"},
            data=response_msg)
        print(status.json())
        return status.json()
    return None





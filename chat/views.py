from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json, requests
from django.views.generic import View
from . import logic
from .models import Order
from celery import task

VERIFY_TOKEN = ""
FB_ENDPOINT = ""
PAGE_ACCESS_TOKEN = ""
partner_id = 15
server_token = '5ooc6jxnj8kdLXphK43tQk5Eoxo9LEIx'
namba_api_url = 'https://partners.staging.swift.kg/api/v1/'

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

    msg = None

    if message in logic.GOT_MESSAGE_TO_RESPOND:
        msg = logic.BOT_RESPONSE_COMMANDS[message]

    elif message.startswith('+') and len(message)==13:
        msg = logic.BOT_RESPONSE_COMMANDS['BOT_ASK_FARE']
        if len(Order.objects.all().filter(ip_as_id = fbid)) == 1:
            phone_save = Order.objects.get(ip_as_id = fbid)
            phone_save.phone_number = message
            phone_save.save()

        else:
            phone_save = Order(ip_as_id = fbid, phone_number = message)
            phone_save.save()

    elif message in ['standart','big','comf']:


        order = Order.objects.get(ip_as_id = fbid)
        order.tariff = message
        order.save()
        msg = logic.BOT_RESPONSE_COMMANDS['BOT_ASK_ADDRESS']
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})


    elif message.startswith('адрес'):

        address = Order.objects.get(ip_as_id = fbid)
        address.address = message
        address.save()
########## API - CREATING AN ORDER ###############
        order = Order.objects.get(ip_as_id = fbid)
        tariff = order.tariff
        phone_number = order.phone_number
        address = order.address

        if tariff == 'standart':
            tariff_id = 1
        elif tariff == 'big':
            tariff_id = 11
        elif tariff == 'comf':
            tariff_id = 21

        post_data = {
            'partner_id': partner_id,
            'server_token': server_token,
            'phone_number': phone_number,
            'address': address,
            'fare': tariff_id
        }

        response = requests.post(url = "https://partners.staging.swift.kg/api/v1/requests/", data=post_data)
#############################################
        if response.json()['message'] == 'success':
            order.order_id = response.json()['order_id']
            order.save()

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

    elif message == 'get_status':
        msg = Order.objects.get(ip_as_id = fbid).status
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})

    elif message == 'cars_nearby':
########## API - GETTING NUMBER OF CARS NEARBY #############
        address = Order.objects.get(ip_as_id = fbid).address
        post_data = {
            'partner_id':partner_id,
            'server_token':server_token,
            'address': address
        }
        msg = requests.post(url = 'https://partners.staging.swift.kg/api/v1/drivers/nearest/', data=post_data).json()['drivers']
############################################################

        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
    elif message == 'cancel':
########## API - CANCELLING ORDER #############

        post_data = {
            'partner_id':partner_id,
            'server_token':server_token,
        }
        order_id = Order.objects.get(ip_as_id = fbid).order_id
        msg = requests.post(url = 'https://partners.staging.swift.kg/api/v1/requests/{id}/cancel/'.format(order_id), data=post_data).json()['message']
###############################################

        cancel = Order.objects.get(ip_as_id = fbid)
        # msg = 'Заказ был отменён!'
        cancel.status = msg
        cancel.save()
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})

    if msg is not None:
        endpoint = f"{FB_ENDPOINT}/me/messages?access_token={PAGE_ACCESS_TOKEN}"

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

        elif message == 'tariff':
            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
        elif message =='BOT_ASK_PHONE':
            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})

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

@task()
def send_status_update():
    orders = Order.objects.all().filter(status="Ищем водителей")
    for order in range(len(orders)):
        msg = None
        fbid = orders[order].ip_as_id
        post_data = {
            'partner_id':partner_id,
            'server_token':server_token,
        }
        order_id = Order.objects.get(ip_as_id = fbid).order_id
        response = requests.post(url = 'https://partners.staging.swift.kg/api/v1/requests/{id}/'.format(order_id), data=post_data)
        if response['status'] == 'Принят':
            change_status = orders[order]
            change_status.status = "Водитель найден"
            change_status.save()
            msg = "Driver:{}, phone:{}".format(response.json()['driver']['name'],
                                               response.json()['driver']['phone_number'])
            endpoint = f"{FB_ENDPOINT}/me/messages?access_token={PAGE_ACCESS_TOKEN}"
            response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
            status = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                data=response_msg)
            print(status.json())
            return status.json()
    return None

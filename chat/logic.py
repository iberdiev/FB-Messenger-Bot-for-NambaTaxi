GOT_MESSAGE_TO_RESPOND = ['start', 'tariff', 'BOT_ASK_PHONE']

BOT_RESPONSE_COMMANDS = {
'start' : 'Вас приветствует Facebook-бот для вызова NambaTaxi!\n'\
                      'Заказывайте такси с моей помощью:\n'\
                      '1. Вызовите команду "Быстрый заказ такси"\n'\
                      '2. Введите телефон\n'\
                      '3. Выберите тариф\n'\
                      '4. Введите адрес\n'\
                      'Я умный (и продолжаю учиться),\n'\
                      'В процессе обработки заказа,можете узнать статус.\n'\
                      'Приятного использования!\n',
'tariff' :  'Стандарт. Стоимость посадки: 50.' \
            'Стоимость за километр: 12.\n\n' \
            'Минивэн. Стоимость посадки: 100.' \
            'Стоимость за километр: 12.\n\n'\
            'Комфорт. Стоимость посадки: 70. ' \
            'Стоимость за километр: 15.\n\n'\
            'Байк+. Стоимость посадки: 100. ' \
            'Стоимость за километр: 10.\n\n'\
            'Портер. Стоимость посадки: 500. ' \
            'Стоимость за километр: 0.\n\n'\
            'Для получения более подробной информации,\n' \
            'перейдите по ссылке: https://nambataxi.kg/ru/tariffs/',
'BOT_ASK_PHONE' : 'Укажите ваш телефон. Например: +996555112233',
'BOT_ASK_FARE' : "Телефон сохранен. Теперь укажите тариф",
'BOT_ASK_ADDRESS' : "Укажите ваш адрес,например \"Ибраимова, 103\"." \
                  " Куда подать машину?",
'BOT_MESSAGE_MY_ORDER_STATUS' : "Спасибо за ваш заказ. " \
                              "Он находится в обработке.\n"\
                              " Вы можете узнать сколько рядом с вами\n\
машин нажав на кнопку 'Машины рядом'. Совсем скоро водитель возьмет ваш заказ",

#BOT_ORDER_DONE : 'Ваш заказ выполнен! Ваш счет составил {}\n' \
#                 'Спасибо, что воспользовались услугами Намба Такси.\n'\
#                'Телефон Отдела Контроля Качества к вашим услугам:\n '\
#                 '+996 (312) 97-90-60 \n' \
#                 '+996 (701) 97-67-03 \n' \
#                 '+996 (550) 97-60-23`',



#BOT_ORDER_CREATED : "Заказ создан! Номер вашего заказа {}",
#BOT_ORDER_BUTTON_MESSAGE : "Узнайте информацию о вашем заказе ниже",

#BOT_ORDER_CANCEL_BY_OPERATOR : "Извините,заказ был отклонен оператором.\n"\
#                   " Возможно в вашем районе нет машин",
#BOT_ORDER_ACCEPTED : 'Ура! Ваш заказ принят ближайшим водителем!\n' \
#                     'Номер борта: {}\nВодитель: {}\nТелефон: {}\n' \
#                     'Госномер: {}\nМарка машины: {}',
#BOT_DRIVER_LOCATION : 'Текущее местоположение водителя',
#BOT_DRIVER_IN_PLACE : 'Машина на месте',
#BOT_CLIENT_BORT : 'Клиент на борту'
}

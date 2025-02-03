import os
import telebot
from telebot import types
from telebot.types import InputMediaPhoto

ASSETS_PATH = f'{os.getcwd()}/assets'

API_TOKEN = '7042315153:AAGfmwrY094mLYZQsS4_82QFJDRps1IDLVE'  
bot = telebot.TeleBot(API_TOKEN)

def get_asset(name: str):
    return open(f'{ASSETS_PATH}/{name}', 'rb')

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton("Зробити замовлення💧🧽"))
keyboard.add(types.KeyboardButton("Прайс лист📕📄"))
keyboard.add(types.KeyboardButton("Інформація про послуги📝"))
keyboard.add(types.KeyboardButton("Підтримка📞📱"))
keyboard.row(
    types.KeyboardButton("Наш Instagram"),
    types.KeyboardButton("Наш Facebook")
)

order_keyboard = types.InlineKeyboardMarkup()
order_keyboard.add(types.InlineKeyboardButton("Прання килимів🧽💦", callback_data="order_product_1"))
order_keyboard.add(types.InlineKeyboardButton("Хімчистка м'яких меблів🏠", callback_data="order_product_2"))
order_keyboard.add(types.InlineKeyboardButton("Хімчистка матраців🛏", callback_data="order_product_3"))
order_keyboard.add(types.InlineKeyboardButton("Хімчистка дитячих візочків\nта автокрісел 🪑🤱🏻", callback_data="order_product_4"))
order_keyboard.add(types.InlineKeyboardButton("Пральня🫧🧺", callback_data="order_product_10"))

order_keyboard1 = types.InlineKeyboardMarkup()
order_keyboard1.add(types.InlineKeyboardButton("Прання килимів 📕📄",callback_data="price"))
order_keyboard1.add(types.InlineKeyboardButton("Хімчистки м'яких меблів 📕📄",callback_data="price1"))
order_keyboard1.add(types.InlineKeyboardButton("Хімчистки матраців🛏 📕📄",callback_data="price2"))
order_keyboard1.add(types.InlineKeyboardButton("Хімчистки дитячих візочків та автокрісел 📕📄",callback_data="price3"))
order_keyboard1.add(types.InlineKeyboardButton("Пральня 📕📄",callback_data="price4"))

order_keyboard2 = types.InlineKeyboardMarkup()
order_keyboard2.add(types.InlineKeyboardButton("Розрахувати вартість💰💳", callback_data="order_product_5"))
order_keyboard2.add(types.InlineKeyboardButton("Підтвердити замовлення✅", callback_data="confirm_order"))
order_keyboard2.add(types.InlineKeyboardButton("Назад⬅️", callback_data="back"))

order_keyboard3 = types.InlineKeyboardMarkup()
order_keyboard3.add(types.InlineKeyboardButton("Прання килимів🧽💦", callback_data="info1"))
order_keyboard3.add(types.InlineKeyboardButton("Хімчистка меблів🏠", callback_data="info2"))
order_keyboard3.add(types.InlineKeyboardButton("Хімчистка матраців🛏", callback_data="info3"))
order_keyboard3.add(types.InlineKeyboardButton("Хімчистки дитячих візочків та автокрісел🪑🤱🏻", callback_data="info4"))
order_keyboard3.add(types.InlineKeyboardButton("Пральня🫧🧺", callback_data="info5"))

function_keyboard = types.InlineKeyboardMarkup()
function_keyboard.add(types.InlineKeyboardButton("Підтвердити замовлення✅", callback_data="confirm_order"))
function_keyboard.add(types.InlineKeyboardButton("Назад⬅️", callback_data="back"))

price_selection_keyboard = types.InlineKeyboardMarkup()
price_selection_keyboard.add(types.InlineKeyboardButton("Короткий ворс", callback_data="price_85"))
price_selection_keyboard.add(types.InlineKeyboardButton("Довгий ворс, акрилові килими", callback_data="price_95"))
price_selection_keyboard.add(types.InlineKeyboardButton("Назад⬅️", callback_data="back_to_order"))

user_data = {}
admin_chat_id = 5299479931

services_map = {
    "order_product_1": "Замовити прання килима",
    "order_product_2": "Хімчистка м'яких меблів",
    "order_product_3": "Хімчистка матраців",
    "order_product_4": "Хімчистка дитячих візочків та автокрісел",
    "order_product_10": "Пральня"
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    photo = get_asset('1697313260483922.jpg')
    bot.send_photo(message.chat.id, photo,
                   caption=f"Привіт! Я бот-помічник компанії Аква Клін.\n"
                           f"Я допоможу Вам переглянути наші послуги та зробити замовлення. "
                           f"{message.from_user.first_name} {message.from_user.last_name}\n"
                           f"Ваш ID: {message.from_user.id}",
                   parse_mode="HTML", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text == "Прайс лист📕📄":
        bot.send_message(message.chat.id, "Виберіть послугу для замовлення:", reply_markup=order_keyboard1)
    elif message.text == "Зробити замовлення💧🧽":
        bot.send_message(message.chat.id, "Виберіть послугу для замовлення:", reply_markup=order_keyboard)
    elif message.text == "Інформація про послуги📝":
        bot.send_message(message.chat.id, "Ось інформація про наші послуги...",reply_markup=order_keyboard3)
    elif message.text == "Підтримка📞📱":
        bot.send_message(message.chat.id, "Ось контактна інформація для підтримки:\n<b>+380980474746</b>",
                         parse_mode="HTML")
    elif message.text == "Наш Instagram":
        bot.send_message(message.chat.id, "Перейдіть на наш Instagram за посиланням: https://www.instagram.com/akva_klin?igsh=bzg1NzQ3c3JucG92")
    elif message.text == "Наш Facebook":
        bot.send_message(message.chat.id, "Перейдіть на наш Facebook за посиланням: https://www.facebook.com/profile.php?id=100064322940508")
    else:
        if message.from_user.id in user_data and user_data[message.from_user.id].get("step") == "enter_dimensions":
            handle_dimensions(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "info1":
        bot.send_message(call.message.chat.id, 
                         "Спеціалізований цех прання килимів - це сучасна, професійна та автоматизована лінія. "
                         "На кожному етапі дотримання технології контролює кваліфікований оператор. "
                         "Для кожного типу килимового покриття підбирається індивідуальна програма чищення.\n\n"
                         "Килим проходить прання (включаючи видалення плям різного походження), "
                         "промивання, віджимання в центрифузі та сушіння в спеціальній камері. "
                         "Саме тому, погодні умови не впливають на нашу роботу.\n\n"
                         "Ви отримуєте чистий килим, який довгий період зберігає свою свіжість.")
    elif call.data == "info2":
        bot.send_message(call.message.chat.id, 
                         "Хімчистка меблів - це чистка будь-якого типу забруднення, видалення плям, "
                         "включаючи знищення пилових кліщів, шкідливих мікроорганізмів та позбавлення від неприємного запаху.\n\n"
                         "Відмінна якість чищення будь-якої складності, кваліфіковані майстри з великим досвідом роботи та безпечні миючі засоби.\n\n"
                         "Ми повернемо красу та свіжість вашим меблям.")
    elif call.data == "info3":
        bot.send_message(call.message.chat.id, 
                         "Хімчистка матраців - це не лише видалення складних забруднень, плям, але й глибока очистка від алергенів, "
                         "шкідливих мікроорганізмів, що забезпечує здоровий та спокійний сон.\n\n"
                         "Використовуємо лише сертифіковані та безпечні миючі засоби для Вашого здоров'я.\n\n"
                         "Відмінна якість чищення будь-якої складності, кваліфіковані майстри з великим досвідом роботи.")
    elif call.data == "info4":
        bot.send_message(call.message.chat.id, 
                         "Хімчистка колясок, автокрісел - це детальна очистка всіх елементів, включаючи колеса, пластикові та металічні елементи.\n\n"
                         "Делікатне видалення будь-яких забруднень, застарілих плям та неприємних запахів може гарантувати найкращу якість.\n\n"
                         "Технологія очистки не тільки надає свіжості, але й продовжує термін експлуатації.\n\n"
                         "Ви можете бути впевнені, наші засоби для чистки є повністю безпечними для Ваших діток.")
    elif call.data == "info5":
        bot.send_message(call.message.chat.id, 
                         "Наша пральня використовує стандартний метод прання,що поєднує у собі очищення за допомогою води із застосуванням миючих засобів та плямовивідників.Ефективно видаляємо будь-яке забруднення та сушимо за допомогою сучасних сушильних машин.")
    elif call.data == "order_product_10":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Виберіть дію:",
                              reply_markup=order_keyboard2)
    
    if call.data in services_map.keys():
        user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
        user_data[call.from_user.id]['selected_service'] = services_map[call.data]
        
        if call.data == "order_product_1":
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Виберіть дію:",
                                  reply_markup=order_keyboard2)
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Виберіть дію:",
                                  reply_markup=function_keyboard)
    
    elif call.data == "back":
        current_markup = call.message.json['reply_markup']['inline_keyboard']
        if current_markup == order_keyboard:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="Оберіть опцію:", reply_markup=function_keyboard)
        elif current_markup == function_keyboard:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="Виберіть дію:", reply_markup=order_keyboard2)
        elif current_markup == order_keyboard2:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="Виберіть послугу для замовлення:", reply_markup=order_keyboard)
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="Виберіть послугу для замовлення:", reply_markup=order_keyboard)

    if call.data == "order_product_5":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text="Оберіть ціну для розрахунку:", reply_markup=price_selection_keyboard)

    elif call.data == "price_85":
        if call.from_user.id not in user_data:
            user_data[call.from_user.id] = {}
        user_data[call.from_user.id]["price_per_m2"] = 110
        user_data[call.from_user.id]["step"] = "enter_dimensions"
        bot.send_message(chat_id, "Введіть довжину і ширину килима через пробіл (наприклад, 2.5 3.2):")

    elif call.data == "price_95":
        if call.from_user.id not in user_data:
            user_data[call.from_user.id] = {}
        user_data[call.from_user.id]["price_per_m2"] = 110
        user_data[call.from_user.id]["step"] = "enter_dimensions"
        bot.send_message(chat_id, "Введіть довжину і ширину килима через пробіл (наприклад, 2.5 3.2):")

    elif call.data == "back_to_order":
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text="Виберіть дію:", reply_markup=order_keyboard2)

    elif call.data == "confirm_order":
        bot.send_message(chat_id, "Натисніть на кнопку, щоб надати номер телефону",
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                             types.KeyboardButton("Надати номер телефону", request_contact=True)
                         ))
    elif call.data == "price":
        bot.send_photo(chat_id, get_asset('коври.jpg'))
    elif call.data == "price1":
        bot.send_photo(chat_id, get_asset('меблі.jpg'))
    elif call.data == "price2":
        bot.send_photo(chat_id, get_asset('матраси.jpg'))
    elif call.data == "price3":
        bot.send_photo(chat_id, get_asset('коляскі.jpg'))
    elif call.data == "price4":
        try:
            media = [
                InputMediaPhoto(get_asset('MyCollages (1).jpg')),
                InputMediaPhoto(get_asset('MyCollages (2).jpg'))
            ]
            bot.send_media_group(chat_id, media)
        except FileNotFoundError:
            bot.send_message(chat_id, "Один з файлів не знайдено.")

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("step") == "enter_dimensions")
def handle_dimensions(message):
    try:
        length, width = map(float, message.text.split())
        area = round(length * width, 2)  # Округляємо площу до 2 цифр після коми
        price_per_m2 = user_data[message.from_user.id].get("price_per_m2", 110)  # За замовчуванням 110 грн/м²
        price = round(area * price_per_m2, 2)  # Округляємо ціну до 2 цифр після коми
        bot.send_message(message.chat.id, f"Площа килима: {area} кв.м\nЦіна за прання килима: {price} грн\n"
                                          f"Ціна може коливатися залежно від ступеня забруднення, наявності пластиліну, слайму, шерсті тварин.")
        
        user_data[message.from_user.id]["order_info"] = f"Площа килима: {area} кв.м\nЦіна за прання килима: {price} грн"
        
        user_data[message.from_user.id].pop("step", None)  
    except ValueError:
        bot.send_message(message.chat.id, "Неправильний формат введення. Введіть довжину і ширину килима через пробіл (наприклад, 2.5 3.2):")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id
    user_data.setdefault(user_id, {})  
    
    user_data[user_id]["contact"] = message.contact.phone_number
    
    user_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    selected_service = user_data[user_id].get('selected_service', 'Не вибрано')
    admin_message = f"Користувач {user_name}, номер телефону: {message.contact.phone_number}, \nзробив замовлення на послугу: {selected_service}"
    
    bot.send_message(admin_chat_id, admin_message)
    bot.send_message(message.chat.id, "Ви успішно виконали замовлення, чекайте доки з вами зв'яжеться менеджер", reply_markup=keyboard)

if __name__ == '__main__':
    bot.polling(none_stop=True)

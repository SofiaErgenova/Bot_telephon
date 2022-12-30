from telegram import ReplyKeyboardMarkup
from telegram.ext import (ConversationHandler,)
from create import *

# Определяем константы этапов разговора
MENU_FIND, FIND_TEL, FIND_NAME, FIND_SURNAME = range(100, 104)
         

def choise_find(update, _):
    # Список кнопок для ответа  
    reply_keyboard = [['по имени', 'по фамилии', 'по номеру телефона']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Выберете поиск: ',
        reply_markup=markup_key)
    return MENU_FIND

def give_choise_find(update, _):
# Обрабатываем выбор пользователя    
    choise = update.message.text        
    if choise == 'по имени':
        update.message.reply_text('Вы выбрали поиск по имени\n'        
        'Введите имя абонента.\n')
        return FIND_NAME
    elif choise == 'по номеру телефона':
        update.message.reply_text('Вы выбрали поиск по номеру\n'        
        'Введите номер телефона: \n')
        return FIND_TEL
    elif choise == 'по фамилии':
        update.message.reply_text('Вы выбрали поиск по фамилии\n'        
        'Введите фамилию: \n')
        return FIND_SURNAME
    else:        
        return MENU_FIND
    
def search_contact_by_name(update, _):
    """
    Функция осуществляет поиск контакта по имени и выводит на печать строки с совпадениями
    """
    name = update.message.text
    count = 0
    with open('data.csv', 'r', encoding='utf-8') as file:
        found_contact = []
        for line in file:
            if name in line:                
                count = count + 1
                found_contact.append(line.rstrip('\n'))    
    if count == 0:
        update.message.reply_text('Контакт не найден')
    return found_contact 
    
    

def search_contact_by_surname(update, _):

    """
    Функция осуществляет поиск контакта по ФИО и выводит на печать строки с совпадениями
    """
    surname = update.message.text
    count = 0
    found_contact = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        for line in file:
            if surname in line:                
                count = count + 1
                found_contact.append(line.rstrip('\n'))
    if count == 0:
        update.message.reply_text('Контакт не найден')
    return found_contact

def search_contact_by_phone_num(update, _):
    """
    Функция осуществляет поиск контакта по номеру телефона или по имени и выводит на печать строки с совпадениями
    """
    tel_num = update.message.text
    count = 0
    found_contact = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        for line in file:
            if tel_num in line:                
                count = count + 1
                found_contact.append(line.rstrip('\n'))
    if count == 0:
        update.message.reply_text('Контакт не найден')
    return found_contact



# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Отвечаем на отказ
    update.message.reply_text('Приходите как надумаете')
    # Заканчиваем разговор.
    return ConversationHandler.END

def start(update, _):
    update.message.reply_text(
        'Варианты поиска.\n')
    return MENU_FIND


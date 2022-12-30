from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram import Update, ReplyKeyboardMarkup
from config import TOKEN
from typing import List
import csv
MENU = 0
END_UPDATE = 8

def search_contact_return_number_line(data_contact='иванов'):
    '''
    Функция осуществляет поиск контакта по ФИО или по номеру телефона и возвращает номер строки в файле 
    Returns:
    (int)line_number
    '''
    count = 0
    line_number=0
    with open('data.csv', 'r', encoding='utf-8') as file:
        for line in file:            
            if data_contact in line:                
                #print(line)
                count = line_number
                return count
            line_number+=1    
    if count == 0:
        return -1
    return count

def update_function(update: Update, context: CallbackContext):
    '''
    Функция редактирует найденный контакт, заменяя старую строку на новую 
    Returns:
    List[str] - перезаписанный список с отредактированной строкой
    '''
    text = update.message.text
    text = text.split()
    text.pop(0)
    # print(text)
    line_num = int(text[0])
    # print(line_num)
    new_surname = text[1]
    new_name = text[2]
    new_number = text[3]
    new_comment = text[4]
    new_line = f'{new_surname}|{new_name}|{new_number}|{new_comment}'
    # print(new_line)
    # print(type(new_line))
    with open('data.csv', 'r',encoding='UTF8') as file:
        init_list = [] 
        for i in file:
            init_list.append(i.rstrip('\n'))
        # print(init_list)
        # print(type(init_list))
        new_contact_list = []
        for i in range(0, len(init_list)):
            if i != line_num:
                # print(i)
                new_contact_list.append(init_list[i])
            else:
                new_contact_list.append(new_line)
    with open('data.csv', "w", encoding='UTF-8') as data_file:
            for i in range(len(new_contact_list)):
                data_file.write(f'{new_contact_list[i]}\n')
    update.message.reply_text(f'{text} Контакт успешно изменён')

    return MENU

def get_message(update: Update, context: CallbackContext):
    '''
    Функция обрабатывает сообщение пользователя 
    Returns:
    str - строка
    '''
    message = update.message.text
    line_num = search_contact_return_number_line(message)
    print(line_num)
    found_list = []
    new_list = []
    with open('data.csv', 'r', encoding='UTF-8') as r_file:    
        file_reader = csv.reader(r_file, delimiter = '|')   
        for row in file_reader:
            if row != []:
                new_list.append(row) 
    data =  new_list
    print(message)
    for item in data:
        if message.capitalize() in item[0]:
            found_list.append(item)
            update.message.reply_text(f'Контакт для редактирования найден\nID редактируемого контакта:{line_num}\nКонтакт:{found_list}\n'
                                        f'Введите новые данные в формате:\n "/update ID редактируемого контакта Фамилия Имя Телефон Комментарий"')
            return END_UPDATE
    else:
        update.message.reply_text(f'Контакт не найден, введите команду /menu чтобы вернуться к меню')
    return END_UPDATE

def error_message(update, _):
    '''
    Функция печатает ошибку
    '''  
    update.message.reply_text(
        "Ошибка. Попробуйте еще раз")        
    return END_UPDATE

def start_update():
    '''
        Функция запускает редактирование найденного контакта
    '''
    updater = Updater(TOKEN)
    dispetcher = updater.dispatcher

    update_handler = CommandHandler('update', update_function)
    message_handler = MessageHandler(Filters.text, get_message)

    dispetcher.add_handler(update_handler)
    dispetcher.add_handler(message_handler)

    print('Server Started')
    updater.start_polling()
    updater.idle()

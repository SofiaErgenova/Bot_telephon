
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

import logging
from create import *
from new_find import *
from update import *
from config import TOKEN 


# Определяем константы этапов разговора
MENU, ADD, ADD_SECONDNAME, ADD_NAME, ADD_TEL_NUM, ADD_COMMENT,SHOW_CONTACTS, UPDATE, END_UPDATE, DELETE, END_DELETE = range(11)
         

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def cancel(update, _):
   
    user = update.message.from_user
    logger.info("Пользователь %s завершил работу.", user.first_name)
    update.message.reply_text(
        'Работа завершена', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END

# функция обратного вызова точки входа в разговор
def start(update, _):    
    
    update.message.reply_text(
        'Вас приветсвует Бот-справочник.\n'
        'Команда /choise, чтобы перейти к меню.\n'
        'Команда /cancel, чтобы завершить.\n') 
    

def choise(update, _):
    # Список кнопок для ответа  
    reply_keyboard = [['Добавить контакт', 'Найти контакт', 'Изменить контакт', 'Удалить контакт']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Я  - телефонный справочник.\n'
        'Выбери что ты хочешь сделать.'
        'Команда /cancel, чтобы завершить.\n\n'
        'что будем делать?',
        reply_markup=markup_key)
   
    return MENU


def give_choise(update, _):
# Обрабатываем выбор пользователя    
    choise = update.message.text        
    if choise == 'Добавить контакт':
        update.message.reply_text('Вы выбрали Добавить контакт\n'        
        'Введите фамилию абонента.\n')
        return ADD_SECONDNAME
    elif choise == 'Найти контакт':
        # update.message.reply_text('Вы выбрали Найти контакт\n'        
        # 'Выберете поиск: \n')
        return choise_find(update, _)
        # return FIND
    elif choise == 'Изменить контакт':
        update.message.reply_text('Вы выбрали Изменить контакт\nВведите фамилию контакта, который вы хотите изменить', reply_markup=ReplyKeyboardRemove(),)
        return UPDATE
    else:        
        return MENU


if __name__ == '__main__':
    
    updater = Updater(TOKEN)
    
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)      

    choise_handler = ConversationHandler(entry_points=[CommandHandler('choise', choise)],
        states = {MENU:[MessageHandler(Filters.regex('^(Добавить контакт|Найти контакт|Изменить контакт|Удалить контакт)$'), give_choise)],
            ADD_SECONDNAME: [MessageHandler(Filters.text, get_second_name)],
            ADD_NAME: [MessageHandler(Filters.text, get_name)],
            ADD_TEL_NUM: [MessageHandler(Filters.text, get_number)],
            ADD_COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment)],
            MENU_FIND:[MessageHandler(Filters.regex('^(по имени|по фамилии|по номеру телефона)$'), give_choise_find)],
            FIND_NAME: [MessageHandler(Filters.text,search_contact_by_name)],
            FIND_SURNAME: [MessageHandler(Filters.text, search_contact_by_surname)],
            FIND_TEL : [MessageHandler(Filters.text, search_contact_by_phone_num)],
            UPDATE:[MessageHandler(Filters.text & ~Filters.command, get_message),
                CommandHandler('menu', choise),],
            END_UPDATE: [CommandHandler('update', update_function),
                CommandHandler('menu', choise), 
                MessageHandler(Filters.text & ~Filters.command, error_message),], 
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(choise_handler)
   

    print('Работа справочника')
    updater.start_polling()
    updater.idle()


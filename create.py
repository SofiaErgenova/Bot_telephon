from telegram import Update
from telegram.ext import CallbackContext
from config import TOKEN
import csv
import logging
from typing import Optional, List
from telegram.ext import (Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,)



contacet_card = []


def check_name(name, state_success, state_fail, message_success, message_fail, update):
    if len(name) > 40 or not name.isalpha():
        logger.warning("Имя введено неверно. Попробуйте ещё раз:)")
        update.message.reply_text(message_fail)
        return state_fail
    else:
        update.message.reply_text(message_success)
        return state_success


def check_number(input_string: str, state_success, state_fail, update,
                 min_str: Optional[int] = None,
                 max_str: Optional[int] = None):
    try:
        if not input_string.isdigit():
            update.message.reply_text('Не верный формат номера. Попробуйте ввести только цифры')
            return state_fail
        if len(input_string) < min_str:
            update.message.reply_text(f'Не верный формат номера. Введите больше чем {min_str} символов')
            return state_fail
        if len(input_string) > max_str:
            update.message.reply_text(f'Не верный формат номера. Введите меньше, чем {max_str} символов')
            return state_fail

        update.message.reply_text('Введите комментарий к контакту:')
        return state_success
    except ValueError:
        logger.error('Ошибка ввода.Попробуйте еще раз')
        return state_fail


# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
SECONDNAME, NAME, TEL_NUM, COMMENT = range(4)
SECONDNAME, NAME, TEL_NUM, COMMENT = 2,3,4,5

# функция обратного вызова точки входа в разговор
def start(update, _):
    update.message.reply_text(
        'Введите фамилию нового контакта.\n')
    contacet_card.clear()

    return NAME


# Фамилия
def get_second_name(update, _):

    user = update.message.from_user
    second_name = update.message.text
    contacet_card.append(second_name)
    logger.info("Фамилия контакта %s: %s", user.first_name, second_name)
    return check_name(second_name, NAME, SECONDNAME, 'Введите имя контакта', 'Введите еще раз', update)


# Имя
def get_name(update, _):
    user = update.message.from_user
    name = update.message.text
    contacet_card.append(name)
    logger.info("Имя контакта %s: %s", user.first_name, name)
    return check_name(name, TEL_NUM, NAME, 'Введите номер телефона.', 'Введите еще раз', update)



# Номер телефона
def get_number(update, _):
    
    user = update.message.from_user
    phone = update.message.text
    logger.info("Номер телефона %s: %s", user.first_name, phone)
    contacet_card.append(phone)
    return check_number(phone, COMMENT, TEL_NUM, update, 6, 11)


# Комментарий
def comment(update, _):
    
    user = update.message.from_user
    comment = update.message.text
    logger.info("Комментарий ", comment)
    contacet_card.append(comment)
    update.message.reply_text('Контакт записан.')
    logger.info("Комментарий от %s: %s", user.first_name, comment)
    write_csv_file('contacts.csv',  contacet_card)

    # Заканчиваем разговор.
    return 0


def write_csv_file(file_name: str, list_to_write: List[str]):
    """
    Записывает список в файл
    Args:
    file_name - имя файла,
    list_to_write - список для записи
    """
    with open(file_name, 'a', encoding='utf-8') as w_file:

        file_writer = csv.writer(w_file, delimiter="|", lineterminator="\n")
        file_writer.writerow(list_to_write)


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    logger.info("Пользователь %s передумал.", user.first_name)
    # Отвечаем на отказ
    update.message.reply_text('Приходите как надумаете')
    # Заканчиваем разговор.
    return ConversationHandler.END


def add_contact():
    # Определяем обработчик разговоров `ConversationHandler`

    add_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('add', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            SECONDNAME: [MessageHandler(Filters.text, get_second_name)],
            NAME: [MessageHandler(Filters.text, get_name)],
            TEL_NUM: [MessageHandler(Filters.text, get_number)],
            COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(add_handler)


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher
    add_contact()

    updater.start_polling()
    updater.idle()

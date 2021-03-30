from loader import bot
from data.config import admin_id
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import count_items, get_items, get_categories, count_all

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "category", "item_id", "cat_name")
buy_item = CallbackData("buy", "item_id")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="0", item_id="0", cat_name="0", new=False):
    return menu_cd.new(level=level, category=category, cat_name=cat_name, item_id=item_id)

async def main_menu_keyboard(user):
    if user == "customer":
        CURRENT_LEVEL = 40

    markup = InlineKeyboardMarkup()


    markup.row(
        InlineKeyboardButton(
            text="📕 Категории",
            callback_data=make_callback_data(level=0))
    )

    markup.row(
        InlineKeyboardButton(
            text="🗺 Контактные данные",
            callback_data=make_callback_data(level=41))
    )

    markup.row(
        InlineKeyboardButton(
            text="🚚 Доставка",
            callback_data=make_callback_data(level=42))
    )

    return markup

async def contacts_keyboard():

    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=40))
    )

    return markup

# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def categories_keyboard(user):
    # Указываем, что текущий уровень меню - 0, при заходе обычным пользователем
    if user == "customer":
        CURRENT_LEVEL = 0
    # Указываем, что текущий уровень меню - 10, при заходе с редактированием
    elif user == "edit":
        CURRENT_LEVEL = 10
    # Указываем, что текущий уровень меню - 20, при заходе с созданием
    elif user == "new":
        CURRENT_LEVEL = 20
        items = await count_all()
    # Указываем, что текущий уровень меню - 30, при заходе с удалением
    elif user == "del":
        CURRENT_LEVEL = 30
    

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    categories = await get_categories()
    for category in categories:
        # Чекаем в базе сколько товаров существует под данной категорией
        number_of_items = await count_items(category.category_code)

        # Сформируем текст, который будет на кнопке
        button_text = f"{category.category_name} ({number_of_items} шт)"

        if user == "new":
            callback_data = make_callback_data(level=12, category=category.category_code, cat_name=f"{category.category_name}", item_id=items + 1)
        else:
            callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code, cat_name=f"{category.category_name}")

        # Вставляем кнопку в клавиатуру
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    
    if user == "new":
        markup.row(
        InlineKeyboardButton(
            text="Создать категорию",
            callback_data=make_callback_data(level=21))
    )

    if user == "customer":
        markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=40))
    )
    
    # Если меню администратора - добавляем возможность выхода в меню магазина
    if user == "edit" or user == "new":
        markup.row(
        InlineKeyboardButton(
            text="Выход",
            callback_data=make_callback_data(level=0))
    )
    #await bot.send_message(chat_id=admin_id, text=make_callback_data(level=10))
    #await bot.send_message(chat_id=admin_id, text=CURRENT_LEVEL)
    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def items_keyboard(category, user):
    # Указываем, что текущий уровень меню - 2, при заходе обычным пользователем
    if user == "customer":
        CURRENT_LEVEL = 1
    # Указываем, что текущий уровень меню - 12, при заходе с редактированием
    elif user == "edit":
        CURRENT_LEVEL = 11
    elif user == "del":
        CURRENT_LEVEL = 31

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
    markup = InlineKeyboardMarkup(row_width=1)

    # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
    items = await get_items(category)
    for item in items:
        # Сформируем текст, который будет на кнопке
        button_text = f"{item.name} - {item.price}"

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           item_id=item.id)
        markup.row(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
def item_keyboard(category, item_id, user):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Купить",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                item_id=item_id)
        )
    )
    if user == "photo":
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                category=category, cat_name="photo"))
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                category=category))
        )
    return markup


# Создаем функцию, которая отдает клавиатуру панели администратора
async def admin_keyboard():
    CURRENT_LEVEL = 99
    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()
    markup.row(
            InlineKeyboardButton(text="Редактировать товар", callback_data=make_callback_data(level=10))
            #InlineKeyboardButton(text="Добавить товар", callback_data=make_callback_data(level=20))
        )
    markup.row(
            InlineKeyboardButton(text="Добавить товар", callback_data=make_callback_data(level=20))
    )
    markup.row(
            InlineKeyboardButton(text="Удалить товар", callback_data=make_callback_data(level=30))
    )
    markup.row(
            InlineKeyboardButton(text="Редактировать контакты", callback_data=make_callback_data(level=82))
    )
    markup.row(
            InlineKeyboardButton(text="Редактировать доставку", callback_data=make_callback_data(level=83))
    )
    markup.row(
            InlineKeyboardButton(text="Добавить администратора", callback_data=make_callback_data(level=80))
    )
    markup.row(
            InlineKeyboardButton(text="Удалить администратора", callback_data=make_callback_data(level=81))
    )
    markup.row(
        InlineKeyboardButton(
            text="Выход",
            callback_data=make_callback_data(level=0))
    )
    return markup

def item_edit_keyboard(category, item_id, name, price, description, photo):
    # Указываем, что текущий уровень меню - 12
    CURRENT_LEVEL = 12
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=name,
            callback_data=make_callback_data(level=13,
                                             category=category, item_id=item_id)
        )
    )

    markup.row(
        InlineKeyboardButton(
            text=price,
            callback_data=make_callback_data(level=14,
                                             category=category, item_id=item_id)
        )
    )

    markup.row(
        InlineKeyboardButton(
            text=description,
            callback_data=make_callback_data(level=15,
                                             category=category, item_id=item_id)
        )
    )

    markup.row(
        InlineKeyboardButton(
            text=photo,
            callback_data=make_callback_data(level=16,
                                             category=category, item_id=item_id)
        )
    )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category, item_id=item_id))
    )

    markup.row(
        InlineKeyboardButton(
            text="Выход",
            callback_data=make_callback_data(level=0))
    )
    return markup

def delete_question_keyboard(category, item_id):
    CURRENT_LEVEL = 32
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Да",
            callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           item_id=item_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Нет",
            callback_data=make_callback_data(level=99)
        )
    )
    return markup

import asyncio
import aiofiles
import types


class Strings:
    def __init__(self, user_id, first_name=None) -> None:
        self.user_id = user_id
        self.first_name = first_name

    def __getattribute__(self, key: str):
        if result := object.__getattribute__(self, key):
            if isinstance(result, list):
                from bot.services.redis_service import get_user_lang
                user_id = object.__getattribute__(self, "user_id")
                user_lang_code = get_user_lang(user_id)
                return result[user_lang_code]
            else:
                return result
        else:
            return key

    async def read_file(self, file_name):
        file_path = f"bot/resources/string_files/{file_name}"
        async with aiofiles.open(file_path, mode='r') as file:
            content = await file.read()
        return content

    async def message_after_hour(self, hour):
        file_name = f"message_after_{hour}_hour"
        text = await self.read_file(file_name)
        text = text.format(
            first_name = self.first_name
        )
        return text

    hello = "<b>⚡️🇺🇸 Авторский секрет мобильной съемки и монтажа по технологии из США</b>\n\n" \
        "Это единственный известный мне способ зарабатывать неприлично большие деньги " \
            "на динамичной съемке и монтаже, на телефон и без стабилизатора."
    added_group = "Чат успешно добавлена ✅"
    uz_ru = ["UZ 🇺🇿", "RU 🇷🇺"]
    main_menu = ["Asosiy menyu 🏠", "Главное меню 🏠"]
    change_lang = [
        "\U0001F1FA\U0001F1FF Tilni o'zgartirish \U0001F1F7\U0001F1FA",
        "\U0001F1FA\U0001F1FF Сменить язык \U0001F1F7\U0001F1FA",
    ]
    select_lang = [""" Tilni tanlang """, """Выберите язык бота """]
    type_name = ["""Ismingizni kiriting """, """Введите ваше имя """]
    send_number = [
        """Telefon raqamingizni yuboring """,
        """Оставьте свой номер телефона """,
    ]
    leave_number = ["Telefon raqamni yuborish", "Оставить номер телефона"]
    back = ["""🔙 Ortga""", """🔙 Назад"""]
    next_step = ["""Davom etish ➡️""", """Далее ➡️"""]
    seller = ["""Sotuvchi 🛍""", """Продавцам 🛍"""]
    buyer = ["""Xaridor 💵""", """Покупателям 💵"""]
    settings = ["""Sozlamalar ⚙️""", """Настройки ⚙️"""]
    language_change = ["""Tilni o\'zgartirish 🇺🇿🇷🇺""", """Смена языка 🇺🇿🇷🇺"""]
    change_phone_number = [
        """Telefon raqamni o\'zgartirish 📞""",
        """Смена номера телефона 📞""",
    ]
    change_name = ["""Ismni o\'zgartirish 👤""", """Смени имени 👤"""]
    settings_desc = ["""Sozlamalar ⚙️""", """Настройки ⚙️"""]
    your_phone_number = [
        """📌 Sizning telefon raqamingiz: [] 📌""",
        """📌 Ваш номер телефона: [] 📌""",
    ]
    send_new_phone_number = [
        """Yangi telefon raqamingizni yuboring!\n<i>Jarayonni bekor qilish uchun "🔙 Ortga" tugmasini bosing.</i>""",
        """Отправьте свой новый номер телефона!\n<i>Нажмите кнопку "🔙 Назад", чтобы отменить процесс.</i>""",
    ]
    number_is_logged = [
        "Bunday raqam bilan ro'yxatdan o'tilgan, boshqa telefon raqam kiriting",
        "Этот номер уже зарегистрирован. Введите другой номер",
    ]
    changed_your_phone_number = [
        """Sizning telefon raqamingiz muvaffaqiyatli o\'zgartirildi! ♻️""",
        """Ваш номер телефона успешно изменен! ♻️""",
    ]
    your_name = ["""Sizning ismingiz: """, """Ваше имя: """]
    send_new_name = [
        """Ismingizni o'zgartirish uchun, yangi ism kiriting:\n<i>Jarayonni bekor qilish uchun "🔙 Ortga" tugmasini bosing.</i>""",
        """Чтобы изменить свое имя, введите новое:\n<i>Нажмите кнопку "🔙 Назад", чтобы отменить процесс.</i>""",
    ]
    changed_your_name = [
        """Sizning ismingiz muvaffaqiyatli o'zgartirildi!""",
        """Ваше имя успешно изменено!""",
    ]

    view_video = [
        "",
        "СМОТРЕТЬ"
    ]

    choose_payment_method = [
        "",
        "Выберите один из способов оплаты"
    ]

    successful_payment = [
        "",
        "<b>Спасибо за покупку!</b> Я очень ценю, что ты решил инвестировать в свои знания :)\n\n"
        "Материалы будут доступны в закрытом телеграм канала:\n"
        "вот ссылка 👇"
    ]

    join_channel = [
        "",
        "Присоединиться"
    ]

    successfully_joined = [
        "",
        "Вы успешно присоединились к каналу"
    ]

    already_joined = [
        "",
        "У вас уже есть доступ к каналу"
    ]

    open_channel = [
        "",
        "Открыть"
    ]

    view_programm = [
        "",
        "ПОСМОТРЕТЬ ПРОГРАММУ"
    ]

    view_offer = [
        "",
        "СМОТРЕТЬ ОФФЕР"
    ]

    here = [
        "",
        "СЮДЫ"
    ]

    link_to_offer = [
        "",
        "ССЫЛКА НА ОФФЕР"
    ]

    pay = [
        "",
        "Оплатить"
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

    _ = [
        "",
        ""
    ]

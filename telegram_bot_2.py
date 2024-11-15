import logging
import asyncio
import telegram
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import datetime
import time
from db import insert_data_to

load_dotenv()
BOT_TOKEN = f"{os.getenv('BOT_TOKEN')}"
bot = telegram.Bot(token=BOT_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

ASK_NAME_1, ASK_NAME, ASK_BIRTH_YEAR, ASK_EDUCATION, ASK_REGION, ASK_DISTRICT, ASK_PHONE, ASK_PHONE_MANUAL,\
ASK_ADDITIONAL_PHONE, ASK_MARITAL_STATUS, ASK_WORKPLACE, ASK_EXPECTED_SALARY, ASK_EXPECTED_LENGTH, \
ASK_LANGUAGE, ASK_LANGUAGE_LEVEL, ASK_ADDITIONAL_LANGUAGE, ASK_ADDITIONAL_LANGUAGE_LEVEL, \
ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL, ASK_IT_KNOWLEDGE, ASK_SOURCE, CONFIRMATION = range(21)

# Define options for responses
OPTIONS_OF = ["Ҳа", "Йўқ"]
EDUCATION_OPTIONS = ["Ўрта махсус", "Ўрта таълим", "Олий"]
REGION_OPTIONS = ["Тошкент шаҳар", "Андижон вилояти", "Бухоро вилояти", "Жиззах вилояти", "Қашқадарё вилояти", "Навоий вилояти", "Наманган вилояти", "Самарқанд вилояти",
                  "Сурхондарё вилояти", "Сирдарё вилояти", "Тошкент вилояти", "Фарғона вилояти", "Хоразм вилояти", "Қорақалпоғистон Республикаси"]
DISTRICT = {
    "Тошкент шаҳар": [
        "Бектемир тумани", "Миробод тумани", "Мирзо Улуғбек тумани",
        "Сергели тумани", "Учтепа тумани", "Чилонзор тумани",
        "Шайхонтоҳур тумани", "Юнусобод тумани", "Яшнобод тумани",
        "Олмазор тумани", "Яккасарой тумани"
    ],
    "Тошкент вилояти": [
        "Бекобод тумани", "Бўстонлиқ тумани", "Бўка тумани",
        "Зангиота тумани", "Қибрай тумани", "Қуйи Чирчиқ тумани",
        "Паркент тумани", "Пискент тумани", "Тошкент тумани",
        "Ўрта Чирчиқ тумани", "Чиноз тумани", "Юқори Чирчиқ тумани"
    ],
    "Андижон вилояти": [
        "Асақа тумани", "Балиқчи тумани", "Бўз тумани",
        "Булоқбоши тумани", "Жалақудуқ тумани", "Қўрғонтепа тумани",
        "Марҳамат тумани", "Пахтаобод тумани", "Олтинкўл тумани",
        "Хўжаобод тумани", "Шаҳрихон тумани"
    ],
    "Бухоро вилояти": [
        "Олот тумани", "Бухоро тумани", "Вобкент тумани",
        "Ғиждувон тумани", "Қоракўл тумани", "Қаршининг Қуёши",
        "Пешкў тумани", "Ромитан тумани", "Шофиркон тумани",
        "Жондор тумани"
    ],
    "Жиззах вилояти": [
        "Арнасой тумани", "Бахмал тумани", "Ғаллаорол тумани",
        "Дўстлик тумани", "Зарбдор тумани", "Зафаробод тумани",
        "Зомин тумани", "Мирзачўл тумани", "Пахтакор тумани",
        "Фориш тумани", "Янгиқўрғон тумани"
    ],
    "Қашқадарё вилояти": [
        "Ғузор тумани", "Деҳқонобод тумани", "Қарши тумани",
        "Китоб тумани", "Касби тумани", "Қамаши тумани",
        "Муборак тумани", "Миришкор тумани", "Нишон тумани",
        "Чироқчи тумани", "Шаҳрисабз тумани", "Яккабоғ тумани"
    ],
    "Навоий вилояти": [
        "Конимех тумани", "Қармони тумани", "Навбаҳор тумани",
        "Нурота тумани", "Томди тумани", "Учқудуқ тумани",
        "Хатирчи тумани", "Зарафшон тумани"
    ],
    "Наманган вилояти": [
        "Косонсой тумани", "Мингбулоқ тумани", "Норин тумани",
        "Наманган тумани", "Поп тумани", "Тўрақўрғон тумани",
        "Учқўрғон тумани", "Чortoq тумани", "Янгиқўрғон тумани"
    ],
    "Самарқанд вилояти": [
        "Булунғур тумани", "Жомбой тумани", "Иштихон тумани",
        "Каттақўрғон тумани", "Нуробод тумани", "Оқдарё тумани",
        "Пайариқ тумани", "Пастдарғом тумани", "Самарқанд тумани",
        "Тойлоқ тумани", "Ургут тумани"
    ],
    "Сурхондарё вилояти": [
        "Олтинсой тумани", "Ангор тумани", "Бойсун тумани",
        "Денов тумани", "Жарқўрғон тумани", "Қизириқ тумани",
        "Қумқўрғон тумани", "Музработ тумани", "Сариосиё тумани",
        "Термиз тумани", "Узун тумани", "Шўрчи тумани"
    ],
    "Сирдарё вилояти": [
        "Оқолтин тумани", "Бўёвут тумани", "Гулистон тумани",
        "Мирзачўл тумани", "Сайхунобод тумани", "Сардоба тумани",
        "Ховос тумани"
    ],
    "Фарғона вилояти": [
        "Олтиариқ тумани", "Боғдод тумани", "Бешариқ тумани",
        "Бувайда тумани", "Данғара тумани", "Қува тумани",
        "Риштон тумани", "Сўх тумани", "Тошлоқ тумани",
        "Ўзбекистон тумани", "Фарғона тумани", "Фурқат тумани"
    ],
    "Хоразм вилояти": [
        "Боғот тумани", "Гурлан тумани", "Хонқа тумани",
        "Шовот тумани", "Урганч тумани", "Янгибозор тумани",
        "Ҳазорасп тумани", "Қўшкўпир тумани"
    ],
    "Қорақалпоғистон Республикаси": [
        "Амударё тумани", "Беруний тумани", "Қораўзак тумани",
        "Кегейли тумани", "Қўнғирот тумани", "Мўйноқ тумани",
        "Нукус тумани", "Тахтакўпир тумани", "Тахиотош тумани",
        "Хўжайли тумани", "Чимбой тумани", "Шуманай тумани"
    ]
}

PHONE_OPTIONS = [KeyboardButton("📲 Контактимни улашиш", request_contact=True)]
MARRITAL_STATUS_OPTIONS = ["Ёлғиз", "Оилали"]
EXPECTED_SALARY_OPTIONS = ["1,000,000 - 3,000,000 UZS", "3,000,000 - 5,000,000 UZS", "+5,000,000 UZS"]
EXPECTED_LENGTH_OPTIONS = ["1 йилгача", "3 йилгача", "5 йил ва ундан кўпроқ"]
LANGUAGE_OPTIONS = ["Ўзбек", "Рус", "Инглиз", "Бошқа"]
IT_KNOWLEDGE_OPTIONS = ["Билмайман", "Қониқарли", "Яхши", "Профессионал"]
SOURCE_OPTIONS = ["Дўстимдан", "Оила аъзоларимдан", "Ижтимоий тармоқлардан", "Реклама ва эълонлардан", "Бошқа"]

help_text = (
    "Сизга ёрдам бериши мумкин бўлган буйруқлар рўйхати:\n"
    "/start - Ботни ишга тушириш\n"
    "/help - Ботдан ёрдам сўраш\n"
    "Сизга ёрдам беришдан мамнунмиз!"
)

async def handle_update(data):

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']

        if message_text == "/help":
            await bot.send_message(chat_id=chat_id, text=help_text)
        else:
            await bot.send_message(chat_id=chat_id, text="Hello! You sent: " + message_text)
    print("Received data:", data)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(help_text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    if username:
        context.user_data["username"] = f"@{username}"
    else:
        context.user_data["username"] = f"N/A"
    await update.message.reply_text("Жараённи бошлаш учун \"Аризани тўлдириш\" тугмасини босинг.\nАриза ҳолатини текшириш учун \"Аризани қайта кўриб чиқиш\" тугмасини босинг.",
                                    reply_markup=ReplyKeyboardMarkup([["Аризани тўлдириш"],["Аризани қайта кўриб чиқиш"]], resize_keyboard=True, one_time_keyboard=True))
    return ASK_NAME_1

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_input = update.message.text
    if name_input == "Аризани тўлдириш":
        await update.message.reply_text("Тўлиқ исм-шарифингизни киритинг: ")
        return ASK_NAME
    elif name_input == "Аризани қайта кўриб чиқиш":
        await update.message.reply_text(f"{context.user_data}")
        return ASK_NAME_1
    else:
        return ASK_NAME_1


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_2 = update.message.text
    if not name_2.isdigit():
        context.user_data['Name'] = name_2
        await update.message.reply_text("📅 Туғилган санангизни қуйидаги тартибда киритинг: \nНамуна: 29-10-2004")
        return ASK_BIRTH_YEAR
    else:
        await update.message.reply_text("Исм-шарифингизни киритишда хатолик юз берди. Илтимос қайтадан уриниб кўринг❗")
        return ASK_NAME

async def ask_birth_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    year = update.message.text
    if len(year) == 10 and year[:2].isdigit() and year[3:5].isdigit() and year[6:].isdigit() and int(year[6:])<datetime.datetime.now().year and int(year[:2])<32 and int(year[3:6])<13:
        if int(year[3:6]) == 2 and int(year[:2])>29:
            await update.message.reply_text("Туғилган санангизни киритишда хатолик юз берди. Илтимос намунадагидек қилиб, қайта юборинг!\nНамуна: 02-02-2004")
            return ASK_BIRTH_YEAR
        else:
            context.user_data['Birth Year'] = year
            await update.message.reply_text("🎓 Таълим даражангизни танланг: ",
                                            reply_markup=ReplyKeyboardMarkup([EDUCATION_OPTIONS], one_time_keyboard=True))
            return ASK_EDUCATION
    else:
        await update.message.reply_text("Туғилган санангизни киритишда хатолик юз берди. Илтимос намунадагидек қилиб, қайта юборинг!\nНамуна: 02-02-2004")
        return ASK_BIRTH_YEAR

async def ask_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    education = update.message.text
    print(education)
    if education in EDUCATION_OPTIONS:
        context.user_data['Education Level'] = education
        await update.message.reply_text("🌍 Вилоятингизни танланг:", reply_markup=ReplyKeyboardMarkup(keyboard=[REGION_OPTIONS], one_time_keyboard=True, resize_keyboard=True))
        return ASK_REGION
    else:
        await update.message.reply_text("Таълим даражангизни қуйидагилар орасидан танланг! ")
        return ASK_EDUCATION

async def ask_region(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    region = update.message.text
    print(region)
    if region in REGION_OPTIONS:
        context.user_data['Region'] = region
        await update.message.reply_text("🌍 Яшаш туманингизни танланг:",
                                        reply_markup=ReplyKeyboardMarkup(keyboard=[DISTRICT[region]], one_time_keyboard=True, resize_keyboard=True))
        return ASK_DISTRICT
    else:
        await update.message.reply_text("🌍 Вилоятингизни қайта танланг:", reply_markup=ReplyKeyboardMarkup(keyboard=[REGION_OPTIONS], one_time_keyboard=True, resize_keyboard=True))
        return ASK_REGION

async def ask_district(update: Update, context: ContextTypes.DEFAULT_TYPE):
    district = update.message.text
    if district:
        context.user_data['District'] = district
        await update.message.reply_text("📞 Телефон рақамингизни киритинг:",
                                        reply_markup=ReplyKeyboardMarkup([PHONE_OPTIONS], one_time_keyboard=True,
                                        resize_keyboard=True))
        return ASK_PHONE
    else:
        await update.message.reply_text("🌍 Яшаш туманингизни қайта танланг:")
        return ASK_DISTRICT

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    print(phone)
    if phone:
        print(phone)
        context.user_data['Phone Number'] = phone
        await update.message.reply_text("📞 Қўшимча телефон рақамингиз борми ? (Ҳа/Йўқ)",
                                        reply_markup=ReplyKeyboardMarkup([OPTIONS_OF], one_time_keyboard=True, resize_keyboard=True))
        return ASK_ADDITIONAL_PHONE
    else:
        await update.message.reply_text("Қайтадан контакт улашиш тугмасини босинг!")
        return ASK_PHONE


async def manual_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text
    if number.isdigit() and len(number) >= 9:
        context.user_data['Additional Phone Number'] = number
        await update.message.reply_text("💍 Ҳозирги оилавий ҳолатингизни танланг:",
                                        reply_markup=ReplyKeyboardMarkup([MARRITAL_STATUS_OPTIONS],
                                                                         one_time_keyboard=True))
        return ASK_MARITAL_STATUS
    else:
        await update.message.reply_text("Қайтадан телефон рақамингизни намунадагидек юборинг! \n(Намуна: 991234567)")
        return ASK_PHONE_MANUAL

async def ask_additional_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = update.message.text
    if phone == "Ҳа":
        await update.message.reply_text("Қайтадан телефон рақамингизни намунадагидек юборинг! \n(Намуна: 991234567)")
        return ASK_PHONE_MANUAL
    if phone == "Йўқ":
        context.user_data['Additional Phone Number'] = "N/A"
        await update.message.reply_text("💍 Ҳозирги оилавий ҳолатингизни танланг:",
                                        reply_markup=ReplyKeyboardMarkup([MARRITAL_STATUS_OPTIONS],
                                        one_time_keyboard=True))
        return ASK_MARITAL_STATUS
    else:
        return ASK_ADDITIONAL_PHONE

async def ask_marital_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        married = update.message.text
        if married in MARRITAL_STATUS_OPTIONS:
            context.user_data['Marital Status'] = married
            await update.message.reply_text("Охирги иш жойингиз қаерлиги ҳақида маълумот беринг:")
            return ASK_WORKPLACE
        else:
            return ASK_MARITAL_STATUS

async def ask_workplace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    workplace = update.message.text
    if not workplace.isdigit():
        context.user_data['Previous Workplace'] = workplace
        await update.message.reply_text("💰 Қанча маош кутмоқдасиз ?", reply_markup=ReplyKeyboardMarkup([EXPECTED_SALARY_OPTIONS], one_time_keyboard=True))
        return ASK_EXPECTED_SALARY
    else:
        await update.message.reply_text("Охирги иш жойингиз ҳақида маълумотларни илтимос қайтадан киритинг:")
        return ASK_WORKPLACE

async def ask_expected_salary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    salary = update.message.text
    if salary in EXPECTED_SALARY_OPTIONS:
        context.user_data['Expected Salary'] = salary
        await update.message.reply_text("⏳ Биз билан қанча муддат давомида бирга ишлай оласиз?", reply_markup=ReplyKeyboardMarkup([EXPECTED_LENGTH_OPTIONS], one_time_keyboard=True))
        return ASK_EXPECTED_LENGTH
    else:
        await update.message.reply_text("Қанча маош кутмоқдасиз ?")
        return ASK_EXPECTED_SALARY

async def ask_expected_length(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    length = update.message.text
    if length in EXPECTED_LENGTH_OPTIONS:
        context.user_data['Expected Length'] = length
        await update.message.reply_text("🗣 Қайси тилларни биласиз?", reply_markup=ReplyKeyboardMarkup([LANGUAGE_OPTIONS], one_time_keyboard=True, resize_keyboard=True))
        return ASK_LANGUAGE
    else:
        await update.message.reply_text("Биз билан қанча муддат давомида бирга ишлай оласиз?")
        return ASK_EXPECTED_LENGTH


async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = update.message.text
    if language in LANGUAGE_OPTIONS:
        context.user_data['Language'] = language
        await update.message.reply_text("🌍 Тил билиш даражангизни кўрсатинг:", reply_markup=ReplyKeyboardMarkup([["Бошланғич", "Ўрта", "Юқори", "Она тилим"]], one_time_keyboard=True, resize_keyboard=True))
        return ASK_LANGUAGE_LEVEL
    else:
        await update.message.reply_text("Қайси тилларни биласиз?")
        return ASK_LANGUAGE

async def ask_language_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language_level = update.message.text
    if language_level in ["Бошланғич", "Ўрта", "Юқори", "Она тилим"]:
        context.user_data['Language Level'] = language_level
        await update.message.reply_text(
            "🌍 Қўшимча бошқа тилни ҳам биласизми? (Ҳа/Йўқ)",
            reply_markup=ReplyKeyboardMarkup([OPTIONS_OF], one_time_keyboard=True)
        )
        return ASK_ADDITIONAL_LANGUAGE
    else:
        await update.message.reply_text("Тил билиш даражангизни кўрсатинг:")
        return ASK_LANGUAGE_LEVEL

async def ask_additional_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer == "Ҳа":
        await update.message.reply_text("🌍 Қуйидагилар орасидан биладиган тилингизни танланг:", reply_markup=ReplyKeyboardMarkup([LANGUAGE_OPTIONS], one_time_keyboard=True, resize_keyboard=True))
        return ASK_ADDITIONAL_LANGUAGE_LEVEL
    elif update.message.text == "Йўқ":
        context.user_data['Additional Language'] = "N/A"
        context.user_data['Additional Language Level'] = "N/A"
        await update.message.reply_text(
            "💻 Компьютер саводхонлик даражангизни қуйидагилар орасидан танланг:",
            reply_markup=ReplyKeyboardMarkup([IT_KNOWLEDGE_OPTIONS], one_time_keyboard=True, resize_keyboard=True)
        )
        return ASK_IT_KNOWLEDGE
    else:
        await update.message.reply_text("Илтимос \"Ҳа\" ёки \"Йўқ\" тугмаларидан бирини танланг:")
        return ASK_ADDITIONAL_LANGUAGE

async def ask_additional_language_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    additional_language = update.message.text
    if additional_language in LANGUAGE_OPTIONS:
        context.user_data['Additional Language'] = additional_language
        await update.message.reply_text(f"{additional_language} тилини биладиган даражангизни кўрсатинг:!", reply_markup=ReplyKeyboardMarkup([["Бошланғич", "Ўрта", "Юқори", "Она тилим"]],
                                                                                            resize_keyboard=True,one_time_keyboard=True))
        return ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL
    else:
        await update.message.reply_text("Илтимос тил билиш даражангизни қайтадан танланг:")
        return ASK_ADDITIONAL_LANGUAGE_LEVEL

async def ask_additional_language_level_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    additional_language_level = update.message.text
    if additional_language_level in ["Бошланғич", "Ўрта", "Юқори", "Она тилим"]:
        context.user_data['Additional Language Level'] = additional_language_level
        await update.message.reply_text(
            "💻 Компьютер саводхонлик даражангизни қуйидагилар орасидан танланг:",
            reply_markup=ReplyKeyboardMarkup([IT_KNOWLEDGE_OPTIONS], one_time_keyboard=True,resize_keyboard=True))
        return ASK_IT_KNOWLEDGE
    else:
        await update.message.reply_text("What is your level of knowledge!",
                                        reply_markup=ReplyKeyboardMarkup(
                                            [["Бошланғич", "Ўрта", "Юқори", "Она тилим"]],
                                            one_time_keyboard=True, resize_keyboard=True))
        return ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL


async def ask_it_knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    it_knowledge = update.message.text
    if it_knowledge in IT_KNOWLEDGE_OPTIONS:
        context.user_data['IT Knowledge'] = it_knowledge
        await update.message.reply_text(
            "👤 Биз ҳақимизда қаердан хабар топдингиз. Жавоблар орасидан танланг:",
            reply_markup=ReplyKeyboardMarkup([SOURCE_OPTIONS], one_time_keyboard=True, resize_keyboard=True)
        )
        return ASK_SOURCE
    else:
        await update.message.reply_text("Компьютер саводхонлик даражангизни қуйидагилар орасидан танланг:")
        return ASK_IT_KNOWLEDGE

async def ask_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    source = update.message.text
    if source in SOURCE_OPTIONS:
        context.user_data['Source'] = source
        await update.message.reply_text(f"{context.user_data}")
        await update.message.reply_text(
            "🥳 Рўйхатдан ўтиш жараёнини муваффақиятли якунлаганингиз билан табриклаймиз! \nИлтимос маълумотларингизни қайта кўриб чиқинг ва тасдиқланг.",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text="Тасдиқлаш")],
                                              [KeyboardButton(text="Қайта бошлаш")]], resize_keyboard=True, one_time_keyboard=True)
        )
        return CONFIRMATION
    else:
        await update.message.reply_text("👤 Биз ҳақимизда қаердан хабар топдингиз. Жавоблар орасидан танланг:")
        return ASK_SOURCE

async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    confirmation_of = update.message.text
    if confirmation_of == "Тасдиқлаш":
        da_ta = list(context.user_data.values())
        print(da_ta)
        keyboard_1 = [[InlineKeyboardButton("Instagram саҳифамизга қуйидаги ҳавола орқали ўтинг👇👇👇", url="https://www.instagram.com/profter_uz/profilecard/?igsh=N2F5YWZtZmNwNTR0")]]
        reply_markup_3 = InlineKeyboardMarkup(keyboard_1)
        await update.message.reply_text("✅ Маълумотларингиз қабул қилинди. Тез орада сиз билан ходимларимиз боғланади 😊.\n\nБизни ижтимоий тармоқларда кузатиб боришни унутманг!\n",
                                        reply_markup=reply_markup_3)
        insert_data_to(da_ta)
        return ConversationHandler.END
    elif confirmation_of == "Қайта бошлаш":
        await update.message.reply_text("✏️ Бироз кутинг....\nДастур қайта ишга туширилмоқда....")
        time.sleep(5)
        await update.message.reply_text("Тўлиқ исм-шарифингизни киритинг: ")
        return ASK_NAME
    else:
        await update.message.reply_text("Илтимос бироздан сўнг қайта уриниб кўринг!")
        return CONFIRMATION

from telegram.ext import ConversationHandler

def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("help", help_command))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_BIRTH_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birth_year)],
            ASK_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_education)],
            ASK_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_region)],
            ASK_DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_district)],
            ASK_PHONE: [MessageHandler(filters.CONTACT & ~filters.COMMAND, ask_phone)],
            ASK_ADDITIONAL_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_additional_phone)],
            ASK_PHONE_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, manual_numbers)],
            ASK_MARITAL_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_marital_status)],
            ASK_WORKPLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_workplace)],
            ASK_EXPECTED_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_expected_salary)],
            ASK_EXPECTED_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_expected_length)],
            ASK_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_language)],
            ASK_LANGUAGE_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_language_level)],
            ASK_ADDITIONAL_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_additional_language)],
            ASK_ADDITIONAL_LANGUAGE_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_additional_language_level)],
            ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_additional_language_level_level)],
            ASK_IT_KNOWLEDGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_it_knowledge)],
            ASK_SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_source)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv_handler)
    app.run_polling()
if __name__ == "__main__":
    main()

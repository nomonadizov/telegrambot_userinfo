import logging
import telegram
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import datetime
from db import insert_data_to

load_dotenv()
BOT_TOKEN = f"{os.getenv('BOT_TOKEN')}"
bot = telegram.Bot(token=BOT_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

ASK_NAME_1, ASK_NAME, ASK_BIRTH_YEAR, ASK_BIRTH_MONTH, ASK_BIRTH_DAY, ASK_EDUCATION, ASK_REGION, ASK_PHONE, ASK_PHONE_MANUAL,\
ASK_ADDITIONAL_PHONE, ASK_MARITAL_STATUS, ASK_WORKPLACE, ASK_EXPECTED_SALARY, ASK_EXPECTED_LENGTH, \
ASK_LANGUAGE, ASK_LANGUAGE_LEVEL, ASK_ADDITIONAL_LANGUAGE, ASK_ADDITIONAL_LANGUAGE_LEVEL, \
ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL, ASK_IT_KNOWLEDGE, ASK_SOURCE, CONFIRMATION = range(22)

# Define options for responses
OPTIONS_OF = ["Yes", "No"]
EDUCATION_OPTIONS = ["Bachelors", "High School Diploma", "Masters", "Other"]
REGION_OPTIONS = ["Tashkent", "Samarkand", "Andijan", "Other"]
PHONE_OPTIONS = [KeyboardButton("📲 Share my contact", request_contact=True)]
MARRITAL_STATUS_OPTIONS = ["Single", "Married"]
EXPECTED_SALARY_OPTIONS = ["5,000,000 UZS", "10,000,000 UZS", "15,000,000 UZS", "Prefer not to say"]
EXPECTED_LENGTH_OPTIONS = ["1 Year", "3 Years", "5 Years", "Prefer not to say"]
LANGUAGE_OPTIONS = ["Uzbek", "Russian", "English", "Other"]
IT_KNOWLEDGE_OPTIONS = ["0%", "30%", "50%", "70%", "100%"]
SOURCE_OPTIONS = ["Friend", "Family Member", "Social Media", "Street Advertisement", "Other"]

help_text = (
    "Here are the commands you can use:\n"
    "/start - Start interacting with the bot\n"
    "/help - Get this help message\n"
    "Feel free to ask anything!"
)

async def handle_update(data):
    # Process data from Telegram webhook here
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']

        if message_text == "/help":
            await bot.send_message(chat_id=chat_id, text=help_text)
        else:
            # Send a generic reply or custom response
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
    await update.message.reply_text("👋 Welcome to our bot!", reply_markup=ReplyKeyboardMarkup([["Start application"],["Review my information"]]))

    return ASK_NAME_1

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_input = update.message.text
    if name_input == "Start application":
        await update.message.reply_text("Enter your full name: ")
        return ASK_NAME
    elif name_input == "Review my information":
        await update.message.reply_text(f"{context.user_data}")
        return ASK_NAME_1


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_2 = update.message.text
    if not name_2.isdigit():
        context.user_data['Name'] = name_2
        await update.message.reply_text("📅 Enter your birth day-month-year: \nexample: 02-02-2004")
        return ASK_BIRTH_YEAR
    else:
        await update.message.reply_text("❗ Please enter a valid name (letters only). Try again:")
        return ASK_NAME

async def ask_birth_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    year = update.message.text
    if len(year) == 10 and year[:2].isdigit() and year[3:5].isdigit() and year[6:].isdigit() and int(year[6:])<datetime.datetime.now().year:
        if year[3:6] == "02" and int(year[:2])>29:
            await update.message.reply_text("❗ Please enter a valid year (numeric). Try again!\nexample: 02-02-2004")
            return ASK_BIRTH_YEAR
        else:
            context.user_data['Birth Year'] = year
            await update.message.reply_text("🎓 What is your level of education?",
                                            reply_markup=ReplyKeyboardMarkup([EDUCATION_OPTIONS], one_time_keyboard=True))
            return ASK_EDUCATION
    else:
        await update.message.reply_text("❗ Please enter a valid year (numeric). Try again!\nexample: 02-02-2004")
        return ASK_BIRTH_YEAR

async def ask_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    education = update.message.text
    print(education)
    if education in EDUCATION_OPTIONS:
        context.user_data['Education Level'] = education
        await update.message.reply_text("🌍 Choose your region:", reply_markup=ReplyKeyboardMarkup(keyboard=[REGION_OPTIONS], one_time_keyboard=True))
        return ASK_REGION
    else:
        await update.message.reply_text("❗ Please select a valid option. Try again:")
        return ASK_EDUCATION


async def ask_region(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    region = update.message.text
    print(region)
    if region in REGION_OPTIONS:
        context.user_data['Region'] = region
        await update.message.reply_text("📞 Enter your phone number:",
                                        reply_markup=ReplyKeyboardMarkup([PHONE_OPTIONS], one_time_keyboard=True,
                                        resize_keyboard=True))
        return ASK_PHONE
    else:
        await update.message.reply_text("Choose a valid option. Try again:")
        return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    print(phone)
    if phone:
        print(phone)
        context.user_data['Phone Number'] = phone
        await update.message.reply_text("📞 Do you have an additional phone number? (Yes/No)",
                                        reply_markup=ReplyKeyboardMarkup([OPTIONS_OF], one_time_keyboard=True, resize_keyboard=True))
        return ASK_ADDITIONAL_PHONE
    else:
        await update.message.reply_text("❗ Please select a valid option. Try again:2")
        return ASK_PHONE


async def manual_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text
    if number.isdigit() and len(number) >= 9:
        context.user_data['Additional Phone Number'] = number
        await update.message.reply_text("💍 What is your marital status?",
                                        reply_markup=ReplyKeyboardMarkup([MARRITAL_STATUS_OPTIONS],
                                                                         one_time_keyboard=True))
        return ASK_MARITAL_STATUS
    else:
        await update.message.reply_text("❗ Please select a valid option. Try again:1")
        return ASK_PHONE_MANUAL

async def ask_additional_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = update.message.text
    if phone == "Yes":
        await update.message.reply_text("Please enter your phone number:  (only last 9 digits)")
        return ASK_PHONE_MANUAL
    if phone == "No":
        context.user_data['Additional Phone Number'] = "N/A"
        await update.message.reply_text("💍 What is your marital status?",
                                        reply_markup=ReplyKeyboardMarkup([MARRITAL_STATUS_OPTIONS],
                                        one_time_keyboard=True))
        return ASK_MARITAL_STATUS
    else:
        return ASK_ADDITIONAL_PHONE

async def ask_marital_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        married = update.message.text
        if married in MARRITAL_STATUS_OPTIONS:
            context.user_data['Marital Status'] = married
            await update.message.reply_text("What was your previous workplace?")
            return ASK_WORKPLACE
        else:
            return ASK_MARITAL_STATUS

async def ask_workplace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    workplace = update.message.text
    if not workplace.isdigit():
        context.user_data['Previous Workplace'] = workplace
        await update.message.reply_text("💰 What is your expected salary?", reply_markup=ReplyKeyboardMarkup([EXPECTED_SALARY_OPTIONS], one_time_keyboard=True))
        return ASK_EXPECTED_SALARY
    else:
        await update.message.reply_text("❗ Please enter a valid workplace name. Try again:")
        return ASK_WORKPLACE

async def ask_expected_salary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    salary = update.message.text
    if salary in EXPECTED_SALARY_OPTIONS:
        context.user_data['Expected Salary'] = salary
        await update.message.reply_text("⏳ What is your expected length of work with us?", reply_markup=ReplyKeyboardMarkup([EXPECTED_LENGTH_OPTIONS], one_time_keyboard=True))
        return ASK_EXPECTED_LENGTH
    else:
        await update.message.reply_text("❗ Please select a valid salary option. Try again:")
        return ASK_EXPECTED_SALARY

async def ask_expected_length(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    length = update.message.text
    if length in EXPECTED_LENGTH_OPTIONS:
        context.user_data['Expected Length'] = length
        await update.message.reply_text("🗣 What languages do you know?", reply_markup=ReplyKeyboardMarkup([LANGUAGE_OPTIONS], one_time_keyboard=True))
        return ASK_LANGUAGE
    else:
        await update.message.reply_text("❗ Please select a valid option. Try again:")
        return ASK_EXPECTED_LENGTH


async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = update.message.text
    if language in LANGUAGE_OPTIONS:
        context.user_data['Language'] = language
        await update.message.reply_text("🌍 What is your level in this language?", reply_markup=ReplyKeyboardMarkup([["Beginner", "Intermediate", "Advanced", "Native"]], one_time_keyboard=True))
        return ASK_LANGUAGE_LEVEL
    else:
        await update.message.reply_text("❗ Please select a valid language option. Try again:")
        return ASK_LANGUAGE

async def ask_language_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language_level = update.message.text
    if language_level in ["Beginner", "Intermediate", "Advanced", "Native"]:
        context.user_data['Language Level'] = language_level
        await update.message.reply_text(
            "🌍 Do you know any additional languages? (Yes/No)",
            reply_markup=ReplyKeyboardMarkup([OPTIONS_OF], one_time_keyboard=True)
        )
        return ASK_ADDITIONAL_LANGUAGE
    else:
        await update.message.reply_text("❗ Please select a valid option. Try again:")
        return ASK_LANGUAGE_LEVEL

async def ask_additional_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer == "Yes":
        await update.message.reply_text("🌍 Please enter the additional language you know:", reply_markup=ReplyKeyboardMarkup([LANGUAGE_OPTIONS], one_time_keyboard=True))
        return ASK_ADDITIONAL_LANGUAGE_LEVEL
    elif update.message.text == "No":
        context.user_data['Additional Language'] = "N/A"
        context.user_data['Additional Language Level'] = "N/A"
        await update.message.reply_text(
            "💻 How familiar are you with IT and computer systems?",
            reply_markup=ReplyKeyboardMarkup([IT_KNOWLEDGE_OPTIONS], one_time_keyboard=True)
        )
        return ASK_IT_KNOWLEDGE
    else:
        await update.message.reply_text("❗ Please choose 'Yes' or 'No'.")
        return ASK_ADDITIONAL_LANGUAGE

async def ask_additional_language_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    additional_language = update.message.text
    if additional_language in LANGUAGE_OPTIONS:
        context.user_data['Additional Language'] = additional_language
        await update.message.reply_text(f"What is your level of {additional_language} knowledge!", reply_markup=ReplyKeyboardMarkup([["Beginner", "Intermediate", "Advanced", "Native"]], one_time_keyboard=True))
        return ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL
    else:
        await update.message.reply_text("❗ Please select a valid level. Try again:")
        return ASK_ADDITIONAL_LANGUAGE_LEVEL

async def ask_additional_language_level_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    additional_language_level = update.message.text
    if additional_language_level in ["Beginner", "Intermediate", "Advanced", "Native"]:
        context.user_data['Additional Language Level'] = additional_language_level
        await update.message.reply_text(
            "💻 How familiar are you with IT and computer systems?",
            reply_markup=ReplyKeyboardMarkup([IT_KNOWLEDGE_OPTIONS], one_time_keyboard=True))
        return ASK_IT_KNOWLEDGE
    else:
        await update.message.reply_text("What is your level of knowledge!",
                                        reply_markup=ReplyKeyboardMarkup(
                                            [["Beginner", "Intermediate", "Advanced", "Native"]],
                                            one_time_keyboard=True))
        return ASK_ADDITIONAL_LANGUAGE_LEVEL_LEVEL


async def ask_it_knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    it_knowledge = update.message.text
    if it_knowledge in IT_KNOWLEDGE_OPTIONS:
        context.user_data['IT Knowledge'] = it_knowledge
        await update.message.reply_text(
            "👤 How did you hear about us?",
            reply_markup=ReplyKeyboardMarkup([SOURCE_OPTIONS], one_time_keyboard=True)
        )
        return ASK_SOURCE
    else:
        await update.message.reply_text("❗ Please select a valid IT knowledge level. Try again:")
        return ASK_IT_KNOWLEDGE

async def ask_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    source = update.message.text
    if source in SOURCE_OPTIONS:
        context.user_data['Source'] = source
        await update.message.reply_text(f"{context.user_data}")
        await update.message.reply_text(
            "Thank you for your information! Please review and confirm your details.",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text="Confirm")],
                                              [KeyboardButton(text="Restart")]])
        )
        return CONFIRMATION
    else:
        await update.message.reply_text("❗ Please select a valid source option. Try again:")
        return ASK_SOURCE

async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    confirmation_of = update.message.text
    if confirmation_of == "Confirm":
        da_ta = list(context.user_data.values())
        print(da_ta)
        await update.message.reply_text("✅ Your information has been saved! Thank you!")
        insert_data_to(da_ta)
        return ConversationHandler.END
    elif confirmation_of == "Restart":
        await update.message.reply_text("✏️ We will  restart the program.\nEnter your name: ")
        return ASK_NAME
    else:
        await update.message.reply_text("If something went wrong, try again later!")
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
            # ASK_BIRTH_MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birth_month)],
            # ASK_BIRTH_DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birth_day)],
            ASK_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_education)],
            ASK_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_region)],
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
        fallbacks=[CommandHandler("start", start)],  # Optionally, restart with /start
    )

    # Add the conversation handler to the application
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import openai
from openai import AsyncOpenAI

# Загрузка переменных окружения
load_dotenv()

# Установка констант из переменных окружения
TOKEN = os.getenv('TG_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEFAULT_SYSTEM = os.getenv('SYSTEM',"Ты умный помощник")
MODEL = os.getenv('MODEL', 'gpt-3.5-turbo')  # Установка модели по умолчанию, если не задана
TEMPERATURE = int(os.getenv('TEMPERATURE', 0))  # Установка температуры по умолчанию, если не задана

# Фиксированный набор моделей, которые пользователь может выбрать
USER_CHOICE_MODELS = {'gpt-4-turbo', 'gpt-4-1106', 'gpt-3.5-turbo'}

# Установка ключа OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    raise ValueError("Не задан OPENAI_API_KEY в .env файле")

# Инициализация асинхронного клиента OpenAI
client = AsyncOpenAI()

# Обработчик команды /start
async def start(update, context):
    await update.message.reply_text('Добро пожаловать, я готов помочь вам!')

# Обработчик текстовых сообщений
async def text(update, context):
    user_message = update.effective_message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = await async_get_answer(DEFAULT_SYSTEM, user_message)
    await update.message.reply_text(response)

# Обработчик изображений
async def image(update, context):
    # TODO: Добавить обработку изображений, если необходимо
    await update.message.reply_text('Изображение получено, но обработка ещё не настроена.')

# Обработчик голосовых сообщений
async def voice(update, context):
    # TODO: Добавить обработку голосовых сообщений, если необходимо
    await update.message.reply_text("Голосовое сообщение получено, но обработка ещё не настроена.")

# Обработчик команды /settings
async def settings(update, context):
    global MODEL, DEFAULT_SYSTEM
    command_text = update.message.text
    parts = command_text.split(maxsplit=2)

    if len(parts) == 3:
        option, value = parts[1], parts[2]
        if option == 'model' and value in USER_CHOICE_MODELS:
            MODEL = value
            await update.message.reply_text(f"Модель успешно изменена на: {value}")
        elif option == 'system':
            DEFAULT_SYSTEM = value
            await update.message.reply_text(f"System успешно изменен на: {value}")
    elif len(parts) == 2:
        option = parts[1]
        if option == 'model':
            await update.message.reply_text(f"Текущая модель: {MODEL}")
        elif option == 'system':
            await update.message.reply_text(f"Текущий system: {DEFAULT_SYSTEM}")

# Асинхронная функция получения ответа от chatgpt
async def async_get_answer(system, query):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": query}
    ]
    completion = await client.chat.completions.create(model=MODEL, messages=messages, temperature=TEMPERATURE)
    return completion.choices[0].message.content

# Основная функция запуска бота
def main():
    # Создание приложения с заданным токеном
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(MessageHandler(filters.TEXT, text))
    application.add_handler(MessageHandler(filters.PHOTO, image))
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # Запуск бота
    application.run_polling()
    print('Бот остановлен')

# Точка входа в приложение
if __name__ == "__main__":
    main()
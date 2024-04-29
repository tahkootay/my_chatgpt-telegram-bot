from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from dotenv import load_dotenv
import os 
import openai
from openai import OpenAI, AsyncOpenAI
#import asyncio

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

# настройки chatgpt
default_system = os.getenv('SYSTEM')
model = os.getenv('MODEL')
user_choice_model = {'gpt-4-turbo','gpt-4-1106','gpt-3.5-turbo'}
temperature = int(os.getenv('TEMPERATURE'))

client = AsyncOpenAI()

# функция-обработчик команды /start
async def start(update, context):
    await update.message.reply_text('Добро пожаловать')

# функция-обработчик текстовых сообщений
async def text(update, context):   
    user_message = update.effective_message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")  # Отправляем информацию о том, что бот печатает   
    response = await async_get_answer(default_system, user_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_to_message_id=update.message.message_id)

# функция-обработчик изображение
async def image(update, context):
    # получаем изображение из апдейта
    file = await update.message.photo[-1].get_file() 
    await update.message.reply_text(f'Изобржение получено (не обработано)') 

# функция-обработчик голосовых сообщений
async def voice(update: Update, context):
    # получаем файл голосового сообщения из апдейта
    new_file = await update.message.voice.get_file()
    await update.message.reply_text(f"Голосовое сообщение получено!")

async def settings(update, context):
    global model
    global default_system
    command_text = update.message.text 
    # Разделяем команду и аргументы
    parts = command_text.split(maxsplit=2) 
    if len(parts) == 3:
            if parts[1]=='model' and parts[2] in user_choice_model:
                model = parts[2]
                await update.message.reply_text(f"Модель успешно изменена на: {parts[2]}")
            elif parts[1]=='system':
                default_system = parts[2]
                await update.message.reply_text(f"System успешно изменен на: {parts[2]}")
    elif len(parts) == 2:
        if parts[1]=='model':
            await update.message.reply_text(f"Текущая модель: {model}") 
        if parts[1]=='system':
            await update.message.reply_text(f"Текущий system: {default_system}") 
         

async def async_get_answer(system:str = default_system, query:str = None):
        #Асинхронная функция получения ответа от chatgpt   
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": query}
        ]
        # получение ответа от chatgpt
        completion = await client.chat.completions.create(model=model,
                                                  messages=messages,
                                                  temperature=temperature)
        
        return completion.choices[0].message.content


def main():
    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    #добавляем обработчик команды /settings
    application.add_handler(CommandHandler("settings", settings))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик фото 
    application.add_handler(MessageHandler(filters.PHOTO, image))   

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))  

    # запускаем бота (нажать Ctrl-C для остановки бота)
    application.run_polling()
    print('Бот остановлен')
if __name__ == "__main__":
    main()
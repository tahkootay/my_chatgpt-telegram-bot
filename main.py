from telegram.ext import Application, CommandHandler, MessageHandler, filters #CallbackQueryHandler, CallbackContext
from telegram import Update, Update
from dotenv import load_dotenv
import os 
import openai


# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

# API-key
openai.api_key = os.environ.get("OPENAI_API_KEY")
default_system = "" #инструкция для chatgpt
model = "gpt-3.5-turbo"
temperature = 0


# функция-обработчик команды /start
async def start(update, context):
    await update.message.reply_text('Добро пожаловать')

# функция-обработчик текстовых сообщений
async def text(update, context):   
    user_message = update.effective_message.text
    await update.message.reply_text(f'Текстовое собщение получено:{user_message}') 

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

# async def settings(update, context):
#     command_text = update.message.text 
#     # Разделяем команду и аргументы
#     parts = command_text.split(maxsplit=1)
#     if len(parts) > 1:
#         answer_text = parts[1]
#         await update.message.reply_text(f"Спасибо, изменения внесены. Новое значение {answer_text}") 

async def async_get_answer(self, system:str = default_system, query:str = None):
        #Асинхронная функция получения ответа от chatgpt   
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": query}
        ]

        # получение ответа от chatgpt
        completion = await openai.ChatCompletion.acreate(model=model,
                                                  messages=messages,
                                                  temperature=temperature)
        
        return completion.choices[0].message.content

def main():
    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик команды /settings
    # application.add_handler(CommandHandler("settings", settings))

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
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "BOTOKEN"
OPENAI_API_KEY = "APIKEY"

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Ты помощник по государственным услугам Казахстана. 
Отвечай ТОЛЬКО на вопросы связанные с:
- ЦОН (Центр обслуживания населения)
- 1414 (контакт-центр)
- Egov.kz
- Государственные услуги, документы, справки
- Старайся что бы пользыватель решил проблему на своем уровне
- Старайся что бы он часто не звонил 1414

Если вопрос НЕ связан с этими темами — вежливо откажи и скажи что можешь помочь только по госуслугам Казахстана.
Отвечай на том языке на котором пишет пользователь (казахский или русский)."""
            },
            {"role": "user", "content": user_text}
        ]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен!")
app.run_polling()
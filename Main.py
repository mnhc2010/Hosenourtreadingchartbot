import os
import telebot
from google import genai
from google.genai import types

TELEGRAM_TOKEN = os.environ.get("https://core.telegram.org/bots/api")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6LCIIjxz1uX10gc4EuGYRfrYAZkvv2woxusd4kucObohg")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "স্বাগতম! যেকোনো ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট পাঠান, আমি UP নাকি DOWN যাওয়ার সম্ভাবনা বেশি তা জানিয়ে দেব।"
    )

@bot.message_handler(content_types=['photo'])
def handle_chart_photo(message):
    status_msg = bot.reply_to(message, "চার্টটি বিশ্লেষণ করা হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        prompt = (
            "Analyze this trading chart as an expert technical analyst. "
            "Look at candlestick patterns, support/resistance, and indicators. "
            "Provide a short answer in Bengali with: "
            "1. Prediction: UP or DOWN "
            "2. Confidence: High / Medium / Low "
            "3. Reason: 2 short points."
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=downloaded_file,
                    mime_type='image/jpeg',
                ),
            ]
        )
        
        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.reply_to(message, f"সমস্যা হয়েছে: {str(e)}")

bot.infinity_polling()

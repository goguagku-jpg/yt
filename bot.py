import os
import time
from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# التحقق من وجود التوكن
BOT_TOKEN = "8152510678:AAH7mFrO08lhj0jBAN6WV8l2-5xMWPDqxcg"  # التوكن الخاص بك
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

def play_video(update: Update, context: CallbackContext):
    url = "https://www.youtube.com/watch?v=j683w-kMTu8&t"

    options = Options()
    options.add_argument("--headless=new")  # تشغيل بدون واجهة
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get(url)
    time.sleep(5)
    update.message.reply_text("✅ الفيديو تم فتحه في المتصفح (Railway).")
    driver.quit()

def main():
    try:
        print("🚀 Starting bot...")
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        # إضافة معالج الأوامر
        dp.add_handler(CommandHandler("video", play_video))
        
        # بدء البوت
        print("✅ Bot is running... Press Ctrl+C to stop")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise e

if __name__ == "__main__":
    main()
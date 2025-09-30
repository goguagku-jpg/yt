import os
import time
import sys
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# التحقق من وجود التوكن
BOT_TOKEN = "8152510678:AAH7mFrO08lhj0jBAN6WV8l2-5xMWPDqxcg"  # التوكن الخاص بك
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

async def play_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.youtube.com/watch?v=j683w-kMTu8&t"

    options = Options()
    options.add_argument("--headless=new")  # تشغيل بدون واجهة
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get(url)
    time.sleep(5)
    await update.message.reply_text("✅ الفيديو تم فتحه في المتصفح (Railway).")
    driver.quit()

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("video", play_video))
    print("🚀 Bot started...")
    app.run_polling()
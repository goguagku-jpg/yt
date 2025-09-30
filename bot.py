import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get logger
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً! استخدم الأمر /open_youtube لفتح موقع يوتيوب في المتصفح.'
    )

async def open_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('جاري فتح المتصفح...')
    
    try:
        # إعداد متصفح كروم بدون وضع headless لرؤية المتصفح
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')  # تكبير النافذة
        
        # تشغيل المتصفح
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # فتح يوتيوب
        driver.get('https://www.youtube.com')
        await update.message.reply_text('تم فتح يوتيوب بنجاح! ✅')
        
    except Exception as e:
        logger.error(f"Error in open_youtube: {e}")
        await update.message.reply_text('عذراً، حدث خطأ أثناء فتح المتصفح.')

def main():
    # استخدام التوكن مباشرة
    token = "8152510678:AAH7mFrO08lhj0jBAN6WV8l2-5xMWPDqxcg"
    
    # إنشاء التطبيق
    application = Application.builder().token(token).build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open_youtube", open_youtube))

    # تشغيل البوت
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
import logging
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# تحميل المتغيرات من ملف .env
load_dotenv()

# استيراد المتغيرات
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 300))
CHROME_HEADLESS = os.getenv('CHROME_HEADLESS', 'True').lower() == 'true'
CHROME_WIDTH = int(os.getenv('CHROME_WIDTH', 1920))
CHROME_HEIGHT = int(os.getenv('CHROME_HEIGHT', 1080))
YOUTUBE_URL = os.getenv('YOUTUBE_URL', 'https://www.youtube.com')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get logger
logger = logging.getLogger(__name__)

# حفظ معرف آخر مستخدم للإشعارات
NOTIFICATION_CHAT_ID = None

class YouTubeChecker:
    def __init__(self):
        self.setup_driver()
        self.is_running = False
        self.notification_chat_id = None

    def setup_driver(self):
        chrome_options = Options()
        if CHROME_HEADLESS:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--window-size={CHROME_WIDTH},{CHROME_HEIGHT}')
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    async def check_youtube_status(self, context: ContextTypes.DEFAULT_TYPE):
        if not self.notification_chat_id:
            logger.warning("No notification chat ID set")
            return

        try:
            self.driver.get(YOUTUBE_URL)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-app")))
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"✅ يوتيوب يعمل بشكل طبيعي\nآخر فحص: {current_time}"
            
            await context.bot.send_message(
                chat_id=self.notification_chat_id,
                text=message
            )
            
            if DEBUG:
                logger.info(f"Successfully checked YouTube at {current_time}")
                
        except (TimeoutException, WebDriverException) as e:
            error_message = f"⚠️ مشكلة في الوصول إلى يوتيوب\nالخطأ: {str(e)}"
            logger.error(error_message)
            
            await context.bot.send_message(
                chat_id=self.notification_chat_id,
                text=error_message
            )

    def cleanup(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

# إنشاء نسخة عالمية من الفاحص
youtube_checker = YouTubeChecker()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global youtube_checker
    
    if update.effective_chat:
        youtube_checker.notification_chat_id = update.effective_chat.id
        
        await update.message.reply_text(
            'مرحباً! سأقوم بإرسال إشعارات عن حالة يوتيوب.\n'
            'استخدم /start_monitoring لبدء المراقبة\n'
            'استخدم /stop_monitoring لإيقاف المراقبة'
        )
    else:
        logger.error("No effective chat available")

async def start_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global youtube_checker
    
    if not youtube_checker.notification_chat_id:
        await update.message.reply_text('الرجاء استخدام الأمر /start أولاً')
        return
    
    if not youtube_checker.is_running:
        youtube_checker.is_running = True
        await update.message.reply_text(
            f'بدأت مراقبة يوتيوب. سأرسل لك إشعارات كل {CHECK_INTERVAL//60} دقائق.'
        )
        
        while youtube_checker.is_running:
            await youtube_checker.check_youtube_status(context)
            await asyncio.sleep(CHECK_INTERVAL)
    else:
        await update.message.reply_text('المراقبة قيد التشغيل بالفعل!')

async def stop_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global youtube_checker
    
    if not youtube_checker.notification_chat_id:
        await update.message.reply_text('الرجاء استخدام الأمر /start أولاً')
        return
    
    if youtube_checker.is_running:
        youtube_checker.is_running = False
        await update.message.reply_text('تم إيقاف المراقبة.')
    else:
        await update.message.reply_text('المراقبة متوقفة بالفعل!')

def main():
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN found in .env file!")
        return
        
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_monitoring", start_monitoring))
    application.add_handler(CommandHandler("stop_monitoring", stop_monitoring))

    # تشغيل البوت
    try:
        logger.info("Starting bot...")
        if DEBUG:
            logger.info(f"Debug mode: ON")
            logger.info(f"Chrome headless mode: {CHROME_HEADLESS}")
            logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        # تنظيف الموارد عند إيقاف البوت
        youtube_checker.cleanup()

if __name__ == '__main__':
    main()
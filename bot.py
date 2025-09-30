import logging
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

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

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # تشغيل في وضع headless للسيرفر
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    async def check_youtube_status(self, context: ContextTypes.DEFAULT_TYPE):
        try:
            self.driver.get('https://www.youtube.com')
            # انتظار ظهور عنصر معين للتأكد من تحميل الصفحة
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-app")))
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"✅ يوتيوب يعمل بشكل طبيعي\nآخر فحص: {current_time}"
            
            if NOTIFICATION_CHAT_ID:
                await context.bot.send_message(
                    chat_id=NOTIFICATION_CHAT_ID,
                    text=message
                )
                
        except (TimeoutException, WebDriverException) as e:
            error_message = f"⚠️ مشكلة في الوصول إلى يوتيوب\nالخطأ: {str(e)}"
            logger.error(error_message)
            if NOTIFICATION_CHAT_ID:
                await context.bot.send_message(
                    chat_id=NOTIFICATION_CHAT_ID,
                    text=error_message
                )

    def cleanup(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

# إنشاء نسخة عالمية من الفاحص
youtube_checker = YouTubeChecker()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global NOTIFICATION_CHAT_ID
    NOTIFICATION_CHAT_ID = update.effective_chat.id
    
    await update.message.reply_text(
        'مرحباً! سأقوم بإرسال إشعارات عن حالة يوتيوب.\n'
        'استخدم /start_monitoring لبدء المراقبة\n'
        'استخدم /stop_monitoring لإيقاف المراقبة'
    )

async def start_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global youtube_checker
    
    if not youtube_checker.is_running:
        youtube_checker.is_running = True
        await update.message.reply_text('بدأت مراقبة يوتيوب. سأرسل لك إشعارات كل 5 دقائق.')
        
        while youtube_checker.is_running:
            await youtube_checker.check_youtube_status(context)
            await asyncio.sleep(300)  # انتظار 5 دقائق
    else:
        await update.message.reply_text('المراقبة قيد التشغيل بالفعل!')

async def stop_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global youtube_checker
    
    if youtube_checker.is_running:
        youtube_checker.is_running = False
        await update.message.reply_text('تم إيقاف المراقبة.')
    else:
        await update.message.reply_text('المراقبة متوقفة بالفعل!')

def main():
    # استخدام التوكن مباشرة
    token = "8152510678:AAH7mFrO08lhj0jBAN6WV8l2-5xMWPDqxcg"
    
    # إنشاء التطبيق
    application = Application.builder().token(token).build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_monitoring", start_monitoring))
    application.add_handler(CommandHandler("stop_monitoring", stop_monitoring))

    # تشغيل البوت
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        # تنظيف الموارد عند إيقاف البوت
        youtube_checker.cleanup()

if __name__ == '__main__':
    main()
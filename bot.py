import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get logger
logger = logging.getLogger(__name__)

class YouTubeBot:
    def __init__(self, headless=True):
        self.headless = headless
        self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Set up Chrome service
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_window_size(1920, 1080)

    def take_screenshot(self, url):
        try:
            self.driver.get(url)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f'screenshot_{timestamp}.png'
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None

    def cleanup(self):
        if self.driver:
            self.driver.quit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً! أنا بوت التقاط صور من يوتيوب. استخدم الأمر /open_youtube مع رابط يوتيوب أو بدونه لالتقاط صورة.'
    )

async def open_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = ' '.join(context.args) if context.args else 'https://www.youtube.com'
    
    try:
        bot = YouTubeBot(headless=True)
        screenshot_path = bot.take_screenshot(url)
        bot.cleanup()
        
        if screenshot_path:
            with open(screenshot_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
            os.remove(screenshot_path)
        else:
            await update.message.reply_text('عذراً، حدث خطأ أثناء التقاط الصورة.')
    except Exception as e:
        logger.error(f"Error in open_youtube: {e}")
        await update.message.reply_text('عذراً، حدث خطأ غير متوقع.')

def main():
    # Get bot token from environment variable
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("No BOT_TOKEN environment variable found!")
        return

    # Create application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open_youtube", open_youtube))

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
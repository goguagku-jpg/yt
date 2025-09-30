# Telegram YouTube Bot on Railway

## خطوات التشغيل:

1. انسخ هذا المشروع وارفعه على **GitHub**.
2. ادخل إلى **Railway** ➝ أنشئ Project جديد ➝ اربطه مع مستودع GitHub.
3. في تبويب **Variables** أضف:
   - `BOT_TOKEN` : توكن البوت من BotFather
   - `CHROMEDRIVER_PATH` : `/usr/bin/chromedriver`
4. Railway سيبني المشروع باستخدام Dockerfile تلقائيًا.
5. بعد إتمام الـ Deploy ستظهر لك Logs فيها: `🚀 Bot started...`
6. الآن جرب في التلغرام: `/video` ➝ سيفتح الفيديو ويبعث لك رسالة تأكيد.

## متطلبات المشروع:
- Python 3.11
- python-telegram-bot
- selenium
- Google Chrome
- ChromeDriver

## الميزات:
- فتح فيديوهات يوتيوب تلقائياً
- تشغيل في وضع headless
- سهولة النشر على Railway
- تكامل مع Docker

## ملاحظات هامة:
- تأكد من إضافة المتغيرات البيئية في Railway
- البوت يعمل في وضع headless لتوفير الموارد
- يمكن تعديل رابط الفيديو في ملف `bot.py`
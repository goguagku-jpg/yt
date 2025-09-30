# بوت تلغرام لالتقاط صور من يوتيوب

هذا بوت تلغرام يقوم بالتقاط صور من موقع يوتيوب باستخدام سيلينيوم. يمكن استخدامه لأخذ لقطات شاشة من أي صفحة يوتيوب.

## المميزات
- التقاط صور من يوتيوب بجودة عالية
- دعم الروابط المخصصة
- وضع التشغيل الخفي (headless)
- سهولة النشر باستخدام Docker

## متطلبات التشغيل المحلي
1. بايثون 3.8 أو أحدث
2. متصفح Google Chrome
3. ChromeDriver متوافق مع إصدار متصفحك
4. توكن بوت تلغرام من [@BotFather](https://t.me/BotFather)

## خطوات التثبيت المحلي

1. استنسخ المستودع:
\`\`\`bash
git clone [رابط-المستودع]
cd [اسم-المجلد]
\`\`\`

2. قم بتثبيت المتطلبات:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. قم بإعداد متغير البيئة BOT_TOKEN:
\`\`\`bash
# Windows
set BOT_TOKEN=your-token-here

# Linux/Mac
export BOT_TOKEN=your-token-here
\`\`\`

4. شغّل البوت:
\`\`\`bash
python bot.py
\`\`\`

## التشغيل باستخدام Docker

1. ابنِ الصورة:
\`\`\`bash
docker build -t youtube-screenshot-bot .
\`\`\`

2. شغّل الحاوية:
\`\`\`bash
docker run -e BOT_TOKEN=your-token-here youtube-screenshot-bot
\`\`\`

## الأوامر المتاحة
- /start - بدء استخدام البوت
- /open_youtube [رابط] - التقاط صورة من يوتيوب (الرابط اختياري)

## النشر على Railway

1. انشئ حساباً على [Railway](https://railway.app/)
2. اربط حسابك على GitHub
3. انشئ مشروعاً جديداً واختر "Deploy from GitHub repo"
4. أضف متغير البيئة BOT_TOKEN في إعدادات المشروع
5. سيتم نشر البوت تلقائياً

## ملاحظات مهمة
- تأكد من استخدام توكن بوت صحيح
- البوت يعمل بوضع headless افتراضياً
- تأكد من توفر مساحة كافية للقطات الشاشة

## المساهمة
نرحب بمساهماتكم! يرجى إنشاء issue أو pull request.
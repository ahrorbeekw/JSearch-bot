# Ish Qidiruv Telegram Bot

Bu loyiha **Aiogram 3.21** yordamida qurilgan professional Telegram bot bo‘lib, u **JSearch API (RapidAPI)** bilan integratsiya qilingan. Bot orqali foydalanuvchilar to‘g‘ridan-to‘g‘ri Telegram ichida ish qidirishlari mumkin.

## Xususiyatlari
- Kalit so‘z va joylashuv bo‘yicha dunyo bo‘ylab ishlarni qidirish.
- Davlat, sana va sahifalash (pagination) orqali filtrlash.
- Toza va strukturalangan ish natijalari.
- `.env` konfiguratsiyasi (maxfiy kalitlarni saqlash uchun).
- To‘liq asinxron va production darajada tayyorlangan.

## Talablar
- Python 3.10+
- Telegram Bot API token – [@BotFather](https://t.me/BotFather) orqali olinadi.
- JSearch API kaliti – [RapidAPI](https://rapidapi.com/) orqali olinadi.

## O‘rnatish

```bash
git clone https://github.com/ahrorbeekw/JSearch-bot/.git
cd jobsearch-bot
python -m venv venv
source venv/bin/activate  # Windows uchun: venv\Scripts\activate
pip install -r requirements.txt
```

## Sozlash

Loyihaning ildiz qismida `.env` fayl yarating va quyidagilarni qo‘shing:

```
API_TOKEN=telegram_bot_tokeningiz
RAPID_API_KEY=rapidapi_kalitingiz
RAPID_API_HOST=jsearch.p.rapidapi.com
```

## Ishga tushirish

```bash
python main.py
```

## Loyihaning tuzilishi
```
jobsearch-bot/
│── main.py          # Asosiy fayl
│── .env             # Muhit o‘zgaruvchilari
│── requirements.txt # Kutubxonalar ro‘yxati
│── README.md        # Inglizcha hujjat
│── README_UZ.md     # O‘zbekcha hujjat
```

## Buyruqlar namunasi
- `/start` – Xush kelibsiz xabari.
- `/search python developer in usa` – AQSH bo‘yicha Python developer ishlarini ko‘rsatadi.
- `/help` – Yordamchi qo‘llanma.

## Litsenziya
MIT Litsenziya © 2025  

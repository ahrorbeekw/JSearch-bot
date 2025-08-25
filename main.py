import requests
import asyncio
import html
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import os 
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

BASE_URL = f"https://{RAPID_API_HOST}"

headers = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": RAPID_API_HOST
}

def escape_html(text: str) -> str:
    """HTML parse_mode uchun xavfsiz matn"""
    if not text:
        return ""
    return html.escape(str(text))


# Start command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        "👋 Salom! Men <b>Job Search Bot</b>man.\n\n"
        "Mening imkoniyatlarim:\n"
        "🔍 /search - ish qidirish\n"
        "ℹ️ /details - job ID bo‘yicha ma’lumot\n"
        "💰 /salary - lavozim bo‘yicha maosh\n"
        "🏢 /company_salary - kompaniya bo‘yicha maosh\n"
    )
    await message.answer(text, parse_mode="HTML")


# Search
@dp.message(Command("search"))
async def search_handler(message: types.Message):
    await message.answer(
        "Iltimos, izlash uchun quyidagicha yozing:\n"
        "<code>lavozim, joylashuv</code>\n\n"
        "Masalan: <code>developer, chicago</code>",
        parse_mode="HTML"
    )


@dp.message(F.text.regexp(r"^.+,\s?.+$"))
async def get_jobs(message: types.Message):
    try:
        role, location = message.text.split(",", 1)
        params = {
            "query": f"{role.strip()} jobs in {location.strip()}",
            "page": "1",
            "num_pages": "1",
            "country": "us",
            "date_posted": "all"
        }
        response = requests.get(BASE_URL + "/search", headers=headers, params=params)
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            await message.answer("❌ Hech qanday natija topilmadi.")
            return

        jobs = data["data"][:5]
        text = "🔎 <b>Topilgan ishlar:</b>\n\n"
        for job in jobs:
            text += (
                f"📌 <b>{escape_html(job.get('job_title'))}</b>\n"
                f"🏢 {escape_html(job.get('employer_name'))}\n"
                f"📍 {escape_html(job.get('job_city'))}, {escape_html(job.get('job_country'))}\n"
                f"🔗 <a href='{escape_html(job.get('job_apply_link'))}'>Apply Link</a>\n"
                f"🆔 ID: <code>{escape_html(job.get('job_id'))}</code>\n\n"
            )
        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await message.answer(f"❌ Xatolik: {escape_html(str(e))}", parse_mode="HTML")


# Details
@dp.message(Command("details"))
async def details_handler(message: types.Message):
    await message.answer("Iltimos, job ID kiriting:\nMasalan: <code>/details JOB_ID</code>", parse_mode="HTML")


@dp.message(F.text.regexp(r"^/details\s+\S+"))
async def get_job_details(message: types.Message):
    try:
        job_id = message.text.split(" ", 1)[1]
        response = requests.get(BASE_URL + "/job-details", headers=headers, params={"job_id": job_id})
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            await message.answer("❌ Ma’lumot topilmadi.")
            return

        job = data["data"][0]
        desc = escape_html(job.get("job_description", ""))
        if len(desc) > 500:
            desc = desc[:500] + "..."

        text = (
            f"📌 <b>{escape_html(job.get('job_title'))}</b>\n"
            f"🏢 {escape_html(job.get('employer_name'))}\n"
            f"📍 {escape_html(job.get('job_city'))}, {escape_html(job.get('job_country'))}\n\n"
            f"📝 {desc}\n\n"
            f"🔗 <a href='{escape_html(job.get('job_apply_link'))}'>Apply Link</a>"
        )
        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await message.answer(f"❌ Xatolik: {escape_html(str(e))}", parse_mode="HTML")


# Salary
@dp.message(Command("salary"))
async def salary_handler(message: types.Message):
    await message.answer("Iltimos, lavozim va joylashuvni yuboring:\nMasalan: <code>/salary developer, chicago</code>", parse_mode="HTML")


@dp.message(F.text.regexp(r"^/salary\s+.+,\s?.+$"))
async def get_salary(message: types.Message):
    try:
        text = message.text.replace("/salary", "").strip()
        role, location = text.split(",", 1)
        params = {"job_title": role.strip(), "location": location.strip()}
        response = requests.get(BASE_URL + "/estimated-salary", headers=headers, params=params)
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            await message.answer("❌ Maosh ma’lumotlari topilmadi.")
            return

        salary = data["data"][0]
        await message.answer(
            f"💰 <b>{escape_html(role.strip())}</b> uchun {escape_html(location.strip())} hududida maosh: \n"
            f"{escape_html(salary.get('publisher_name'))}: {escape_html(salary.get('publisher_salary'))}",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik: {escape_html(str(e))}", parse_mode="HTML")


# Company salary
@dp.message(Command("company_salary"))
async def company_salary_handler(message: types.Message):
    await message.answer("Iltimos, kompaniya nomi va lavozimni yuboring:\nMasalan: <code>/company_salary Google, developer</code>", parse_mode="HTML")


@dp.message(F.text.regexp(r"^/company_salary\s+.+,\s?.+$"))
async def get_company_salary(message: types.Message):
    try:
        text = message.text.replace("/company_salary", "").strip()
        company, role = text.split(",", 1)
        params = {"job_title": role.strip(), "company": company.strip()}
        response = requests.get(BASE_URL + "/company-job-salary", headers=headers, params=params)
        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            await message.answer("❌ Kompaniya bo‘yicha maosh ma’lumotlari topilmadi.")
            return

        salary = data["data"][0]
        await message.answer(
            f"🏢 {escape_html(company.strip())} dagi <b>{escape_html(role.strip())}</b> lavozimi uchun maosh:\n"
            f"{escape_html(salary.get('publisher_name'))}: {escape_html(salary.get('publisher_salary'))}",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik: {escape_html(str(e))}", parse_mode="HTML")


# Run bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

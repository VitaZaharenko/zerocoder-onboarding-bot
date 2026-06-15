import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8620507702:AAFKChmAgsBP7llf6TB-WeEFKX26cTemmMw")

FAQ = {
    "структура команды": """
👥 *Структура команды Zerocoder*

• *Методисты* — разрабатывают программы и уроки
• *Продакты* — управляют продуктом и метриками
• *Авторы контента* — создают учебные материалы
• *Операционный менеджер* — процессы и регламенты

По любому вопросу о задачах — сначала к своему тимлиду.
""",
    "инструменты": """
🛠 *Инструменты команды*

• *Notion* — база знаний, регламенты, задачи
• *Telegram* — основное общение
• *Google Docs/Sheets* — документы и таблицы
• *Figma* — дизайн и прототипы
• *Claude Code* — AI-автоматизации

Доступы запроси у операционного менеджера.
""",
    "первая неделя": """
📅 *Что делать на первой неделе*

1. Познакомься с командой в общем чате
2. Прочитай базовые регламенты в Notion
3. Запроси доступы к инструментам
4. Посети все командные встречи как наблюдатель
5. Задавай вопросы — это нормально и ожидаемо

Никаких задач на первой неделе — только погружение.
""",
    "документы": """
📁 *Где найти документы*

• *Регламенты* — Notion → Команда → Регламенты
• *Шаблоны уроков* — Notion → Методология → Шаблоны
• *Контакты* — Notion → Команда → Контакты
• *Задачи* — Notion → Проекты → Текущий спринт

Если не можешь найти — напиши операционному менеджеру.
""",
    "контакты": """
📞 *Ключевые контакты*

• *Тимлид методологии* — по вопросам задач и уроков
• *Операционный менеджер* — доступы, процессы, орг.вопросы
• *HR* — оформление, отпуска, больничные
• *IT* — технические проблемы

Все контакты есть в Notion → Команда → Контакты
""",
}

MAIN_MENU = [
    ["📅 Первая неделя", "👥 Структура команды"],
    ["🛠 Инструменты", "📁 Документы"],
    ["📞 Контакты", "❓ Задать вопрос"],
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    keyboard = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, {name}! 👋\n\n"
        "Я помогу тебе разобраться в Zerocoder — отвечу на вопросы о команде, "
        "инструментах и процессах.\n\n"
        "Выбери тему или напиши свой вопрос:",
        reply_markup=keyboard,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    mapping = {
        "первая неделя": "первая неделя",
        "структура команды": "структура команды",
        "инструменты": "инструменты",
        "документы": "документы",
        "контакты": "контакты",
    }

    for key, faq_key in mapping.items():
        if key in text:
            await update.message.reply_text(FAQ[faq_key], parse_mode="Markdown")
            return

    await update.message.reply_text(
        "Не нашла готового ответа на этот вопрос.\n\n"
        "Напиши операционному менеджеру — он поможет. "
        "Или выбери тему из меню ниже 👇"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()

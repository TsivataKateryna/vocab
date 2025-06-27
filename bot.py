import os
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    CallbackQueryHandler,
)

load_dotenv()

def load_pairs(path):
    pairs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "#" not in line:
                continue
            fr, en = line.split("#", 1)
            pairs.append(
                {
                    "question": fr.strip(),
                    "answer": en.strip(),
                    "hint": f"C'est le mot anglais pour '{fr.strip()}'",
                }
            )
    return pairs


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pairs_path = os.path.join(BASE_DIR, "database", "words.txt")
PAIRS = load_pairs(pairs_path)


async def start(update: Update, context: CallbackContext):
    context.user_data.clear()
    questions = random.sample(PAIRS, min(5, len(PAIRS)))
    context.user_data["questions"] = questions
    context.user_data["current"] = 0
    context.user_data["score"] = 0

    await update.message.reply_text(
        "Bienvenue au quiz de vocabulaire! Je vais vous poser 5 questions."
    )
    await ask_question(update, context)


async def ask_question(update: Update, context: CallbackContext):
    current = context.user_data["current"]
    questions = context.user_data["questions"]

    if current >= len(questions):
        score = context.user_data["score"]
        await update.message.reply_text(
            f"Quiz terminé! Vous avez obtenu {score} sur {len(questions)}."
        )
        return

    q = questions[current]
    keyboard = [
        [InlineKeyboardButton("Afficher l'indice", callback_data=f"hint_{current}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Traduisez ce mot: {q['question']}", reply_markup=reply_markup)


async def handle_answer(update: Update, context: CallbackContext):
    if "questions" not in context.user_data:
        await update.message.reply_text("Tapez /start pour commencer le quiz.")
        return

    user_answer = update.message.text.strip().lower()
    current = context.user_data["current"]
    questions = context.user_data["questions"]

    if current >= len(questions):
        await update.message.reply_text("Le quiz est déjà terminé. Tapez /start pour recommencer.")
        return

    correct_answer = questions[current]["answer"].lower()
    if user_answer == correct_answer:
        context.user_data["score"] += 1
        await update.message.reply_text("Correct ! 🎉")
    else:
        await update.message.reply_text(f"Incorrect. La bonne réponse était: {correct_answer}")

    context.user_data["current"] += 1
    await ask_question(update, context)


async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("hint_"):
        idx = int(data.split("_")[1])
        questions = context.user_data.get("questions", [])
        if 0 <= idx < len(questions):
            question = questions[idx]
            await query.message.reply_text(f"Indice : {question['hint']}")


def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    # print("TOKEN =", TOKEN) 
    if not TOKEN:
        print("Erreur.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_answer))
    app.add_handler(CallbackQueryHandler(button))

    commands = [BotCommand("start", "Commencer le quiz")]
    app.bot.set_my_commands(commands)

    print("Bot démarré...")
    app.run_polling()


if __name__ == "__main__":
    main()

import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = "https://api.cricketapi.com/v1/matches"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Cricket Live Score Bot! 🎉\n\n"
        "Available commands:\n"
        "/live - Get live cricket scores\n"
        "/matches - Get upcoming matches\n"
        "/help - Get help"
    )

# Live scores command
async def live_scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = response.json()
        scores = ""
        for match in data.get("matches", []):
            score_text = match.get('score', "Score not available")
            scores += f"{match['team1']['name']} vs {match['team2']['name']}: {score_text}\n"
        if not scores:
            scores = "No live matches currently. 🏏"
        await update.message.reply_text(scores)
    except Exception as e:
        await update.message.reply_text(f"Error fetching live scores: {e}")

# Upcoming matches command
async def upcoming_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = response.json()
        matches_text = ""
        for match in data.get("matches", []):
            date = match.get('date', "Date not available")
            matches_text += f"{match['team1']['name']} vs {match['team2']['name']} on {date}\n"
        if not matches_text:
            matches_text = "No upcoming matches found. 🏏"
        await update.message.reply_text(matches_text)
    except Exception as e:
        await update.message.reply_text(f"Error fetching upcoming matches: {e}")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/live - Get live cricket scores\n"
        "/matches - Get upcoming matches"
    )

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("live", live_scores))
    app.add_handler(CommandHandler("matches", upcoming_matches))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()

import os
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Telegram Bot Token
API_KEY = os.getenv("API_KEY")  # Cricket API Key
API_ENDPOINT = "https://api.cricketapi.com/v1/matches"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Cricket Live Score Bot! 🎉\n"
        "Commands:\n"
        "/live - Get live cricket scores\n"
        "/matches - Get upcoming matches\n"
        "/help - Get help"
    )

# Async HTTP fetch function
async def fetch_json(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.json()

# Live scores command
async def live_scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = await fetch_json(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        scores = ""
        for match in data.get("matches", []):
            score_text = match.get("score", "Score not available")
            scores += f"{match['team1']['name']} vs {match['team2']['name']}: {score_text}\n"
        if not scores:
            scores = "No live matches currently. 🏏"
        await update.message.reply_text(scores)
    except Exception as e:
        await update.message.reply_text(f"Error fetching live scores: {e}")

# Upcoming matches command
async def upcoming_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = await fetch_json(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        matches_text = ""
        for match in data.get("matches", []):
            date = match.get("date", "Date not available")
            matches_text += f"{match['team1']['name']} vs {match['team2']['name']} on {date}\n"
        if not matches_text:
            matches_text = "No upcoming matches found. 🏏"
        await update.message.reply_text(matches_text)
    except Exception as e:
        await update.message.reply_text(f"Error fetching upcoming matches: {e}")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/live - Get live cricket scores\n"
        "/matches - Get upcoming matches\n"
        "/help - Show this help message"
    )

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("live", live_scores))
    app.add_handler(CommandHandler("matches", upcoming_matches))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()

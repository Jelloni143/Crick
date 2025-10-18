import logging
import os
from telegram.ext import Updater, CommandHandler
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = "https://api.cricketapi.com/v1/matches"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
def start(update, context):
    update.message.reply_text(
        "Welcome to Cricket Live Score Bot! 🎉\n\n"
        "Available commands:\n"
        "/live - Get live cricket scores\n"
        "/matches - Get upcoming matches\n"
        "/help - Get help"
    )

# Live scores
def live_scores(update, context):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = response.json()
        scores = ""
        for match in data.get("matches", []):
            score_text = match.get('score', "Score not available")
            scores += f"{match['team1']['name']} vs {match['team2']['name']}: {score_text}\n"

        if not scores:
            scores = "No live matches currently. 🏏"
        update.message.reply_text(scores)
    except Exception as e:
        logger.error(f"Error fetching live scores: {e}")
        update.message.reply_text("Error fetching live scores. Please try again later.")

# Upcoming matches
def upcoming_matches(update, context):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = response.json()
        matches_text = ""
        for match in data.get("matches", []):
            date = match.get('date', "Date not available")
            matches_text += f"{match['team1']['name']} vs {match['team2']['name']} on {date}\n"

        if not matches_text:
            matches_text = "No upcoming matches found. 🏏"
        update.message.reply_text(matches_text)
    except Exception as e:
        logger.error(f"Error fetching upcoming matches: {e}")
        update.message.reply_text("Error fetching upcoming matches. Please try again later.")

# Help command
def help_command(update, context):
    update.message.reply_text(
        "Available commands:\n"
        "/live - Get live cricket scores\n"
        "/matches - Get upcoming matches"
    )

# Main
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('live', live_scores))
    dispatcher.add_handler(CommandHandler('matches', upcoming_matches))
    dispatcher.add_handler(CommandHandler('help', help_command))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

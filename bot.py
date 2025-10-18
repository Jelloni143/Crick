import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_ENDPOINT = "https://api.cricketapi.com/v1/matches"
API_KEY = "YOUR_CRICKET_API_KEY"

logging.basicConfig(level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Cricket Live Score Bot! 🎉\n\nAvailable commands:\n/live - Get live cricket scores\n/matches - Get upcoming matches\n/help - Get help")

def live_scores(update, context):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = json.loads(response.text)
        scores = ""
        for match in data["matches"]:
            scores += f"{match['team1']['name']} vs {match['team2']['name']}: {match['score']}\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=scores)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching live scores. Please try again later.")

def upcoming_matches(update, context):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = json.loads(response.text)
        matches = ""
        for match in data["matches"]:
            matches += f"{match['team1']['name']} vs {match['team2']['name']}: {match['date']}\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=matches)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching upcoming matches. Please try again later.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Available commands:\n/live - Get live cricket scores\n/matches - Get upcoming matches")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    live_scores_handler = CommandHandler('live', live_scores)
    upcoming_matches_handler = CommandHandler('matches', upcoming_matches)
    help_handler = CommandHandler('help', help)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(live_scores_handler)
    dispatcher.add_handler(upcoming_matches_handler)
    dispatcher.add_handler(help_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
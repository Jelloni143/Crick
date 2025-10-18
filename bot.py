from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
import json

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_ENDPOINT = "https://api.cricketapi.com/v1/matches"
API_KEY = "YOUR_CRICKET_API_KEY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Cricket Live Score Bot! 🎉\n\nAvailable commands:\n/live - Get live cricket scores\n/matches - Get upcoming matches\n/help - Get help")

async def live_scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = json.loads(response.text)
        scores = ""
        for match in data["matches"]:
            scores += f"{match['team1']['name']} vs {match['team2']['name']}: {match['score']}\n"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=scores)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching live scores. Please try again later.")

async def upcoming_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
        data = json.loads(response.text)
        matches = ""
        for match in data["matches"]:
            matches += f"{match['team1']['name']} vs {match['team

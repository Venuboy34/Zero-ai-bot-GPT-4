from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests
import asyncio
import json

# Function to fetch GPT-4 response using the Teleservices API
def get_gpt4_response(telegram_id, user_message):
    url = "https://teleserviceapi.vercel.app/gpt"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": user_message,
        "id": str(telegram_id)  # Ensure the Telegram ID is passed as a string
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        # Extract message from the API response
        if response_data["status"] == "success":
            return response_data["message"]
        else:
            return "Sorry, I couldn't get a response from GPT-4. 😞"
    except Exception as e:
        print(f"Error occurred while fetching GPT-4 response: {e}")
        return "Sorry, there was an issue with the service. 😔"

# Function to handle /start command with emojis
async def start(update: Update, context):
    welcome_message = (
        "👋 Hello! I'm your assistant bot 🤖, powered by Zero AI ⚡\n\n"
        "Here's what I can do for you:\n"
        "🔹 **Answer your questions** using GPT-4 💬\n"
        "🔹 **Provide information** about various topics 📚\n"
        "🔹 **Assist with tasks** like reminders, notes, etc. 📝\n"
        "🔹 **Chat with you** and keep you company 🤗\n\n"
        "Feel free to ask me anything! 😄 I'm here to help! ✨\n\n"
        "Powered by Zero AI ⚡"
    )
    await update.message.reply_text(welcome_message)

# Function to handle user messages and send them to GPT-4
async def handle_message(update: Update, context):
    user_message = update.message.text  # Get user message
    telegram_id = update.message.from_user.id  # Get user's Telegram ID
    print("Received message:", user_message)  # Log the received message

    # Send a preliminary message indicating that the bot is processing the request
    await update.message.reply_text("🔄 Preparing your answer... Please wait a moment ⏳")

    # Simulate processing time (optional)
    await asyncio.sleep(1)  # You can adjust the delay as needed

    # Get response from GPT-4 API
    gpt4_response = get_gpt4_response(telegram_id, user_message)
    print("GPT-4 response:", gpt4_response)  # Log the GPT-4 response

    # Send GPT-4 response back to the user
    await update.message.reply_text(f"💬 {gpt4_response} ✨\n\nPowered by Zero AI ⚡")

# Main function to set up the bot
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
try:
    app.run_polling()
except Exception as e:
    print(f"Error occurred: {e}")

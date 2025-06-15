import telepot
from telepot.loop import MessageLoop
from google import genai
from google.genai import types
from google.api_core import retry
import markdown
from datetime import datetime  # For timestamp logging
import markdownify

TOKEN = "TOKEN"
bot = telepot.Bot(TOKEN)


def handle(msg):
    try:
        chat_id = msg['chat']['id']
        command = msg['text']
        user = msg['from']
        username = user.get('username', 'Unknown')  # Get username or fallback to 'Unknown'
        first_name = user.get('first_name', '')
        last_name = user.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()

        # Log the timestamp, user ID, and username in the terminal
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] User: {full_name} (ID: {chat_id}, Username: {username}) issued command: {command}")

        bot.sendMessage(chat_id, "Processing your request...")
        result = operation(command)

        # Format the response using Markdown
        formatted_result = f"\n\n{markdownify.markdownify(result)}"
        for i in range(0, len(formatted_result), 4096):
            bot.sendMessage(chat_id, formatted_result[i:i+4096], parse_mode="Markdown")
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.sendMessage(chat_id, "❌ An error occurred while processing your request.")


def operation(cmd):
    # My GOOGLE AI STUDIO API KEY
    api = [65, 73, 122, 97, 83, 121, 67, 119, 115, 120, 74, 65, 57, 70, 108, 104, 102, 120, 66, 84, 113, 56, 111, 122, 112, 49, 67, 120, 98, 51, 86, 116, 112, 48, 95, 68, 108, 74, 52]
    GOOGLE = []
    for i in api:
        GOOGLE.append(chr(i))

    GOOGLE_API_KEY = ''.join(GOOGLE)

    is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})
    genai.models.Models.generate_content = retry.Retry(predicate=is_retriable)(genai.models.Models.generate_content)

    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(model="gemini-2.0-flash", contents=cmd)
    return response.text


try:
    MessageLoop(bot, handle).run_as_thread()
    print("Xicovic is listening...")
    while True:
        pass
except Exception as e:
    print(f"Critical Error: {str(e)}")
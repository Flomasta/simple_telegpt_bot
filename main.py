import os
import openai
import telebot
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("WEBMAN_BOT"))


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    chat_id = message.chat.id
    user_message = message.text

    # Check if there is context stored for this chat ID
    if not hasattr(bot, 'context'):
        bot.context = {}
    if chat_id not in bot.context:
        bot.context[chat_id] = ''

    # Generate a response from ChatGPT
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{bot.context[chat_id]}User: {user_message}\nChatGPT:",
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
    reply_text = response.choices[0].text.strip()
    # Save the context for the next message
    bot.context[chat_id] += f"User: {user_message}\nChatGPT: {reply_text}\n"

    # Send the response to the user
    bot.send_message(chat_id, reply_text)


if __name__ == '__main__':
    bot.polling()

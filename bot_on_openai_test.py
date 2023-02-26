import openai
import telebot

token = '6081728663:AAFap3-a7_eL9RV9NQNcm5ijxcWP5VUTQFQ'

openai.api_key = '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'

bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.0
        #stop=["\n"]
    )
    bot.send_message(chat_id=message.chat.id, text=response['choices'][0]['text'])
    
bot.polling()
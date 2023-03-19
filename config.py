from aiogram import types
import os

# main
TELEGRAM_TOKEN = '6149748819:AAEjslsLQo2UMxnaL4H2sXfXHfn_QSDe_5o'
OPENAI_TOKEN = '5908266258:AAGjwTsYJr_mZS3UILDx8hzpiyhlHCIAquU'
# deployment test
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TELEGRAM_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=5000)
# db
MONGODB_CONNECTION_STRING = 'mongodb+srv://markiyanch:IiGPXXLIyyoTw4JL@cluster0.soznvr3.mongodb.net/?retryWrites=true&w=majority'
# payment
PAYMENT_TOKEN = '284685063:TEST:ZWIxMjMwYjVjMTcz' # stripe
PRICE = types.LabeledPrice(label="Купити", amount=200*100)
# logic
QUESTIONS_COUNT = 3
REFERRALS_NEEDED = 3
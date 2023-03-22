from aiogram import types
import os

# main
TELEGRAM_TOKEN = '5908266258:AAGjwTsYJr_mZS3UILDx8hzpiyhlHCIAquU'
OPENAI_TOKEN = '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'
# deployment test
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TELEGRAM_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get('PORT', '8443'))
# db
MONGODB_CONNECTION_STRING = 'mongodb+srv://markiyanch:IiGPXXLIyyoTw4JL@cluster0.soznvr3.mongodb.net/?retryWrites=true&w=majority'
# payment
PAYMENT_TOKEN = '284685063:TEST:ZWIxMjMwYjVjMTcz' # stripe
PRICE = types.LabeledPrice(label="Купити", amount=200*100)
# logic
QUESTIONS_COUNT = 3
REFERRALS_NEEDED = 3
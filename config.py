import os

# main
TELEGRAM_TOKEN = ''
OPENAI_TOKEN = ''
# deployment test
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TELEGRAM_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get('PORT', '8443'))
# db
MONGODB_CONNECTION_STRING = 'mongodb+srv://'
# payment
PAYMENT_TOKEN = '' # stripe
CHAT_ID = None
PURCHASED_ANSWERS = None
# logic
QUESTIONS_COUNT = 3
REFERRALS_NEEDED = 3

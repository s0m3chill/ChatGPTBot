import config
from main import *
from base64 import urlsafe_b64decode, urlsafe_b64encode

# setup
from aiogram import types
from aiogram.types.message import ContentType

# this is for testing purposes only, we'll need to create a db table for this shit
referral_count = {}  # dictionary to keep track of the referral count
referred_users = []  # list to keep track of referred users

# helpers
def encode_payload(payload: str) -> str:
    """Encode payload with URL-safe base64url."""
    payload = str(payload)
    bytes_payload: bytes = urlsafe_b64encode(payload.encode())
    str_payload = bytes_payload.decode()
    return str_payload.replace("=", "")

def decode_payload(payload: str) -> str:
    """Decode payload with URL-safe base64url."""
    payload += "=" * (4 - len(payload) % 4)
    result: bytes = urlsafe_b64decode(payload)
    return result.decode()

# commands
async def process_referrals_on_startup(message: types.Message):
    # Check if the message contains the referral parameter
    referral_user_id = referrals.decode_payload(message.get_args())
    if referral_user_id:
        referral_user_id = int(referral_user_id.split("_")[-1])
        # Check if the user is using own referral link
        if int(referral_user_id) == message.from_user.id:
            await message.reply('Ей ти, в морду дати? Своє реферал посилання не можна юзати')
        # Check if user was already referred
        elif referral_user_id in referrals.referred_users:
            await message.reply("Ви вже були зареферені") # this message is for debug purposes only, in final script, we'll remove that
        else:
            referrals.referred_users.append(referral_user_id)
            # Increment the referral counter for the user who referred someone
            if referrals.referral_count.get(int(referral_user_id)):
                referrals.referral_count[int(referral_user_id)] += 1
            else:
                referrals.referral_count[int(referral_user_id)] = 1

            # Check if the referral count has reached 3 and send congratulations message
            if referrals.referral_count.get(int(referral_user_id)) == 3:
                referrals.referral_count[int(referral_user_id)] = 0
                await bot.send_message(int(referral_user_id), "Вітаю! 3 людей долучились за допомогою твоєї рефералки!")

async def process_ref_link(message: types.Message):
    user_id = referrals.encode_payload(message.from_user.id)
    referral_link = f'Тут є <a href="tg://resolve?domain=asjhdkaksjbot&start={user_id}">реферальне посилання</a>'

    # Send the referral link to the user
    await bot.send_message(
        message.chat.id,
        referral_link,
        parse_mode='HTML'
    )

async def process_ref_status(message: types.Message):
    user_id = message.from_user.id

    # Get the referral count for the user
    if user_id in referrals.referral_count:
        count = referrals.referral_count[user_id]
    else:
        count = 0

    # Send the referral count to the user
    await bot.send_message(
        message.chat.id,
        f"{count} людей використали твоє посилання"
    )
import os
import logging
import requests
import datetime
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DATE_FORMAT='%Y-%m-%dT%H:%M:%S%z'
# The bot token and group chat ID
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
# The desired schedule time, defaulting to 18:00 (6 PM)
SCHEDULE_HOUR = int(os.getenv('DAILY_SCHEDULE_HOUR', 18))
SCHEDULE_MINUTE = int(os.getenv('DAILY_SCHEDULE_MINUTE', 0))
# The API URL
API_URL = "https://apis.smartenergy.at/market/v1/price"

def get_energy_prices():
    try:
        # Make the API request
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Parse the JSON data

        # Extract important information from JSON
        tariff = data.get('tariff', 'Unknown')
        unit = data.get('unit', 'Unknown')
        interval = data.get('interval', 0)
        price_data = data.get('data', [])

        # Format the API-data in a human-readable way
        price_info = f"Tarif: {tariff}\nEinheit: {unit}\nInterval: {interval} Minuten, Durchschnitt über 1 Stunde\n\n"

        for i in range(0, len(price_data), 4):  # use average of one hour
            one_hour = price_data[i:i+4]
            average_price_hour = sum([quarter['value'] for quarter in one_hour]) / 4
            date = datetime.datetime.strptime(one_hour[0]['date'], DATE_FORMAT)
            if date.hour == 0: # depending on the API, it returns more than one day (tomorrows data available after 17:00)
                price_info += f"Tag: {date.day}. {date.month}. {date.year} \n"
                price_info += f"Stunde: {date.hour}, Preis: {average_price_hour}{unit} \n"
            else:
                price_info += f"Stunde: {date.hour}, Preis: {average_price_hour}{unit} \n"

        return price_info

    except requests.RequestException as e:
        return f"Error fetching data from API: {e}"

async def scheduled_price_announcement(context: ContextTypes.DEFAULT_TYPE):
    price_info = get_energy_prices()

    if not CHANNEL_ID:
        logger.error("No CHANNEL_ID found in environment variables. Add it via docker run -e CHANNEL_ID=\"-12354\"")
        return
        
    await context.bot.send_message(chat_id=CHANNEL_ID, text=price_info)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Schedule the daily job at SCHEDULE_HOUR:SCHEDULE_MINUTE server time
    application.job_queue.run_daily(
        scheduled_price_announcement,
        time=datetime.time(hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE),
        name="daily_price"
    )

    # Start
    application.run_polling()

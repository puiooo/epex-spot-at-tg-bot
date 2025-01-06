# epex-spot-at-tg-bot

Telegram-Bot publishing the EPEX-Spot AT price everyday in human readable form.
See the bot in action here: https://t.me/+BvLGnMgijSMzNmE8 

# Libraries used

using python-telegram-bot for interaction with Telegram: https://python-telegram-bot.org/ 

# how-to use

If you want to deploy your own bot, use the included Dockerfile. Start it with:
`
docker run -d \
    --name epexspot_bot_container \
    -e BOT_TOKEN="YOUR TOKEN GOES HERE" \
    -e CHANNEL_ID="YOUR CHANNEL ID GOES HERE" \
    -e DAILY_SCHEDULE_HOUR="13" \
    -e DAILY_SCHEDULE_MINUTE="37" \
    epexspot_bot
`

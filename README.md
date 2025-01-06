# epex-spot-at-tg-bot

Telegram-Bot publishing the EPEX-Spot AT price everyday in human readable form.
If you are to lazy to deploy your own container or see the bot in action: https://t.me/+BvLGnMgijSMzNmE8 

# How to use

If you want to deploy your own bot, use the included Dockerfile. Start it with:

```
docker build -t epexspot_bot .
docker run -d \
        --name epexspot_bot_container \
        -e BOT_TOKEN="YOUR TOKEN GOES HERE" \
        -e CHANNEL_ID="YOUR CHANNEL ID GOES HERE" \
        -e DAILY_SCHEDULE_HOUR="13" \
        -e DAILY_SCHEDULE_MINUTE="37" \
        epexspot_bot
```

# Libraries used

using python-telegram-bot for interaction with Telegram: https://python-telegram-bot.org/ 

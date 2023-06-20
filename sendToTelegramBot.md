# How-to send information to a Telegram Bot
## Bot Creation (Telegram Part)
On Telegram, open a chat with @BotFather

Then write `/newbot` in the chat and send it.

Answer all questions sent by BotFather.

At the end, BotFather, will send you a API Token, save it somewhere.

## Chat ID resolution
Go in the search bar and search for the bot name you just created.

Click on the start button, send a basic "test" message.

Next, we need to find the Chat ID that exists between you and the bot.

To do so, just replace `{token}` by the token of the first step, in the following url `https://api.telegram.org/bot{token}/getUpdates` and paste it in any web browser.

You will find your chat id after the `"chat" :` part, just save it somewhere.

## Seeker
Append the token of the first step and the chat id of the second one, separated with `:`, the string should have 2 colons symbols `:` (including one existing in the token).

Either use `--telegram` seeker argument or `TELEGRAM` environment variable to provide the appended content.

Then all information/result will be send to you via the telegram bot

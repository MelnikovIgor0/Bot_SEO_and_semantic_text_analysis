# Telegram bot for SEO and semantic text analysis.

You can try to use this bot in TG: [@seo_and_semantic_analyzer_bot](https://t.me/seo_and_semantic_analyzer_bot).

This bot is presented as 2 microservices: bot and BLL.

## How to run?

1) Clone this repository:

```sh
git clone https://github.com/MelnikovIgor0/Bot_SEO_and_semantic_text_analysis.git .
```

2) Install all requirements:

```sh
pip install requirements.txt
```

3) Open `bot/config.json` and set token for TG-bot, url of API and DEBUG mode ON/OFF.

... HERE SPECIFY STAGES FOR BLL MICROSERVICE

4) Run the BLL microservice \<EXPLAIN HOW>

5) Run the TG bot:

```sh
cd bot
python bot.py
```
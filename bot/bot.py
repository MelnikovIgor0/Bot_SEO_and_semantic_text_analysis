import telebot
from BotConfig import BotConfig, parse_bot_config
from BLLInteractor import BLLInteractor
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat


config = parse_bot_config('config.json')
bot = telebot.TeleBot(config.telegram_api_token)
api_interactor = BLLInteractor(config.bll_api_url, config.debug)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome to SEO and Semantic Text Analyzer bot! Type /info to get more information.')

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message,
                 """I\'m a telegram bot for SEO and semantic text analysis. That\'s what I can do:
/start - starts the bot
/info - displaye info about me
/count <text> - counts the number of words in the sent text
/summary <text> - returns a summary of the sent text
/lemmatize <text> - lemmatize each word in the sent text
/stemming <text> - applies stemming to each word in the sent text
/translate <lang1> <lang2> <text> - translates <text> from <lang1> to <lang2>. Available languages:
    ru: russian
    en: england
    fr: french
    it: italian
    ge: german
    sp: spanish
    ch: chinese
    ja: japanese
/censure <text> - masks all obscene words in the sent text
""")

@bot.message_handler(commands=['count'])
def send_welcome(message):
    if len(message.text) < 7:
        bot.reply_to(message, 'There\'s no text!')
    else:
        bot.reply_to(message, api_interactor.count_words(message.text[7:]))


@bot.message_handler(commands=['lemmatize'])
def send_welcome(message):
    if len(message.text) < 11:
        bot.reply_to(message, 'There\'s no text!')
    else:
        bot.reply_to(message, api_interactor.lemmatize_text(message.text[11:]))

@bot.message_handler(commands=['stemming'])
def send_welcome(message):
    if len(message.text) < 10:
        bot.reply_to(message, 'There\'s no text!')
    else:
        bot.reply_to(message, api_interactor.stemming_text(message.text[10:]))

@bot.message_handler(commands=['translate'])
def send_welcome(message):
    if len(message.text) < 17:
        bot.reply_to(message, 'There\'s wrong format of message!')
    else:
        chat = GigaChat(
            credentials=config.gigachat_key,
            verify_ssl_certs=False)

        messages = [SystemMessage(
            content="Ты бот переводчик, выдавать в сообщении ничего кроме переведенного текста не нужно."
        ), HumanMessage(content=f"Translate from {message.text[11:13]} to {message.text[14:16]} '{message.text[17:]}'")]

        res = chat(messages)

        bot.reply_to(message, res.content)


@bot.message_handler(commands=['censure'])
def send_welcome(message):
    if len(message.text) < 9:
        bot.reply_to(message, 'There\'s no text!')
    else:
        bot.reply_to(message, api_interactor.censure_text(message.text[9:]))

@bot.message_handler(commands=['summary'])
def send_welcome(message):
    chat = GigaChat(
        credentials=config.gigachat_key,
        verify_ssl_certs=False)

    messages = [SystemMessage(
        content=""
    ), HumanMessage(content=f"summarize this text, try to keep within no more than 3 sentences: {message}")]

    res = chat(messages)

    bot.reply_to(message, res.content)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Undefined command!")



if __name__ == '__main__':
    bot.polling()

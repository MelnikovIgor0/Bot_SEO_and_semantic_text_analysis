import openai

def generate_lemmatization(text, openai_api_key):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Lemmatize the following text: {text}"}
        ]
    )
    lemmatized_text = response['choices'][0]['message']['content']
    return lemmatized_text

def register_lemmatize_handler(bot, openai_api_key):
    @bot.message_handler(commands=['lemmatize'])
    def lemmatize_text(message):
        if len(message.text) < 11:
            bot.reply_to(message, 'There\'s no text!')
        else:
            text_to_lemmatize = message.text[11:]
            lemmatized_text = generate_lemmatization(text_to_lemmatize, openai_api_key)
            bot.reply_to(message, lemmatized_text)

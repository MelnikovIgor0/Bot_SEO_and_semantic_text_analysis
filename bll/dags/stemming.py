import openai

def generate_stemming(text, openai_api_key):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Stem the following text: {text}"}
        ]
    )
    stemmed_text = response['choices'][0]['message']['content']
    return stemmed_text

def register_stemming_handler(bot, openai_api_key):
    @bot.message_handler(commands=['stemming'])
    def stemming_text(message):
        if len(message.text) < 10:
            bot.reply_to(message, 'There\'s no text!')
        else:
            text_to_stem = message.text[10:]
            stemmed_text = generate_stemming(text_to_stem, openai_api_key)
            bot.reply_to(message, stemmed_text)
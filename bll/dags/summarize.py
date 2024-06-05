import openai

def generate_summary(text, openai_api_key):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."}, # чего...
            {"role": "user", "content": f"Please summarize the following text: {text}"}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary

def register_summary_handler(bot, openai_api_key):
    @bot.message_handler(commands=['summary'])
    def summarize_text(message):
        if len(message.text) < 9:
            bot.reply_to(message, 'There\'s no text!')
        else:
            # Extract the text after the command '/summary '
            text_to_summarize = message.text[9:]
            summary = generate_summary(text_to_summarize, openai_api_key)
            bot.reply_to(message, summary)



import requests

def catch_error(f):
    def wrapped(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            return response
        except:
            return 'Error during response!'
    return wrapped

class BLLInteractor:
    def __init__(self, api_url: str, debug: bool):
        self.api_url = api_url
        self.debug = debug
    
    @catch_error
    def count_words(self, text: str) -> int:
        if self.debug:
            return 42
        else:
            return requests.get(self.api_url + '/count', params={'text': text}).json()['response']
    
    @catch_error
    def summarize_text(self, text: str) -> str:
        if self.debug:
            return "lorem ipsum"
        else:
            return requests.get(self.api_url + '/summarize', params={'text': text}).json()['response']
    
    @catch_error
    def lemmatize_text(self, text: str) -> str:
        if self.debug:
            return "lorem ipsum"
        else:
            return requests.get(self.api_url + '/lemmatize', params={'text': text}).json()['response']
    
    @catch_error
    def stemming_text(self, text: str) -> str:
        if self.debug:
            return "lorem ipsum"
        else:
            return requests.get(self.api_url + '/stemming', params={'text': text}).json()['response']
    
    @catch_error
    def translate_text(self, lang_from: str, lang_to: str, text: str) -> str:
        if self.debug:
            return "lorem ipsum"
        else:
            return requests.get(self.api_url + '/translate', params={'lang_from': lang_from, 'lang_to': lang_to, 'text': text}).json()['response']
    
    @catch_error
    def censure_text(self, text: str) -> str:
        if self.debug:
            return "lorem ipsum"
        else:
            return requests.get(self.api_url + '/censure', params={'text': text}).json()['response']

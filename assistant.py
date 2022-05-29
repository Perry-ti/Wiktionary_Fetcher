import requests
from bs4 import BeautifulSoup as bs

__LANGUAGES__ = (
    ('pl', 'polish'),
    ('ca', 'catalan'),
    ('cs', 'chech'),
    ('de', 'german'),
    ('et', 'estonian'),
    ('el', 'greek'),
    ('en', 'english'),
    ('es', 'spanish'),
    ('eo', 'esperanto'),
    ('fa', 'persian'),
    ('fr', 'french'),
    ('ko', 'korean'),
    ('hy', 'armenian'),
    ('hi', 'hindi'),
    ('io', 'ido'),
    ('id', 'indonesian'),
    ('it', 'italian'),
    ('kn', 'kannada'),
    ('ku', 'kurdish'),
    ('lt', 'lithuanian'),
    ('li', 'limburgish'),
    ('hu', 'hungarian'),
    ('mg', 'malagasy'),
    ('ml', 'malayalam'),
    ('nl', 'dutch'),
    ('ja', 'chinese'),
    ('nb', 'norvegian'),
    ('or', 'oriya'),
    ('uz', 'uzbek'),
    ('pt', 'portuguese'),
    ('ro', 'romanian'),
    ('ru', 'russian'),
    ('sr', 'serbian'),
    ('sh', 'serbo-Croatian'),
    ('fi', 'finnish'),
    ('sv', 'swedish'),
    ('ta', 'tamil'),
    ('te', 'telugu'),
    ('th', 'thai'),
    ('tr', 'turkish'),
    ('vi', 'vietnamese'),
    ('zh', 'japanese'),
    ('my', 'burmese')
    )

class Language_Not_Supported(Exception):
    """Raised when the language of interest is not supported"""
    def __init__(self,lang):
        super().__init__(f"The language {lang} is not supported...")

class Word_Not_Set(Exception):

    def __init(self):
        super().__init__("There is no word set yet...")

class URL_Not_Crafted(Exception):

    def __init__(self):
        super().__init__("The URL is not crafted yet...")

class Wiktionary_Fetcher_Not_Complete(Exception):

    def __init__(self):
        super().__init__("Wiktionary_Fetcher not complete...")
class Wiktionary_Fetcher:

    __lang = None
    __word = None
    __url = None
    __response = None
    __complete = None

    def __init__(self,lang="en"):
    
        self.__lang = self.__lang_acronym(lang)
        self.__check_and_set_complete()
    

    #as soon as a new word is set, the url needs to be updated
    def word_of_interest(self,word):
        self.__word = word
        self.__craft_url()
        self.__check_and_set_complete()

    def language_of_interest(self,lang="en"):
        self.__lang = self.__lang_acronym(lang)
        if not self.__word is None:
            self.__craft_url()
            self.__check_and_set_complete()

    def send_request(self):
        if not self.__url is None:
            with requests.get(self.__url) as request:
                self.__response = request

            self.__check_and_set_complete()
        else:
            raise URL_Not_Crafted

    def __check_and_set_complete(self):
        if self.__word and self.__lang and self.__url:
            if not self.__response is None:
                self.__complete = True
        else:
            self.__complete = False
        
    def __lang_acronym(self,lang):

        lang = lang.lower()
        
        for lan in __LANGUAGES__:
            if lang in lan:
                self.__check_and_set_complete()
                return lan[0]

        raise Language_Not_Supported

    def __craft_url(self):
        if self.__word is None:
            raise Word_Not_Set
        else:
            self.__url = f"https://{self.__lang}.wiktionary.org/wiki/{self.__word}"
            self.__check_and_set_complete()
        
    @property
    def language(self):
        return self.__lang

    @property
    def word(self):
        return self.__word

    @property
    def url(self):
        return self.__url

    @property
    def response(self):
        return self.__response

    @property
    def complete(self):
        return self.__complete

    @property
    def object_status(self):
        return f"Language: {str(self.__lang)}\tWord: {str(self.__word)}\tURL: {str(self.__url)}\tResponse: {str(self.__response)}\tComplete: {str(self.__complete)}"

class Wiktionary_Response_Handler:

    __status_code = None
    __html = None
    __enable_Handler = False

    def __init__(self, wf: Wiktionary_Fetcher):

        if not wf.complete:
            raise Wiktionary_Fetcher_Not_Complete
        else:
            self.__status_code = wf.response.status_code
            self.__html = bs(wf.response.text,"html.parser")

            self.__check_status()

    def __check_status(self):
        self.__enable_Handler =  True if str(self.__status_code) == 200 else False

    @property
    def status_code(self):
        return self.__status_code
    
    @property
    def html(self):
        return self.__html

    @property
    def found(self):
        return self.__word_found


#just for debug
if __name__ == "__main__":

    english_request = Wiktionary_Fetcher("english")
    english_request.word_of_interest("lemon")

    print(english_request.url)

    english_request.word_of_interest("uzeti")

    print(english_request.url)
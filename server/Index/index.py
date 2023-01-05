import json
import string
import random

class Index:
    
    filename = './Index/index.json'
    
    data = {
        # 'documents': {
        #     'asdasda' : {
        #         'doc_id': 'asdasda',
        #         'text': 'Hi everyone, today is wednesday!'
        #     },
        #     'jfhasdh' : {
        #         'doc_id': 'jfhasdh',
        #         'text': 'wednesday is today!'
        #     }
        # },
        # 'tokens': {
        #     'hi' : ['asdasda'],
        #     'everyone': ['asdasda'],
        #     'today': ['asdasda', 'jfhasdh'],
        #     'is': ['asdasda', 'jfhasdh'],
        #     'wednesday': ['asdasda', 'jfhasdh']
        # }
    }
    
    def __init__(self) -> None:
        pass
    
    def readFromFile(self):
        file = open(self.filename)
        self.data = json.load(file)
        file.close()

    def saveToFile(self):
        json_object = json.dumps(self.data, indent=4)
        with open(self.filename, "w") as file:
            file.write(json_object)
    
    @staticmethod
    def getRandomId(length=7):
        id = "".join(random.choices(string.ascii_letters + string.digits, k=length))
        return id
    
    @staticmethod
    def extractTokensFromString(str):
        str = str.lower()
        
        # Allowed Characters are [a-z],[A-Z] & [0-9] only
        allowed_characters_for_tokenization = string.ascii_lowercase + string.digits
        
        for character in str:
            if character not in allowed_characters_for_tokenization:
                str = str.replace(character, '')
            
        tokens = str.split(' ')
        
        # Remove empty/useless tokens
        tokens = [token for token in tokens if token and token != '']
        return tokens
    
    
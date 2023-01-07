import json
import string
import random

from collections import Counter
from Ingestor.models import YoutubeVideo
from Ingestor.util import serializeYoutubeVideoToJson

class Index:

    filename = './Index/index.json'

    data = {}

    def __init__(self):
        self.readFromFile()
        if 'documents' not in self.data or 'tokens' not in self.data:
            self.data = {
                'documents': {},
                'tokens': {}
            }
            self.saveToFile()

    def readFromFile(self):
        try:
            file = open(self.filename)
            self.data = json.load(file)
            file.close()
        except Exception as exception:
            print(
                f'Error in Index module, in readFromFile ====> {str(exception)}')

    def saveToFile(self):
        try:
            json_object = json.dumps(self.data, indent=4)
            with open(self.filename, "w") as file:
                file.write(json_object)
        except Exception as exception:
            print(
                f'Exception in Index module, in saveToFile ====> {str(exception)}')

    @staticmethod
    def getRandomId(length: int = 7) -> str:
        id = "".join(random.choices(
            string.ascii_letters + string.digits, k=length))
        return id

    @staticmethod
    def extractTokensFromString(str) -> list[str]:
        str = str.lower()

        # Allowed Characters are [a-z],[A-Z] & [0-9] only
        allowed_characters_for_tokenization = string.ascii_lowercase + string.digits + ' '

        for character in str:
            if character not in allowed_characters_for_tokenization:
                str = str.replace(character, ' ')

        tokens = str.split(' ')

        # Remove empty/useless tokens
        tokens = [token for token in tokens if token and token != '']
        
        # Remove duplicates
        tokens = list(dict.fromkeys(tokens))
        
        return tokens

    def addObjectToIndex(self, youtubevideo: YoutubeVideo):
        '''
        Add a youtube video object to the index.

        Do not use for other objects
        '''
        self.readFromFile()

        documents = self.data['documents']
        tokens = self.data['tokens']

        text = youtubevideo.title + ' ' + youtubevideo.description

        # Handle the case where same object might be indexed again
        for document_id in documents:
            if documents[document_id]['id'] == youtubevideo.pk:
                return

        doc_id = self.getRandomId(length=10)
        extracted_tokens = self.extractTokensFromString(str=text)

        documents[doc_id] = {
            'doc_id': doc_id,
            'text': text,
            'id': youtubevideo.pk
        }

        for token in extracted_tokens:
            if token in tokens:
                tokens[token].append(doc_id)
            else:
                tokens[token] = [doc_id]

        self.saveToFile()

    def removeObjectFromIndex(self, youtubevideo: YoutubeVideo):
        '''
        Remove a youtube video object from the index

        Do not use for other objects
        '''
        self.readFromFile()

        documents = self.data['documents']
        tokens = self.data['tokens']

        for document_id in documents:
            if documents[document_id]['id'] == youtubevideo.pk:
                doc_id = document_id
                text = documents[document_id]['text']

        # The object is not present in index
        if not doc_id:
            return

        del documents[doc_id]

        extracted_tokens = self.extractTokensFromString(str=text)

        for token in extracted_tokens:
            if token in tokens and doc_id in tokens[token]:
                tokens[token].remove(doc_id)
                if not tokens[token]:
                    del tokens[token]

        self.saveToFile()

    def search(self, query: str, size: int = 50) -> list[dict]:
        '''
        Search in the index for objects that match the query
        '''
        self.readFromFile()

        documents = self.data['documents']
        tokens = self.data['tokens']

        query_tokens = self.extractTokensFromString(query)

        result_ids = []

        for token in query_tokens:
            if token in tokens:
                result_ids.extend([documents[document_id]['id']
                                  for document_id in tokens[token]])

        # Sort the list based on the number of occurences in the list
        result_ids.sort(key=Counter(result_ids).get, reverse=True)

        # Make the list unique
        result_ids = list(dict.fromkeys(result_ids))

        # Limit the results
        result_ids = result_ids[0:size]

        result = [serializeYoutubeVideoToJson(YoutubeVideo.objects.get(
            pk=result_id)) for result_id in result_ids]

        return result
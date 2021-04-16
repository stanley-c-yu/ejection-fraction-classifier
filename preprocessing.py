"""
Contains methods for cleaning and reorganizing textual data for assembling a dataset 
for pattern searching and or for assembling a training dataset for machine learning 
purposes.  
"""
## ----------------------------------------------------------------------------##
## Import Dependencies ##
import spacy
nlp = spacy.load('en_core_web_sm') # Load English model package using 'en' shortcut link.  By default, we're using the en_core_web_sm model.
import re
import json

from spacy.matcher import Matcher
## ----------------------------------------------------------------------------##
# Import Search Patterns for Ejection Fraction phrasing
filename = "patterns.json"
with open(filename) as f_obj:
    patterns = json.load(f_obj)
## ----------------------------------------------------------------------------##
## Preprocessing Code ## 

class Preprocessing: 
    """ Contains methods for preparing HHC textual data for analysis """ 

    def clean(self, text):
        """ Removes special characters and other quirks from the notes that might make it difficult to search for info. """
        text = re.sub('•', '', text) # Get rid of bullet points 
        text = re.sub('-', ' ', text) # Get rid of dashes and replace with a space
        text = re.sub('%', '', text) # Get rid of percentage symbols
        text = re.sub('\.', '', text) # Get rid of percentage symbols
        text = re.sub(':', '', text) # Get rid of colon symbols
        text = re.sub("'", '', text) # get rid of apostophe symbols

        return text 

    def standard_spacing(self, text): 
        """ Standardizes all texts to have single spacing. """
        text = " ".join(text.split())
        return text

    def find_pattern(self, text):
        ''' 
        Searches through records for excerpts of text that match our patterns.  
        
        Args: 
            text: A text document we are interested in searching through for matching excerpts. 
            patterns: A dictionary of patterns.  Each pattern has a value that is a list of dictionaries.  This list of
            dictionaries are SpaCy patterns.  
        Output: 
            A list of excerpts that match our patterns from the original document.  
        '''
        mentions = []
        pattern_list = []
        
        doc = nlp(text)
        
        # Matcher class object
        matcher = Matcher(nlp.vocab, validate=True)
        # OLD: loop works for earlier version of SpaCy
        # for key, value in patterns.items():
        #     matcher.add(key, None, value)   
        # Replacement
        for value in patterns.values():
            pattern_list.append(value)
        
        matcher.add("ef_patterns", pattern_list)
        
        matches = matcher(doc)
        
        # finding patterns in the text
        for i in range(0, len(matches)):
            # match: id, start, end
            token = doc[matches[i][1]:matches[i][2]]
            # append token to list 
            mentions.append(str(token))
            
        return mentions

    def second_clean(self, text): 
        '''
        Removes special characters and other quirks from the notes that might make it more difficult to search for info.  Intended for the 'Mentions" Column.  

        Args:
            text: A text document we are interested in clearning of special characters, namely square brackets and single quotation marks.  
        Output:
            Cleaned text stripped of square brackets and single quotation marks.  
        '''
        text = str(text)
        text = re.sub(r'\[', '', text)
        text = re.sub(r'\]', '', text)
        text = re.sub(r"'", '', text)

        return text
       
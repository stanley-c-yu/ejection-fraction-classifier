import re 
import pandas as pd
from tqdm import tqdm

class Search: 
    ''' Contains methods for searching through the 'mentions' column for ejection fraction measurement methods. '''				
		
    def simpson_biplane(self, text): 
        """ Takes a text string as an argument and tries to find a match with 2D Simpson Biplane""" 
        text = text.lower()
        method = re.findall(r'2d simpson[s]? biplane', text)
        if len(method) == 0: 
            method = re.findall(r'biplane', text)
            if len(method) == 0:
                return "None"
            else: 
                method = method.pop()
                return "2d simpson biplane"
        method = method.pop()
        return method

    def imaging(self, text):
        """ Takes a text string as an argument and tries to find a match with 3D Imaging"""
        text = text.lower()
        method = re.findall(r'3d imaging', text)
        if len(method) == 0: 
            method = re.findall(r'imaging', text)
            if len(method) == 0:
                return "None"
            else: 
                method = method.pop()
                return "3d imaging"
        method = method.pop()
        return method

    def find_method(self, text): 
        """ Attempts to find the method employed for ef measurement from excerpt """
        result = self.simpson_biplane(text)
        if result == "None": 
            result = self.imaging(text)
            if result == "None": 
                return "None"
            else: 
                return result
        else: 
            return result

    def find_numbers(self, text):
        """ Attempt to find ejection fraction numbers from excerpts. """
        result = re.findall(r'\d{2,3}', text)
        for i in range(len(result)):
            if len(result[i]) > 2:
                result[i] = result[i][:2] + "." + result[i][2:]
        return result

    def find_measurement(self, text):
        """ Attempts to extract the lower and upper ejection fraction measurements """
        results = self.find_numbers(text)
        if len(results) == 1:
            result = results.pop()
            result = float(result)
            l_bound = result 
            u_bound = result
            return l_bound, u_bound
        elif len(results) > 1:
            tmp = []
            for num in results:
                num = float(num)
                tmp.append(num)
            tmp.sort()
            l_bound = tmp[0]
            u_bound = tmp[len(tmp)-1]
            return l_bound, u_bound
        else:
            return 0, 0

    def attach_measurement(self, df):
        """
        Adds measurements to each record by: 
            1. Converting dataframe to a dictionary. 
            2. For each record, creates a new key-value pair for lower bound, and then another for the upper bound. 
            3. Converts back into a data frame 
            4. Saves 
        """
        records = df.to_dict(orient="records")
        for rec in records:
            text = rec['MENTIONS']
            l_bound, u_bound = self.find_measurement(text)
            rec['LOWER EF'] = l_bound
            rec['UPPER EF'] = u_bound 
        records = pd.DataFrame(records)
        return records


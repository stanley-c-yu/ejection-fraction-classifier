import re 
import pandas as pd
from tqdm import tqdm

class Finder: 
	""" Contains methods for classifying documents as mentioning ejection fraction or not """
	
	def find(self, mode, text): 
		""" Takes a text string as an argument and tried to find a match with Ejection Fraction or EF """
		if mode == 1:
			word = "ejection fraction"
			alt = "ef"
		elif mode == 2:
			word = "left ventricular ejection fraction"
			alt = "lvef"
		elif mode == 3:
			word = "right ventricular ejection fraction"
			alt = "rvef"	
			
		text = text.lower()
		measure = re.findall(r'%s' % word, text)
		if len(measure) == 0:
			measure = re.findall(r'%s' % alt, text)
			if len(measure) == 0:
				return "None"
			else:
				measure = measure.pop()
				return "ejection fraction"
		measure = measure.pop()
		return measure

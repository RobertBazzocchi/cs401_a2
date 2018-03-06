import re
import argparse # ADDED
import os # ADDED
import json # ADDED
import html # ADDED
import spacy # ADDED
import time # ADDED

global punctuation, contractions
punctuation = r"[\w]+|[,:;()+=\"<>\-]|(?:\'\')"
contractions = r"[\w]+[,:;()+=\"<>\-]|j'+(?=\w+)|l'+(?=\w+)|qu'+(?=\w+)|puisqu'+(?=\w+)|lorsqu'+(?=\w+)|\w+'\w+|\w+|[^\s\w]" #|   +|n't|\w+(?=n't)|\w+|[^\s\w]" # '\w+|n't|\w+(?=n't)|\w+|[^\s\w]"

def preprocess(in_sentence, language):
	""" 
	This function preprocesses the input text according to language-specific rules.
	Specifically, we separate contractions according to the source language, convert
	all tokens to lower-case, and separate end-of-sentence punctuation 

	INPUTS:
	in_sentence : (string) the original sentence to be processed
	language	: (string) either 'e' (English) or 'f' (French)
				   Language of in_sentence
				   
	OUTPUT:
	out_sentence: (string) the modified sentence
	"""
	# CONVERT TO LOWER CASE
	in_sentence = in_sentence.lower()

	# SEPARATE PUNCTUATION (i.e., commas, colons and semicolons, parentheses, dashes between parentheses, mathematical operators (e.g., +, -, <, >, =), and quotation marks.)
	p = False
	print("_______________________INPUT SENTENCE_______________________")
	print(in_sentence)
	p = True
	

	# PROBLEM: IS NOT SPLITTING THE '' FROM THE BEGINNING OF QUOTES, ONLY SPLITS THE END
	global punctuation
	punctuation = r"[\w']+|[,:;()+=\"<>\-]|(?:\'\')" #[!?.\_\/$&\*+=()@%:;<>\[\]\^\\\#\"\}\{\~\|\-]+"
	sep_punc = re.findall(punctuation, in_sentence)
	out_sentence = " ".join(sep_punc)

	# PROBLEM: STILL HAVE TO ACCOUNT FOR DOUBLE QUOTES
	if language == 'f':
		global contractions
		sep_clitics = re.findall(contractions, out_sentence)
		out_sentence = " ".join(sep_clitics)

	if p:
		print("_______________________OUTPUT SENTENCE_______________________")
		print(out_sentence)

	return out_sentence

def main():
    indir = '../data/Hansard/Training/'# '/u/cs401/A1/data/' # CHANGE FOR SUBMISSION

    for subdir, dirs, files in os.walk(indir):
        for file in files:
            if file == ".DS_Store":
                continue
            if file.endswith(".e"): # DETERMINE THE LANGUAGE AND SET THE LANGUAGE VARIABLE
            	language = "e"
            else:
            	language = "f"

            fullFile = os.path.join(subdir, file)
            # print("Processing " + fullFile)

            path = '../data/Hansard/Training/'+file
            hansard_file = open(path,'r')

            for sentence in hansard_file.readlines():
            	preprocess(sentence,language)
main()

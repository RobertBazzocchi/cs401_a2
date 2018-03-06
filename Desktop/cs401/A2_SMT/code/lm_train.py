from preprocess import *
import pickle
import os
import string
def compute_unigram_dict(data_str):
	for word in data_str:
		if word not in string.punctuation:
			print(word)
def lm_train(data_dir, language, fn_LM):
	"""
	This function reads data from data_dir, computes unigram and bigram counts,
	and writes the result to fn_LM

	INPUTS:

	data_dir	: (string) The top-level directory continaing the data from which
					to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
	language	: (string) either 'e' (English) or 'f' (French)
	fn_LM		: (string) the location to save the language model once trained

	OUTPUT

	LM			: (dictionary) a specialized language model

	The file fn_LM must contain the data structured called "LM", which is a dictionary
	having two fields: 'uni' and 'bi', each of which holds sub-structures which 
	incorporate unigram or bigram counts

	e.g., LM['uni']['word'] = 5 		# The word 'word' appears 5 times
		  LM['bi']['word']['bird'] = 2 	# The bigram 'word bird' appears 2 times.
	"""

	data_list = [] # WILL CONTAIN ALL SENTENCES OF EACH .f or .e FILE AS A LIST
	# ITERATE THROUGH EACH FILE IN THE TRAINING DATA
	for subdir, dirs, files in os.walk(data_dir):
	    for file in files:
	        print("Processing file: " + file)
	        if file == ".DS_Store":
	            continue
	        if file.endswith(language): # CHECK IF FILE IS OF CORRECT LANGUAGE
	        	process = True
	        else:
	        	process = False

	        if process: # PROCESS SENTENES IN THE FILE
	            path = '../data/Hansard/Training/'+file
	            hansard_file = open(path,'r')

	            for sentence in hansard_file.readlines():
	            	data_list.append(preprocess(sentence,language))
	
	print(data_list)
	data_str = ' '.join(data_list)
	compute_unigram_dict(data_str)

	return
	#Save Model
	with open(fn_LM+'.pickle', 'wb') as handle:
	    pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
	    
	return language_model

def main():
	data_dir = '../data/Hansard/Training/'
	language = "e"
	fn_LM = '../models/'+language+'_language_model'
	lm_train(data_dir, language, fn_LM) # CHANGE FOR SUBMISSION

main()




















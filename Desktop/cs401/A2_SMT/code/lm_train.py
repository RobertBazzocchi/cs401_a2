from preprocess import *
import pickle
import os
import string

def compute_dicts(sentence, uni_dict, bi_dict):
	"""
	INPUTS:
	sentence	: (string) a sentences from the training set
	uni_dict  	: (dictionary) containing the unigram model data
	bi_dict 	: (dictionary) containing the bigram model data

	OUTPUT:
	uni_dict	: (dictionary) modified unigram model including data from sentence
	bi_dict		: (dictionary) modified bigram model including data from sentence
	"""
	sentence_tokens = sentence.split()
	global prev_token

	for token in sentence_tokens: # SPLITS THE DATA INTO WORDS AND PUNCTUATION
		
		# __________BUILD UNIGRAM__________
		if token not in uni_dict:
			uni_dict[token] = 1
		else:
			uni_dict[token] += 1

		#___________BUILD BIGRAM___________
		if token == "SENTSTART": # CHECK IF THIS IS THE FIRST TOKEN ITERATION
			if token not in bi_dict:
				bi_dict[token] = {}
			prev_token = token
		if token not in bi_dict[prev_token]: # CHECK IF BIGRAM EXISTS IN DICT ALREADY
			bi_dict[prev_token][token] = 1 # SET TO 1 IF IT DOES NOT
		else:
			bi_dict[prev_token][token] += 1 # ADD 1 IF IT DOES

		if token not in bi_dict:
			bi_dict[token] = {}
		prev_token = token
	return uni_dict, bi_dict

def get_gram_counts(data_dir,language):

	# A LIST THATWILL CONTAIN ALL SENTENCES OF EACH .f or .e FILE AS A LIST
	data_list = []
	uni_dict = {}
	bi_dict = {}

	# ITERATE THROUGH EACH FILE IN THE TRAINING DATA
	for subdir, dirs, files in os.walk(data_dir):
	    for file in files:
	        if file == ".DS_Store":
	            continue
	        if file.endswith(language): # CHECK IF FILE IS OF CORRECT LANGUAGE
	        	process = True
	        else:
	        	process = False

	        if process: # PROCESS SENTENES IN THE FILE
	            print("Processing file: " + file)
	            path = data_dir+file
	            hansard_file = open(path,'r')

	            for sentence in hansard_file.readlines():
	            	processed_sentence = preprocess(sentence,language)
	            	data_list.append(processed_sentence)
	            	uni_dict, bi_dict = compute_dicts(processed_sentence,uni_dict,bi_dict)

	return data_list, uni_dict, bi_dict

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
	"""
	# INITIALIZE AN EMPTY LM DICTIONARY
	LM = {}

	# DECLARE prev_token AS A GLOBAL VARIABLE AND INITIALIZE TO NONE
	global prev_token
	prev_token = None

	# GET UNIGRAM AND BIGRAM MODELS FROM FUNCTION get_gram_counts
	data_list, uni_dict, bi_dict = get_gram_counts(data_dir,language)

	# AN ADDITIONAL RETURNED VARIABLE THAT CONTAINS ALL SENTENCES IN ONE STRING
	data_str = ' '.join(data_list)

	# SET THE KEYS OF LM TO BE THE RETURNED DICTIONARIES FROM get_gram_counts
	LM["uni"] = uni_dict
	LM["bi"] = bi_dict

	# SAVE THE MODEL
	with open(fn_LM+'.pickle', 'wb') as handle:
	    pickle.dump(LM, handle, protocol=pickle.HIGHEST_PROTOCOL)
	    
	return LM

def main():
	data_dir = '../data/Hansard/Training/'
	for language in ["e","f"]:
		fn_LM = '../models/'+language+'_language_model'
		LM = lm_train(data_dir, language, fn_LM) # CHANGE FOR SUBMISSION

def load_LMs(LM_path):
	LM = pickle.load(open(LM_path, "rb"))
	return LM

#________________________RUN EACH PART________________________
# 1. RUN main() TO BUILD AND SAVE THE FRENCH AND ENGLISH LMS FROM HANSARD TRAINING DATA
# main()

# 2. RUN load_LMs() TO LOAD LMs
# e_LM = load_LMs("../models/e_language_model.pickle") # LOAD ENGLISH LM
# f_LM = load_LMs("../models/f_language_model.pickle") # LOAD FRENCH LM















from preprocess import *
import pickle
import os
import string

# def compute_unigram_dict(data_str):
# 	"""
# 	INPUTS:
# 	data_str	: (string) all the sentences in a training set for a language model

# 	OUTPUT:
# 	uni_dict	: (dictionary) with words as keys and their unigram count as values
# 	"""

# 	uni_dict = {}
# 	i = 0
# 	data_str_tokens = data_str.split()

# 	for token in data_str_tokens: # SPLITS THE DATA INTO WORDS AND PUNCTUATION
# 		if token in ["(",")"]: # ACCOUNT FOR PARANTHESES ERROR
# 			token = "\\"+token
# 		uni_dict[token] = len(re.findall(token,data_str))
# 		if i %500 == 0:
# 			print(uni_dict)
# 		i+=1
# 	return uni_dict

def compute_unigram_dict(sentence, uni_dict, bi_dict):
	"""
	INPUTS:
	data_str	: (string) all the sentences in a training set for a language model

	OUTPUT:
	uni_dict	: (dictionary) with words as keys and their unigram count as values
	"""
	sentence_tokens = sentence.split()

	for token in sentence_tokens: # SPLITS THE DATA INTO WORDS AND PUNCTUATION
		if token not in uni_dict:
			uni_dict[token] = 1
		else:
			uni_dict[token] += 1

	return uni_dict, bi_dict

def bi_gram():
	prev_token = None
	for token in sentence_tokens:
		if not prev_token:
			prev_token = token
			continue
		
		if prev_token not in bi_dict:
			bi_dict[prev_token] = {} 

		if token not in bi_dict:
			bi_dict[token] = 2

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
	            path = '../data/Hansard/Training/'+file
	            hansard_file = open(path,'r')

	            for sentence in hansard_file.readlines():
	            	processed_sentence = preprocess(sentence,language)
	            	data_list.append(processed_sentence)
	            	uni_dict, bi_dict = compute_unigram_dict(processed_sentence,uni_dict,bi_dict)

	return data_list, uni_dict

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

	# CHECK IF DATA_LIST WAS ALREADY COMPUTED
	# if os.path.isfile("data_list.txt"):
	# 	with open("data_list.txt", "rb") as fp:   # Unpickling
	# 		data_list = pickle.load(fp)
	# else:
	# 	data_list, uni_dict = get_gram_counts(data_dir,language)
	# 	with open("data_list.txt", "wb") as fp:   #Pickling
	# 		pickle.dump(data_list, fp)

	data_list, uni_dict = get_gram_counts(data_dir,language)
	data_str = ' '.join(data_list)
	# uni_val = compute_unigram_dict(data_str)

	# print(uni_dict[")"])
	# print(data_str.count(")"))

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




















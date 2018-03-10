from preprocess import *
from lm_train import *
import math
from math import log2

def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
	"""
	Compute the LOG probability of a sentence, given a language model and whether or not to
	apply add-delta smoothing
	
	INPUTS:
	sentence :	(string) The PROCESSED sentence whose probability we wish to compute
	LM :		(dictionary) The LM structure (not the filename)
	smoothing : (boolean) True for add-delta smoothing, False for no smoothing
	delta : 	(float) smoothing parameter where 0<delta<=1
	vocabSize :	(int) the number of words in the vocabulary
	
	OUTPUT:
	log_prob :	(float) log probability of sentence
	"""

	# EXTRACT THE UNIGRAM AND BIGRAM DICTIONARIES FROM LM
	uni_dict = LM["uni"]
	bi_dict = LM["bi"]
	p_sentence = 1
	prev_token = None

	# COMPUTE AND RETURN THE ML ESTIMATE
	sentence_tokens = sentence.split()

	# COMPUTE PROBABILITY OF SENTENCE
	for token in sentence_tokens: # SPLITS THE DATA INTO WORDS AND PUNCTUATION
		if token == "SENTSTART": # ASSUMING STARTSENT INCLUDED IN PROCESSED SENTENCE
			prev_token = token
			continue
		else:
			try:
				if smoothing:
					p_bigram = (bi_dict[prev_token][token]+delta)/(uni_dict[prev_token]+delta*vocabSize) # HAD THIS BEFORE: uni_dict[prev_token]/bi_dict[prev_token][token]
				else:
					p_bigram = (bi_dict[prev_token][token])/(uni_dict[prev_token]) # HAD THIS BEFORE: uni_dict[prev_token]/bi_dict[prev_token][token]
			except KeyError:
				# print("KeyError: No bigram \"{} {}\".".format(prev_token,token))
				p_bigram = 0
				log_prob = float('-inf')
				return log_prob	# RETURNS -inf LOG PROBABILITY IF BIGRAM DOES NOT EXIST

			p_sentence *= p_bigram

		prev_token = token # UPDATE prev_token TO CURRENT token FOR NEXT ITERATION
	
	# TAKE THE LOG OF THE PROBABILITY OF THE SENTENCE AND RETURN
	log_prob = math.log(p_sentence,2)
	return log_prob

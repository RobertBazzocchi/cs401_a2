import math
from preprocess import *
from lm_train import *
from log_prob import *
from align_ibm1 import *
from decode import *
import csv # ADDED

def BLEU_score(candidate, references, n):
	"""
	Compute the LOG probability of a sentence, given a language model and whether or not to
	apply add-delta smoothing
	
	INPUTS:
	sentence :	(string) Candidate sentence.  "SENTSTART i am hungry SENTEND"
	references:	(list) List containing reference sentences. ["SENTSTART je suis faim SENTEND", "SENTSTART nous sommes faime SENTEND"]
	n :			(int) one of 1,2,3. N-Gram level.

	
	OUTPUT:
	bleu_score :	(float) The BLEU score
	"""

	words = candidate.split() # A LIST OF WORDS IN THE CANDIDATE SENTENCE
	res = 1

	if n > 0:
		p1 = compute_p1(words,references)
		res *= p1
	if n > 1:
		p2 = compute_p2(words,references)
		res *= p2
	if n > 2:
		p3 = compute_p3(words,references)
		res *= p3

	BP = compute_brevity_penalty(words,references)
	bleu_score = float(BP*math.pow(res,(1/n)))

	return bleu_score

def compute_p1(words,references):
	N = len(words) # NUMBER OF WORDS IN THE CANDIDATE
	C = 0
	updated = False
	for i in range(N):
		unigram = words[i]
		for ref in references:
			ref_words = ref.split()
			ref_N = len(ref_words)
			for j in range(ref_N):
				ref_unigram = ref_words[j]
				if unigram == ref_unigram:
					C += 1
					updated = True
					break
			if updated:
				updated = False
				break
	p1 = float(C/N)
	return p1

def compute_p2(words,references):
	N = len(words) - 1 # NUMBER OF BIGRAMS IN THE CANDIDATE: # OF WORDS - 1
	C = 0
	updated = False
	for i in range(N):
		bigram = [words[i], words[i+1]]
		for ref in references:
			ref_words = ref.split()
			ref_N = len(ref_words) - 1
			for j in range(ref_N):
				ref_bigram = [ref_words[j],ref_words[j+1]]
				if bigram == ref_bigram:
					C += 1
					updated = True
					break
			if updated:
				updated = False
				break
	p2 = float(C/N)
	return p2

def compute_p3(words,references):
	N = len(words) - 2 # NUMBER OF TRIGRAMS IN THE CANDIDATE: # OF WORDS - 2
	C = 0
	updated = False
	for i in range(N):
		trigram = [words[i], words[i+1],[words[i+2]]]
		for ref in references:
			ref_words = ref.split()
			ref_N = len(ref_words) - 2
			for j in range(ref_N):
				ref_trigram = [ref_words[j],ref_words[j+1],ref_words[j+2]]
				if trigram == ref_trigram:
					C += 1
					updated = True
					break
			if updated:
				updated = False
				break
	p3 = float(C/N)
	return p3

def compute_brevity_penalty(words,references):
	N = len(words)
	min_diff = float(math.inf)

	# COMPUTE BREVITY
	for ref in references:
		N_ref = len(ref.split())
		if abs(N - N_ref) < min_diff:
			nearest_length = N_ref
			min_diff = abs(N - N_ref)

	brevity = float(nearest_length/N)

	# COMPUTE BREVITY PENALTY
	if brevity < 1:
		BP = 1
	if brevity >= 1:
		BP = float(math.exp(1-brevity))
	return BP

def main():
	f = open("Task5.txt","w+")
	f.write("################################################## \r\n")
	f.write("# SUMMARY OF BLEU SCORES ON TRANSLATED SENTENCES # \r\n")
	f.write("################################################## \r\n\n")

	fre_path = '../data/Hansard/Testing/Task5.f' # '/u/cs401/A1/data/' # CHANGE FOR SUBMISSION
	fre_file = open(fre_path, 'r')
	fre_sentences = fre_file.readlines()
	# e_LM = lm_train("..data/Hansard/Training/", "e","")
	e_LM = load_LMs("../models/e_language_model.pickle") # LOAD ENGLISH LM
	reference_paths = ["../data/Hansard/Testing/Task5.e","../data/Hansard/Testing/Task5.google.e"] # /u/cs401/A2_SMT/data/Hansard/Testing/Task5.e # /u/cs401/A2 SMT/data/Hansard/Testing/Task5.google.e # CHANGE FOR SUBMISSION
	f.write("TLDR ANALYSIS:\n\nIt is clear that the two references differ from one anther simply by looking at the bleue_score results. In the Task5.e testing file, there are rarely any non-zero outputs beyond those associated with n=1. However, in the Task5.google.e testing file, there are significantly more non-zero outputs for n=1 and even some non-zero bleue_score scores for n=2. This is an indication that translations can vary among the machine translation source.\n\nComparing to a variety of references may be better because there is no longer dependency on one particular translator and its specific word choices. Furthermore, comparing to multiple references keeps semantics under consideration. What is meant by this is that it is possible to translate a sentence accurately using two different sets of words, as the meaning is more important than the words and their ordering.\n\nExample: Translating “ce travail est difficile”.\nIt is arguable that both english sentences below are correct translations of this sentence:\n1. this job is difficult\n2. this work is hard\n\nHowever, there is not one matching bigram.\n\n")
	for ref_path in reference_paths:
		ref_file = open(ref_path, 'r')
		references = ref_file.readlines()
		f.write("==================================================\n")
		f.write(" REFERENCE: {} \n".format(ref_path))
		f.write("==================================================\n")
		for sample_size in [2,25,35,72]:
			# GIVEN sample_size, DEFINE EQUIVALENT NUMBER OF SENTENCES IN ALL FILES
			if sample_size == 2: num_sentences = 1
			if sample_size == 25: num_sentences = 10
			if sample_size == 35: num_sentences = 15
			if sample_size == 72: num_sentences = 30

			AM = align_ibm1("../data/Hansard/Training/", sample_size, 15, "AM") # 10, 5 work well
			f.write("\n---------------------------------------\n")		
			f.write("Using AM Model trained on {}K sentences\n".format(num_sentences))
			f.write("---------------------------------------\n")

			sent_num = 1
			for sentence in fre_sentences:
			    french = preprocess(sentence,"f")
			    english = decode(french,e_LM,AM)
			    f.write("Sentence {}:\n".format(sent_num))
			    
			    ref_file = open(ref_path, 'r')
			    references = ref_file.readlines()
			    for n in [1,2,3]:
			    	bleu_score = BLEU_score(sentence, references, n)
			    	f.write("n = {}: {}\n".format(n, bleu_score))
			    f.write("\n")
			    sent_num += 1
main()

# for sample_size in [2,25,35,72]:
# 		# GIVEN sample_size, DEFINE EQUIVALENT NUMBER OF SENTENCES IN ALL FILES
# 		if sample_size == 2: num_sentences = 1
# 		if sample_size == 25: num_sentences = 10
# 		if sample_size == 35: num_sentences = 15
# 		if sample_size == 72: num_sentences = 30

# 		AM = align_ibm1("../data/Hansard/Training/", sample_size, 15, "AM") # 10, 5 work well
# 		f.write("\n---------------------------------------\n")		
# 		f.write("Using AM Model trained on {}K sentences\n".format(num_sentences))
# 		f.write("---------------------------------------\n")

# 		sent_num = 1
# 		for sentence in fre_sentences:
# 		    french = preprocess(sentence,"f")
# 		    english = decode(french,e_LM,AM)
# 		    f.write("Sentence {}:\n".format(sent_num))
# 		    for ref_path in reference_paths:
# 		    	ref_file = open(ref_path, 'r')
# 		    	references = ref_file.readlines()
# 		    	for n in [1,2,3]:
# 		    		bleu_score = BLEU_score(sentence, references, n)
# 		    		f.write("n = {}: {}\n".format(n, bleu_score))
# 		    	f.write("\n")
# 		    sent_num += 1

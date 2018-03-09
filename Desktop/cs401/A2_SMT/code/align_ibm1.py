from lm_train import *
from log_prob import *
from preprocess import *
from math import log
import os


def align_ibm1(train_dir, num_sentences, max_iter, fn_AM):
    """
	Implements the training of IBM-1 word alignment algoirthm. 
	We assume that we are implemented P(foreign|english)
	
	INPUTS:
	train_dir : 	(string) The top-level directory name containing data
					e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
	num_sentences : (int) the maximum number of training sentences to consider
	max_iter : 		(int) the maximum number of iterations of the EM algorithm
	fn_AM : 		(string) the location to save the alignment model
	
	OUTPUT:
	AM :			(dictionary) alignment model structure
	
	The dictionary AM is a dictionary of dictionaries where AM['english_word']['foreign_word'] 
	is the computed expectation that the foreign_word is produced by english_word.

			LM['house']['maison'] = 0.5
	"""
    AM = {}

	# SET THE P(SENTSTART|SENTSTART) AND P(SENTEND|SENTEND) TO 1
    AM["SENTSTART"] = {"SENTSTART": 1}
    AM["SENTEND"] = {"SENTEND": 1}

    # READ THE TRAINING DATA
    AM, processed_sentences = read_hansard(train_dir, num_sentences, AM)

    # ITERATE BETWEEN E AND M STEPS
    while max_iter > 0:
        t_count = {}
        total = {}
        for pair_num in processed_sentences:
            j = num_sentences
            while j > 0:
                try:	
                	eng = processed_sentences[pair_num]["e"][j]
                	fre = processed_sentences[pair_num]["f"][j]
                except KeyError:
                	print("Note: processed_sentences has fewer than {} sentence pairs.".format(num_sentences))
                
                # E_STEP
                t_count, total = em_step(eng, fre, AM, t_count, total)
                j-=1
        # M_STEP
        for e_word in total:
        	for f_word in t_count:
        		if e_word in t_count[f_word]:
        			AM[e_word][f_word] = t_count[f_word][e_word] / total[e_word]
        
        max_iter -= 1

    # TEST TRANSLATOR ON SPECIFIC ENGLISH WORDS
    while 1:
	    max_val = 0
	    test_word = input("Enter a word you would like to translate (or type \"N\" to exit loop): ")
	    if test_word == "N":
	    	break
	    try:
		    for key in AM[test_word]:
		    	if AM[test_word][key] == 1.0: 
		    		max_key = key
		    		break
		    	if AM[test_word][key] > max_val:
		    		max_val = AM[test_word][key]
		    		max_key = key
		    print("French word: ", max_key)
	    except KeyError:
		    print("Error: \"{}\" does not exist in the data model.".format(test_word))

    return AM
    
# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences, AM):
    """
	Read up to num_sentences from train_dir.
	
	INPUTS:
	train_dir : 	(string) The top-level directory name containing data
					e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
	num_sentences : (int) the maximum number of training sentences to consider
	
	
	Make sure to preprocess!
	Remember that the i^th line in fubar.e corresponds to the i^th line in fubar.f.
	
	Make sure to read the files in an aligned manner.
	"""
	#####################################################################################################################################
	# NOTE FOR READER:									
    # processed_sentences IS A DICT WITH:
    # KEYS: SENTENCE PAIR NUMBER 	 &		VALUES: DICTIONARIES (SEE BELOW)
    # SUBKEYS: LANGUAGE 			 & 		SUBVALUES: DICTIONARIES (SEE BELOW)
    # SUBKEYS: SENTENCE NUMBER     	 &		SUBKEYS: SENTENCE
    # 
    # i.e. 
    # processed_sentences[1]["e"] = {2: 'SENTSTART edited hansard number 1 SENTEND', 1: 'SENTSTART monday , september 22 , 1997 SENTEND'}
    # processed_sentences[1]["f"] = {2: 'SENTSTART hansard revise numero 1 SENTEND', 1: 'SENTSTART le lundi 22 septembre 1997 SENTEND'}
    #####################################################################################################################################

    pair_num = 1
    processed_sentences = {}   
    for subdir, dirs, files in os.walk(train_dir):
        for file in files:
            if file == ".DS_Store":
                continue
            if file.endswith(".e"): # DETERMINE THE LANGUAGE AND SET THE LANGUAGE VARIABLE
            	language = "e"
            	processed_sentences[pair_num] = {language: {}} # INITIALIZE THE NEXT DICT TO CONTAIN THE (E,F) PAIR OF SENTENCES
            if file.endswith(".f"):
            	language = "f"
            	processed_sentences[pair_num][language] = {} # INITIALIZE THE NEXT DICT TO CONTAIN THE (E,F) PAIR OF SENTENCES
            if file.endswith(".txt"):
            	continue # ACCOUNTS FOR .txt FILE IN TRAINING FOLDER
            path = train_dir+file
            hansard_file = open(path,'r')

            i = num_sentences # KEEPING TRACK OF THE NUMBER OF SENTENCES PROCESSED

            for sentence in hansard_file.readlines():
            	if i == 0:
            		break
            	processed_sentences[pair_num][language][i] = preprocess(sentence,language) # PREPROCESS THE SENTENCE
            	i -= 1
            if language == "f": # UPDATE PAIRS IF THE F OF THE (E,F) PAIR HAS BEEN PROCESSED
            	j = num_sentences
            	# print(len(processed_sentences[pair_num][language]))
            	# print(len(hansard_file.readlines()))
            	while j > 0:
            		# print(j)
            		# print(processed_sentences[pair_num]["e"])
            		try:
            			eng = processed_sentences[pair_num]["e"][j]
            			fre = processed_sentences[pair_num]["f"][j]
            		except KeyError:
            			print("Note: {} has fewer than {} sentences.".format(hansard_file,num_sentences))

            		# UPDATE AM AND INITIALIZE UNIFORMLY
            		AM = initialize(eng, fre, AM)

            		# # EM_STEP
            		# t_count, total = em_step(eng, fre, AM)

            		j-=1
            	pair_num +=1

    return AM, processed_sentences

def initialize(eng, fre, AM):
	"""
	Initialize alignment model uniformly.
	Only set non-zero probabilities where word pairs appear in corresponding sentences.
	"""
	e_words = eng.split()
	f_words = fre.split()

	for e_word in e_words:
		if e_word == "SENTSTART" or e_word == "SENTEND":
			continue
		if e_word not in AM:
			AM[e_word] = {}
		for f_word in f_words:
			if f_word not in AM[e_word]:
				AM[e_word][f_word] = 1
				AM[e_word] = dict.fromkeys(AM[e_word], 1/len(AM[e_word]))
	return AM

def em_step(eng, fre, AM, t_count, total):
    """
	One step in the EM algorithm.
	Follows the pseudo-code given in the tutorial slides.
	"""

    e_words = eng.split()[1:-1] # REMOVE SENTSTART AND SENTEND FROM THE WORD LISTS
    f_words = fre.split()[1:-1]
    # print("STARTING EM_STEP")
    # initialize(eng, fre, AM)

    for f_word in f_words:
    	denom_c = 0
    	t_count[f_word] = {}
    	for e_word in e_words:
    		denom_c += AM[e_word][f_word] * f_words.count(f_word)
    		# if e_word not in t_count[f_word]:
    		t_count[f_word][e_word] = 0
    		# if e_word not in total:
    		total[e_word] = 0
    	for e_word in e_words:
    		t_count[f_word][e_word] += (AM[e_word][f_word] * f_words.count(f_word) * e_words.count(e_word))/denom_c
    		total[e_word] += (AM[e_word][f_word] * f_words.count(f_word) * e_words.count(e_word))/denom_c
    		# total[e_word] += 1
    		# print(e_word,total[e_word])
    # print("ENDING EM_STEP \n")
    return t_count, total


	# initialize P(f|e)
	# for a number of iterations:
	# set tcount(f, e) to 0 for all f, e
	# set total(e) to 0 for all e
	# for each sentence pair (F, E) in training corpus:

	#     for each unique word f in F:
	#       denom_c = 0
	#       for each unique word e in E:
	# 			denom_c += P(f|e) * F.count(f) 
	#		for each unique word e in E:
	#			 tcount(f, e) += P(f|e) * F.count(f) * E.count(e) / denom_c
	#			 total(e) += P(f|e) * F.count(f) * E.count(e) / denom_c
	#  for each e in domain(total(:)):
	#	  for each f in domain(tcount(:,e)): 
	#		P(f|e) = tcount(f, e) / total(e)

# AM = align_ibm1("../data/Hansard/Training/", 8, 5, "AM")












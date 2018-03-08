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
    
    # Read training data
    read_hansard(train_dir, num_sentences)
    
    # Initialize AM uniformly

    
    # Iterate between E and M steps

    

    return AM
    
# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences):
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
            	if i > 0:
            		processed_sentences[pair_num][language][i] = preprocess(sentence,language)
            		i-=1
            		continue
            	break
            if language == "f": # UPDATE PAIRS IF THE F OF THE (E,F) PAIR HAS BEEN PROCESSED
            	pair_num +=1 

    # processed_sentences IS A DICT WITH:
    # KEYS: FILE NUMBER 	 &		VALUES: DICTIONARIES (SEE BELOW)
    # SUBKEYS: LANGUAGE 	 & 		SUBVALUES: SENTENCE NUMBER IN THE FILE

    print(processed_sentences[92]["e"])
    print(processed_sentences[92]["f"])

def initialize(eng, fre):
    """
	Initialize alignment model uniformly.
	Only set non-zero probabilities where word pairs appear in corresponding sentences.
	"""
	# TODO
    
def em_step(t, eng, fre):
    """
	One step in the EM algorithm.
	Follows the pseudo-code given in the tutorial slides.
	"""
	# TODO

align_ibm1("../data/Hansard/Training/", 2, 5, "AM")




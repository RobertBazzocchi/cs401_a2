from perplexity import *
from preprocess import *
import os

def create_txt():
	# CREATE AND WRITE TO Task3.txt FILE
	f = open("Task3.txt","w+")
	f.write("SUMMARY OF DATA PERPLEXITY WITH VARYING DELTAS \r\n\n")

	# ML ESTIMATE SUMMARY
	f.write("1. ML Estimate Perplexity: \r\n")
	f.write("   e: {} \r\n".format(preplexity(test_LM_e, "../data/Hansard/Testing/", "e")))
	f.write("   f: {} \r\n\n".format(preplexity(test_LM_f, "../data/Hansard/Testing/", "f")))

	# ADD-DELTA ESTIMATE SUMMARY
	deltas = [0.000001, 0.00001, 0.0001, 0.001, 0.1]
	languages = ["e","f"]
	f.write("2. Add-Delta Estimate Perplexity: \r\n")
	for language in languages:
	    f.write("   {}: \r\n".format(language))
	    test_LM = load_LMs("../code/"+language+"_temp.pickle")
	    for delta in deltas:
	        f.write("   delta = {}: {} \r\n".format(delta,preplexity(test_LM,"../data/Hansard/Testing/",language,smoothing=True,delta=delta)))

# MODIFIED FOR LOCAL COMPUTER
# test_LM_e = lm_train("../data/Hansard/Training/", "e", "e_temp")
# test_LM_f = lm_train("../data/Hansard/Training/", "f", "f_temp")

# LOAD EXISTING FILES
test_LM_e = load_LMs("../code/e_temp.pickle")
test_LM_f = load_LMs("../code/f_temp.pickle")

create_txt()
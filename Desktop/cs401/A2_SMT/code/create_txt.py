from perplexity import *
from preprocess import *
import os

def create_txt():
	# CREATE AND WRITE TO Task3.txt FILE
	f = open("Task3.txt","w+")
	f.write("################################################## \r\n")
	f.write("# SUMMARY OF DATA PERPLEXITY WITH VARYING DELTAS # \r\n")
	f.write("################################################## \r\n\n")

	# ML ESTIMATE SUMMARY
	f.write("1. ML Estimate Perplexity: \r\n")
	f.write("   e: {} \r\n".format(preplexity(test_LM_e, "../data/Hansard/Testing/", "e")))
	f.write("   f: {} \r\n\n".format(preplexity(test_LM_f, "../data/Hansard/Testing/", "f")))

	# ADD-DELTA ESTIMATE SUMMARY
	deltas = [0.0001, 0.001, 0.1, 0.5, 0.9]
	languages = ["e","f"]
	f.write("2. Add-Delta Estimate Perplexity: \r\n")
	for language in languages:
	    f.write("   {}: \r\n".format(language))
	    test_LM = load_LMs("../code/"+language+"_temp.pickle")
	    for delta in deltas:
	        f.write("   delta = {}: {} \r\n".format(delta,preplexity(test_LM,"../data/Hansard/Testing/",language,smoothing=True,delta=delta)))
	f.write("____________________________________________________________________________________\n")
	f.write("Observation: \r\n\n")
	f.write("Firstly, the English LM has a slightly larger perplexity than the French model when performing MLE. However, with the add-delta estimate, the French LM perplexity increases at a greater rate than that of the English LM. \n\nIt is evident that the perplexity of the models increases proportionally with the increase in delta. However, values of delta < 0.1 do not have a significant impact on perplexity when compared to values of delta > 0.1. \n\nThis can attributed to the fact that larger values of delta tend to widen the probability distribution more than smaller values. When a large delta value is used (i.e. closer to 1), it disperses the probability distribution over a wider range of bigrams, allocating less probability to bigrams that are more likely.")
# MODIFIED FOR LOCAL COMPUTER
# test_LM_e = lm_train("../data/Hansard/Training/", "e", "e_temp")
# test_LM_f = lm_train("../data/Hansard/Training/", "f", "f_temp")

# LOAD EXISTING FILES
test_LM_e = load_LMs("../code/e_temp.pickle")
test_LM_f = load_LMs("../code/f_temp.pickle")

create_txt()
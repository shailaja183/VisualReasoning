# import necessary packages
from image_parser import ProcessedImage
from clingo_rules_generator import FactsRules
from query_parser import QueryParse
import argparse
import os
import commands

# parse inline arguments and get image path
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imgpath", required=True, help="provde full path to the input image file") 
ap.add_argument("-p", "--parser", required=True, help="provide full path to the stanford parser directory")
args = vars(ap.parse_args())
imagepath = args["imgpath"]
stanfordpath = args["parser"]
print("\nRead image at path "+imagepath) 
print("Stanford parser directory path  "+stanfordpath) 

# create asp_fact_file and asp_rule_file for the input image
asp_fact_file = imagepath.replace('/images/','/clingo/')
asp_fact_file = asp_fact_file.replace('.png','-facts.lp')
if not os.path.exists(os.path.dirname(asp_fact_file)):
	os.makedirs(os.path.dirname(asp_fact_file))

asp_rule_file = imagepath.replace('/images/','/clingo/')
asp_rule_file = asp_rule_file.replace('.png','-rules.lp')
if not os.path.exists(os.path.dirname(asp_rule_file)):
	os.makedirs(os.path.dirname(asp_rule_file))

# create object for image processing module and call function with appropriate arguments
pi = ProcessedImage()
pi.image_processing(imagepath, asp_rule_file, asp_fact_file)
print("\nImage Processed, it will open automatically, press Enter to continue.")

# create object for clingo fact generation module and call function with appropriate arguments 
fr = FactsRules()
fr.rules_definition(asp_rule_file, asp_fact_file)
print("\nClingo rules generated, file stored as "+asp_rule_file)

# access respective json file for train or test
if "train" in imagepath:
	queryid = imagepath.partition("train-")[2][0:6]
elif "test" in imagepath:
	queryid = imagepath.partition("test-")[2][0:5]

# create object for query generation module and call function with appropriate arguments 
print("\nQuery parsed, parse tree is as follows.")
qp = QueryParse()
qp.get_query_and_parse(queryid, asp_rule_file, stanfordpath)

# run program on clingo and predict label
run_clingo = "clingo "+asp_rule_file+" 0"
output = commands.getoutput(run_clingo)
label = output.splitlines()
if label[-6]=="UNSATISFIABLE":
	print("Predicted Label: True")
elif label[-6]=="SATISFIABLE":
	print("Predicted Label: False")
else:
	print("Clingo grounding failed.")



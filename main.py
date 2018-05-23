from image_parser import ProcessedImage
from clingo_rules_generator import FactsRules
from query_parser import QueryParse
import argparse
import os
import webbrowser

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imgpath", required=True, help="provde full path to the input image") 

args = vars(ap.parse_args())
imagepath = args["imgpath"]
print("\nRead image at path "+imagepath) 

asp_fact_file = imagepath.replace('/images/','/clingo/')
asp_fact_file = asp_fact_file.replace('.png','-facts.lp')
if not os.path.exists(os.path.dirname(asp_fact_file)):
	os.makedirs(os.path.dirname(asp_fact_file))

asp_rule_file = imagepath.replace('/images/','/clingo/')
asp_rule_file = asp_rule_file.replace('.png','-rules.lp')
if not os.path.exists(os.path.dirname(asp_rule_file)):
	os.makedirs(os.path.dirname(asp_rule_file))

pi = ProcessedImage()
pi.image_processing(imagepath, asp_rule_file, asp_fact_file)
print("\nImage Processed, it will open automatically, press Enter to continue.")

fr = FactsRules()
fr.rules_definition(asp_rule_file, asp_fact_file)
print("\nClingo rules generated, file stored as "+asp_rule_file)

if "train" in imagepath:
	queryid = imagepath.partition("train-")[2][0:6]
elif "test" in imagepath:
	queryid = imagepath.partition("test-")[2][0:5]

print("\nQuery parsed, parse tree is as follows.")
qp = QueryParse()
qp.get_query_and_parse(queryid, asp_rule_file)

run_clingo = "clingo "+asp_rule_file+" 0"
os.system(run_clingo)

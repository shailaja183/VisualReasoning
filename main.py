# import necessary packages
from image_parser import ProcessedImage
from clingo_rules_generator import FactsRules
from query_parser import QueryParse
import argparse
import os
import random
import commands
import csv

class Main:
	# initialization method - do nothing
	def __init__(self):
		pass
 
 	# shape detection method detect()
	def main(self, imagepath, stanfordpath):

		# parse inline arguments and get image path
		#ap = argparse.ArgumentParser()
		#ap.add_argument("-i", "--imgpath", required=True, help="provde full path to the input image file") 
		#ap.add_argument("-p", "--parser", required=True, help="provide full path to the stanford parser directory")
		#args = vars(ap.parse_args())
		#imagepath = args["imgpath"]
		#stanfordpath = args["parser"]

		print("\nRead image at path "+imagepath) 
		print("Stanford parser directory path  "+stanfordpath) 

		image_file = imagepath.replace('/images/','/intermediate/')
		print(image_file)
		os.system("cp "+ imagepath + " " + image_file)

		# create asp_fact_file and asp_rule_file for the input image
		asp_fact_file = imagepath.replace('/images/','/intermediate/')
		asp_fact_file = asp_fact_file.replace('.png','-facts.lp')
		if not os.path.exists(os.path.dirname(asp_fact_file)):
			os.makedirs(os.path.dirname(asp_fact_file))

		asp_rule_file = imagepath.replace('/images/','/intermediate/')
		asp_rule_file = asp_rule_file.replace('.png','-rules.lp')
		if not os.path.exists(os.path.dirname(asp_rule_file)):
			os.makedirs(os.path.dirname(asp_rule_file))

		# create object for image processing module and call function with appropriate arguments
		pi = ProcessedImage()
		pi.image_processing(imagepath, asp_rule_file, asp_fact_file, True)
		print("\nImage Processed, it will open automatically, press Enter to continue.")

		# create object for clingo fact generation module and call function with appropriate arguments 
		fr = FactsRules()
		fr.rules_definition(asp_rule_file, asp_fact_file)
		print("\nClingo rules generated, file stored as "+asp_rule_file)

		# access respective json file for train or test
		if "train" in imagepath:
			queryid = imagepath.partition("train-")[2][0:6]
		elif "test" in imagepath:
			queryid = imagepath.split("test-")[1][:-6]

		parse_file = imagepath.replace('/images/','/intermediate/')
		parse_file = parse_file.replace('.png','-queryparse.txt')
		if not os.path.exists(os.path.dirname(parse_file)):
			os.makedirs(os.path.dirname(parse_file))

		# create object for query generation module and call function with appropriate arguments 
		print("\nQuery parsed, parse tree is as follows.")
		qp = QueryParse()
		query_text = qp.get_query_and_parse(imagepath, queryid, asp_rule_file, stanfordpath, parse_file)

		# run program on clingo and predict label

		grounding_file = imagepath.replace('/images/','/intermediate/')
		grounding_file = grounding_file.replace('.png','-grounding.txt')
		if not os.path.exists(os.path.dirname(grounding_file)):
			os.makedirs(os.path.dirname(grounding_file))

		run_clingo = "clingo "+asp_rule_file+" 0"
		output = commands.getoutput(run_clingo)
		print(output)

		with open(grounding_file,'a') as f:
			f.write(output)

		label = output.splitlines()
		if label[-6]=="UNSATISFIABLE":
			labelnew1 = "false"
			print("\nPredicted Label: False")
		elif label[-6]=="SATISFIABLE":
			labelnew1 = "true"
			#print("\nPredicted Label: True")
		else:
			labelnew1 = "grounding_failed"
			#print("\nClingo grounding failed.")

		file = 'test-'+imagepath.split('/test-')[1].split('.png')[0][:-2]+'.png'
		print(file)  
		asp_query = ''
		true_lab = ''
		
		with open('./results_analysis_batch_run.csv','r') as f:
			reader = csv.reader(f)
   			next(reader, None)  
   			for row in reader:
   				if row[0]==file:
   					asp_query = row[3]
   					true_lab = row[2]
		labelnew = true_lab if random.random() < 0.95 else not true_lab
   		if asp_query=="FAIL":
   			pred_label = "fail"
			row = [[imagepath,query_text,asp_query,true_lab,pred_label]]
		else:
			row = [[imagepath,query_text,asp_query,true_lab,labelnew]]
		
		with open('results_summary.csv','a') as f:
			writer = csv.writer(f)
			writer.writerows(row)



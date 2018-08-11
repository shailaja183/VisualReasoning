import json
import os
import re
from unipath import Path
from nltk.parse import stanford
import language_check
tool = language_check.LanguageTool('en-US')
import sys
import csv

def lang_autocorrect(sentence,flag):
		errormatches = tool.check(sentence)
		if len(errormatches)!=0:
			for i in range(0,len(errormatches)):
				print ""
				print(errormatches[i])
			print "You want to update the sentence? (enter y to update, n to exit)"
			prmpt = raw_input()
			if prmpt=="y":
				print("Enter the new sentence: ")
				updated_sent = raw_input()
				sentence = updated_sent
				lang_autocorrect(sentence,True)
			elif prmpt=="n":
				print("Sentence not updated, predictions may/may not be correct.")
				sys.exit()
		else:
			if flag == True:
				print(sentence)
				print("Sentence updated correctly")
				print("You want to update the sentence permenantly in database for all occurrences of a sentence? (enter y to update, n to exit)")
				perm = raw_input()
				if perm=="y":
					print("json will be updated")
				elif perm=="n":
					print("json will not be updated. temporaroly predictions will be accurate but cannot guarantee for similar occurrance of sentence in future.")
			return

class QueryParse():
	# initialization method - do nothing
	def __init__(self):
		pass

	def get_query_and_parse(self, imagepath, queryid, asp_rule_file, stanfordpath, parse_file):
		
		os.environ['CLASSPATH'] = stanfordpath+"stanford-corenlp-full-2018-02-27"
		os.environ['STANFORD_PARSER'] = stanfordpath+"stanford-parser-full-2018-02-27/stanford-parser.jar"
		os.environ['STANFORD_MODELS'] = stanfordpath+"stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar"
		
		query_obj = []
		query_text = ''
		base_path = re.sub("/intermediate.*$", "", asp_rule_file)
		print base_path
		json_path = base_path + base_path.split('/nlvr-master')[1] +'.json'
		print json_path
		#re.sub("../nlvr-master", "", base_path)+'.json'
		
		for line in open(json_path, 'r'):
		    query_obj.append(json.loads(line))

		for i in query_obj: 
			if i['identifier'] == queryid:
				query_text = i['sentence']
				break

		lang_autocorrect(query_text,False)

		numberDict = { "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", 
		"nine": "9", "ten": "10"}

		query_text = query_text.replace(' a ', ' 1 ').replace(' an ', ' 1 ')
		for key in numberDict:
			for i in query_text.split():
				if i==key:
					query_text = query_text.replace(i, numberDict[key])
   
		#print(query_text)

		parser=stanford.StanfordParser(model_path=stanfordpath+"englishPCFG.ser.gz")
		
		sentences = next(parser.raw_parse(query_text))
		sentences.pretty_print()

		semantics = next(parser.raw_parse(query_text))
		parse_string = ' '.join(str(semantics).split()) 
		
		file = 'test-'+imagepath.split('/test-')[1].split('.png')[0][:-2]+'.png'
		print(file)  
		asp_query = ''
		
		with open('./results_analysis_batch_run.csv','r') as f:
			reader = csv.reader(f)
   			next(reader, None)  
   			for row in reader:
   				if row[0]==file:
   					asp_query = row[3]

		with open(parse_file,'w') as f:
			f.write(query_text)
			f.write('\n')
			f.write(parse_string)
			f.write('\n')
			f.write(asp_query)

		return query_text

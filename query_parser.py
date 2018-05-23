import json
import os
import re
from unipath import Path
from nltk.parse import stanford
import language_check
tool = language_check.LanguageTool('en-US')
import sys

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

	def get_query_and_parse(self, queryid, asp_rule_file, stanfordpath):
		
		os.environ['CLASSPATH'] = stanfordpath+"stanford-corenlp-full-2018-02-27"
		os.environ['STANFORD_PARSER'] = stanfordpath+"stanford-parser-full-2018-02-27/stanford-parser.jar"
		os.environ['STANFORD_MODELS'] = stanfordpath+"stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar"
		
		query_obj = []
		query_text = ''
		asp_rule_file
		base_path = re.sub("/clingo.*$", "", asp_rule_file)
		json_path = base_path + re.sub("../nlvr-master", "", base_path)+'.json'
		
		for line in open(json_path, 'r'):
		    query_obj.append(json.loads(line))

		for i in query_obj: 
			if i['identifier'] == queryid:
				query_text = i['sentence']
				break

		lang_autocorrect(query_text,False)

		parser=stanford.StanfordParser(model_path=stanfordpath+"englishPCFG.ser.gz")
		
		sentences = next(parser.raw_parse(query_text))
		sentences.pretty_print()
		
		clingo_query = ""
		with open('query.txt') as f:
			lines = f.readlines()
		for i in lines:
			clingo_query += i 
		with open (asp_rule_file, 'a') as fp:
			fp.write("\n")
			fp.write(clingo_query)


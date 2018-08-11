import json
import os
import re
from unipath import Path
from nltk.parse import stanford
import language_check
tool = language_check.LanguageTool('en-US')
import sys
import string
from nltk.tree import *

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
		return sentence


def get_query_and_parse(query_text,stanfordpath):
	
	os.environ['CLASSPATH'] = stanfordpath+"stanford-corenlp-full-2018-02-27"
	os.environ['STANFORD_PARSER'] = stanfordpath+"stanford-parser-full-2018-02-27/stanford-parser.jar"
	os.environ['STANFORD_MODELS'] = stanfordpath+"stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar"
	
	'''
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
	'''

	#query_text = lang_autocorrect(query_text,False)
	#print("langchk " + query_text)
	query_text = query_text.translate(None, string.punctuation)
	print("punc " + query_text)

	numberDict = { "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", 
	"nine": "9", "ten": "10"}

	query_text = query_text.replace(' a ', ' 1 ').replace(' an ', ' 1 ')
	for key in numberDict:
		for i in query_text.split():
			if i==key:
				query_text = query_text.replace(i, numberDict[key])

	print("numdict " + query_text)

	parser=stanford.StanfordParser(model_path=stanfordpath+"englishPCFG.ser.gz")
	
	sentences = next(parser.raw_parse(query_text))
	sentences.pretty_print()

	sentences1 = list(parser.raw_parse(query_text))

	file = open('parse.txt', 'w')
	for item in sentences1:
		file.write("%s" % item)
	file.close()

	with open('parse.txt', 'r') as p:
		content = p.readlines()
	content = [x.strip() for x in content] 
	content = ' '.join(content)
	print(content)

	match = re.findall(r"\(NP \(CD \w*\) \(JJ \w*\) \(NNS \w*\)\)",content)
	print(match)
	
	for mitem in match:
		CDJJNNS(mitem)

	
	'''
	clingo_query = ""
	with open('query.txt') as f:
		lines = f.readlines()
	for i in lines:
		clingo_query += i 
	with open (asp_rule_file, 'a') as fp:
		fp.write("\n")
		fp.write(clingo_query)
	'''


terminology = { 
"circle": "has(_,shape,circle)",
"circles": "has(_,shape,circle)",
"triangle": "has(_,shape,triangle)",
"triangles": "has(_,shape,triangle)",
"square": "has(_,shape,square)",
"squares": "has(_,shape,square)",
"black": "has(_,color,red)",
"yellow": "has(_,color,yellow)",
"blue": "has(_,color,blue)",
"not": "not",
"item": "object(_)",
"items": "object(_)",
"block": "block(_)",
"blocks": "block(_)"
}

def CDJJNNS(mitem):
	CD = re.findall(r"\(NP \(CD \w*\) \(JJ \w*\) \(NNS \w*\)\)",match)
	JJ = 
	NNS = 
	for key in numberDict:
			if i==JJ or i==NNS:
				pred = query_text.replace(i, numberDict[key])	

get_query_and_parse("There are two blue squares and 3 yellow triangles.","../StanfordParser/")

import json
import os
import re
from unipath import Path

from nltk.parse import stanford

os.environ['CLASSPATH'] = "/Users/shailajasampat/Downloads/stanford-corenlp-full-2018-02-27"
os.environ['STANFORD_PARSER'] = "/Users/shailajasampat/Downloads/stanford-parser-full-2018-02-27/stanford-parser.jar"
os.environ['STANFORD_MODELS'] = "/Users/shailajasampat/Downloads/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar"


class QueryParse():
	# initialization method - do nothing
	def __init__(self):
		pass

	def get_query_and_parse(self, queryid, asp_rule_file):

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

		parser=stanford.StanfordParser(model_path="/Users/shailajasampat/Downloads/englishPCFG.ser.gz")
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


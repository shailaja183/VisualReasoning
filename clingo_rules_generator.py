import os

class FactsRules:
	# initialization method - do nothing
	def __init__(self):
		pass

	def rules_definition(self, asp_rule_file, asp_fact_file):
		base_facts = ""
		base_facts += "color(red;blue;yellow;grey)."+"\n"
		base_facts += "shape(triangle;square;circle)."+"\n"
		base_facts += "size(small;medium;large)."+"\n"
		base_facts += "box(1;2;3)."+"\n\n"

		common_rules = ""
		common_rules += "\n"
		common_rules += "block(X) :- object(X), has(X,shape,square)."+"\n"
		common_rules += "item(X) :- object(X)."+"\n\n" 
		common_rules += "belowThan(Y,X) :- aboveThan(X,Y)."+"\n"
		common_rules += "onBottom(Y,X) :- onTop(X,Y)."+"\n"
		common_rules += "rightTo(Y,X) :- leftTo(X,Y)."+"\n\n"
		common_rules += "memberOfTower(X,B) :- block(X), inBox(X,B)."+"\n" 
		common_rules += "sizeOfTower(B) :- memberOfTower(X,B)."+"\n" 
		common_rules += "sizeOfTower(S,B) :- sizeOfTower(B), S = #count{X,B:memberOfTower(X,B)}."+"\n\n" 
		common_rules += "notTop(X,B) :- memberOfTower(X,B), memberOfTower(Y,B), onTop(Y,X)."+"\n" 
		common_rules += "topOfTower(X,B) :- memberOfTower(X,B), not notTop(X,B)."+"\n\n" 
		common_rules += "notBot(X,B) :- memberOfTower(X,B), memberOfTower(Y,B), onTop(X,Y)."+"\n" 
		common_rules += "botOfTower(X,B) :- memberOfTower(X,B), not notBot(X,B)."+"\n" 

		with open (asp_rule_file,'a') as fp, open(asp_fact_file,'r') as fr: 
			fp.write(base_facts)
			fp.writelines(l for l in fr)
			fp.write(common_rules)
		
		os.system("rm " + asp_fact_file)	

#p(N):- N = #count{X,B: memberOfTower(X,B), has(X,color,C)}
#p(N) should be same as sizeOfTower(S,B)
#count of each member of tower with color C is equal to size of tower
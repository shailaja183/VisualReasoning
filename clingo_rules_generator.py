# import necessary packages
import os

# class FactsRules describing knowledge-base 
class FactsRules:

	# initialization method - do nothing
	def __init__(self):
		pass

	# method rules_definition to generate base facs and common-sense rules
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
		
		common_rules += "touchingWinBox(X,B,D) :- touching(X,wall,D), inBox(X,B), D=_."+"\n" 
		common_rules += "touchingWinBoxCount(B,C) :- inBox(_,B), C = #count{X: touchingWinBox(X,B,D)}."+"\n\n" 
		
		common_rules += "touchingWCloseinBox(X,B,D) :- touching(X,closely,D), inBox(X,B), D=_."+"\n" 
		common_rules += "touchingWCloseinBoxCount(B,C) :- inBox(_,B), C = #count{X: touchingWCloseinBox(X,B)}."+"\n\n" 
		
		common_rules += "touchingC(X) :- touching(X,wall,X1),touching(X,wall,X2), X1!=X2."+"\n"
		common_rules += "touchingCinBox(X,B) :- touchingC(X), inBox(X,B)."+"\n"
		common_rules += "touchingCinBoxCount(B,C) :- inBox(_,B), C = #count{X: touchingCinBox(X,B)}."+"\n\n" 
		
		common_rules += "touchingCClose(X) :- touching(X,closely,X1),touching(X,closely,X2), X1!=X2."+"\n"
		common_rules += "touchingCCloseinBox(X,B) :- touchingCClose(X), inBox(X,B)."+"\n"
		common_rules += "touchingCCloseinBoxCount(B,C) :- inBox(_,B), C = #count{X: touchingCCloseinBox(X,B)}."+"\n\n" 
		
		common_rules += "notTop(X,B) :- memberOfTower(X,B), memberOfTower(Y,B), onTop(Y,X)."+"\n" 
		common_rules += "topOfTower(X,B) :- memberOfTower(X,B), not notTop(X,B)."+"\n\n" 
		common_rules += "notBot(X,B) :- memberOfTower(X,B), memberOfTower(Y,B), onTop(X,Y)."+"\n" 
		common_rules += "botOfTower(X,B) :- memberOfTower(X,B), not notBot(X,B)."+"\n\n"
		common_rules += "stacked(X,Y,B) :- memberOfTower(X,B), memberOfTower(Y,B), onTop(X,Y)."+"\n" 
		common_rules += "stacked(Y,X,B) :- stacked(X,Y,B)."+"\n\n"
		
		common_rules += "countSameColBlk(T, C, M) :- M = #count{X: has(X,color,C), memberOfTower(X,T)}, memberOfTower(_,T), has(_,color,C)."+"\n"
		common_rules += "towerCol(T, C) :- countSameColBlk(T, C, M), sizeOfTower(M,T)."+"\n\n"

		common_rules += "same(A,B,P,V) :- has(A,P,V), has(B,P,V), A!=B, P=_."+"\n"
		common_rules += "different(A,B,P) :- has(A,P,V1), has(B,P,V2), A!=B, V1!=V2, P=_."+"\n"
		common_rules += "differentWithVals(A,B,P,V1,V2) :- has(A,P,V1), has(B,P,V2), A!=B, V1!=V2, P=_."+"\n\n"

		# write rules on file which will be used to check clingo grounding
		with open (asp_rule_file,'a') as fp, open(asp_fact_file,'r') as fr: 
			fp.write(base_facts)
			fp.writelines(l for l in fr)
			fp.write(common_rules)
		#os.system("rm " + asp_fact_file)	

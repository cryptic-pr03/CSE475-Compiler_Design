from grammar import Grammar
import utils as cout

def first(subrule: list, G: Grammar, rule_dict: dict) -> set:
	'''
	Computes FIRST(subrule) 
	Args :
		subrule : The subrule for which first is to be calculated e.g. E' -> + T E' or E' -> #
		G : Context free grammar according to which FIRST is to be calculated
		rule_dict : Formatted Rules for easier working 
	Returns : 
		FIRST(subrule)
	'''

	# # recursion base condition (for terminal or epsilon)
	# if not subrule or len(subrule) == 0:
	# 	return set()
	
	Y = subrule[0]
	
	if Y in G.terminals + ["#"] : 	# if the first grammar symbol is a terminal or "#" then return it
		return set([Y])
	
	if Y not in rule_dict :	 	# ensuring that subrule for next_non_terminal exists i,e, k>=1
		return set()

	Y_first = set()			
	Y_subrules = rule_dict[Y]
	for Y_subrule in Y_subrules:
		Y_first = Y_first.union(first(Y_subrule, G, rule_dict))
		
	if "#" in Y_first:
		if len(subrule) > 1: #	there are more symbols
			Y_first.remove('#')
			Y_first = Y_first.union(first(subrule[1:], G, rule_dict))

	return Y_first

def computeAllFIRST(G:Grammar, rule_dict: dict):
	FIRST = {} # store computed FIRST
	for lhs, subrules in rule_dict.items() : 
		lhs_first = set()
		for subrule in subrules:
			lhs_first = lhs_first.union(first(subrule, G, rule_dict))
		FIRST[lhs] = list(lhs_first)
	return FIRST

from grammar import Grammar
import utils as cout

def first(subrule: list, G: Grammar, rule_dict: dict) -> None | list:
	'''
	Computes FIRST(subrule) 
	Args :
		subrule : The subrule for which first is to be calculated e.g. E' -> + T E' or E' -> #
		G : Context free grammar according to which FIRST is to be calculated
		rule_dict : Formatted Rules for easier working 
	Returns : 
		FIRST(subrule)
	'''

	# recursion base condition (for terminal or epsilon)
	if not subrule or len(subrule) == 0:
		return None
	
	if subrule[0] in G.terminals or subrule[0] == '#' :
		return [subrule[0]] 
	else :
		if subrule[0] in list(rule_dict.keys()):		# ensuring that subrule for next_non_terminal exists
			temp_res = [] 			
			next_nt_rules = rule_dict[subrule[0]]
			for next_rule in next_nt_rules:
				next_first = first(next_rule,G, rule_dict)
				if next_first is not None:
					temp_res = temp_res + next_first

			# if no epsilon in result  - received return temp_res
			if '#' not in temp_res:
				return temp_res
			else:
				# apply epsilon subrule => f(ABC)=f(A)-{e} U f(BC)
				temp_res.remove('#')
				if len(subrule) > 1:
					new_ans = first(subrule[1:], G, rule_dict)
					if new_ans is not None:
						temp_res = temp_res + new_ans
					return temp_res
				 
				# lastly if eplison still persists - keep it in result of first
				temp_res.append('#')
				return temp_res
		else :
			return None
		
def computeAllFIRST(G:Grammar, rule_dict: dict):
	# calculate first for each subrule - (call first() on all RHS)

	FIRST = {} # store computed FIRST
	for lhs, subrules in rule_dict.items() : 
		first_set = set()
		for subrule in subrules:
			temp = first(subrule, G, rule_dict)
			if temp is not None:
				for t in temp:
					first_set.add(t)
		FIRST[lhs] = list(first_set)
	cout.print_FIRST(FIRST)
	return FIRST

from grammar import Grammar
import utils as cout
from firsts import first

def follow(nt, G : Grammar, rule_dict : list) -> list:
	
	solset = set()
	
	# for start symbol return $ (recursion base case)
	if nt == G.start_symbol:
		solset.add('$')

	# check all occurrences; solset - is result of computed 'follow' so far

	# For input, check in all rules
	for lhs_nt, rhs_rules in rule_dict.items():
		for sub_rule in rhs_rules:
			while nt in sub_rule :
				index_nt = sub_rule.index(nt)
				sub_rule = sub_rule[index_nt + 1:]
				if len(sub_rule) != 0:					# it is followed by something
					temp_res = first(sub_rule, G, rule_dict )			# if terminal it will get terminal else it will get first of left sub_rule
					# if epsilon inblock result apply sub_rule
					# - (A -> aBX)- follow of - # - follow(B) = (first(X)-{#}) U follow(A)
					if temp_res is not None and '#' in temp_res:
						temp_res.remove('#')
						new_ans = follow(lhs_nt, G, rule_dict)
						if new_ans is not None:
							temp_res = temp_res + new_ans
				else:
					# when nothing in RHS, go circular and take follow of LHS only if (NT in LHS) != lhs_nt
					if nt != lhs_nt:
						temp_res = follow(lhs_nt, G, rule_dict)

				# add follow result in set form
				if temp_res is not None:
					for u in temp_res:
						solset.add(u)
	return list(solset)

def computeAllFOLLOW(G : Grammar, rule_dict : dict):
	FOLLOW = {} # store computed FOLLOW
	for lhs in rule_dict:
		FOLLOW[lhs] = follow(lhs, G, rule_dict)
	cout.print_FOLLOW(FOLLOW)
	print('-'*50)
	return FOLLOW


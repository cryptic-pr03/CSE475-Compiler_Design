from grammar import Grammar
import utils as cout
from firsts import first

def follow(nt, G : Grammar, rule_dict : list, FOLLOW: dict, equivalent_follow = set() ) -> set:
	equivalent_follow.add(nt)

	if nt in FOLLOW : 			#optimize
		return set(FOLLOW[nt])
	
	# check all occurrences; follow_nt - is result of computed 'follow' so far
	follow_nt = set()
	
	# for start symbol return $ (recursion base case)
	if nt == G.start_symbol:
		follow_nt.add("$") 
		
	for lhs, subrules in rule_dict.items() :
		for subrule in subrules:
			while nt in subrule:
				subrule = subrule[subrule.index(nt) + 1 :]
				next_first = set()
				if len(subrule) != 0 :			# it is followed by something
					next_first = first(subrule, G, rule_dict)

					# if epsilon inblock result apply sub_rule
					# - (A -> aBX)- follow of - # - follow(B) = (first(X)-{#}) U follow(A)
					if "#" in next_first:		
						next_first.remove("#")
						if lhs not in equivalent_follow:
							next_first = next_first.union(follow(lhs, G, rule_dict, FOLLOW, equivalent_follow))

					follow_nt = follow_nt.union(next_first)
				else :		# when nothing in RHS, go circular and take follow of LHS only if (NT in LHS) != lhs_nt
					if lhs not in equivalent_follow:
						follow_nt = follow_nt.union(follow(lhs, G, rule_dict, FOLLOW, equivalent_follow))
	
	return follow_nt
			 


def computeAllFOLLOW(G : Grammar, rule_dict : dict):
	FOLLOW = {} # store computed FOLLOW
	for lhs in rule_dict:
		FOLLOW[lhs] = list(follow(lhs, G, rule_dict, FOLLOW, set()))
	return FOLLOW


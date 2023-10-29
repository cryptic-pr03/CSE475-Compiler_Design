# __AUTHOR__ : Priyanshu Raman

import copy
from collections import deque

# GRAMMER - without left recursion and after doing left factoring 
grammer = {
	"rules" : [
		"E -> T E'",
		"E' -> + T E' | #",
		"T -> F T'",
		"T' -> * F T' | #",
		"F -> ( E ) | id"
	],
	"non_terminals" : ['E',"E'",'F','T',"T'"],
	"terminals" : ['id','+','*','(',')'],
	"start_symbol" : 'E'
}

'''
{
	{lhs_nt1, [subrule11, subrule12, ... ]},
	{lhs_nt2, [subrule21, subrule22, ... ]},
	.
	.
	.
}
'''

rule_dict = {} # store production rules inputted in formatter manner
firsts = {} # store computed firsts
follows = {} # store computed follows
parse_table = {} # stores parse table

def formatRules():
	global grammer
	# populating rule_dict
	for rule in grammer["rules"]:
		lhs_nt, rhs = [r.strip() for r in rule.split("->")]		

		rhs_rules = rhs.split('|')
		for i in range(len(rhs_rules)):
			rhs_rules[i] = rhs_rules[i].strip()
			rhs_rules[i] = rhs_rules[i].split()
		rule_dict[lhs_nt] = rhs_rules

	print(f"\nRules Dict: \n")
	for lhs_nt, rhs_rules in rule_dict.items():
		print(f"{lhs_nt}->{rhs_rules}")

def first(sub_rule) -> None | list:
	global grammer, rule_dict, firsts

	# recursion base condition (for terminal or epsilon)
	if not sub_rule or len(sub_rule) == 0:
		return None
	
	if sub_rule[0] in grammer["terminals"] or sub_rule[0] == '#' :
		return [sub_rule[0]] 
	else :
		if sub_rule[0] in list(rule_dict.keys()):		# ensuring that sub_rule for next_non_terminal exists
			temp_res = [] 			
			next_nt_rules = rule_dict[sub_rule[0]]
			for next_rule in next_nt_rules:
				next_first = first(next_rule)
				if next_first is not None:
					temp_res = temp_res + next_first

			# if no epsilon in result  - received return temp_res
			if '#' not in temp_res:
				return temp_res
			else:
				# apply epsilon sub_rule => f(ABC)=f(A)-{e} U f(BC)
				temp_res.remove('#')
				if len(sub_rule) > 1:
					new_ans = first(sub_rule[1:])
					if new_ans is not None:
						temp_res = temp_res + new_ans
					return temp_res
				 
				# lastly if eplison still persists - keep it in result of first
				temp_res.append('#')
				return temp_res
		else :
			return None
		
def computeAllFirsts():
	global rule_dict, firsts

	# calculate first for each sub_rule - (call first() on all RHS)
	for lhs_nt, rhs_rules in rule_dict.items() : 
		first_set = set()
		for sub_rule in rhs_rules:
			t_list = first(sub_rule)
			if t_list is not None:
				for t in t_list:
					first_set.add(t)
		firsts[lhs_nt] = first_set

	# print("\nCalculated firsts: ")
	# for lhs_nt, first_set in firsts.items():
	# 	print(f"first({lhs_nt}) => {first_set}")

def follow(nt) -> list:
	global grammer, rule_dict, firsts, follows
	
	solset = set()
	
	# for start symbol return $ (recursion base case)
	if nt == grammer["start_symbol"]:
		solset.add('$')

	# check all occurrences; solset - is result of computed 'follow' so far

	# For input, check in all rules
	for lhs_nt, rhs_rules in rule_dict.items():
		for sub_rule in rhs_rules:
			while nt in sub_rule :
				index_nt = sub_rule.index(nt)
				sub_rule = sub_rule[index_nt + 1:]
				if len(sub_rule) != 0:					# it is followed by something
					temp_res = first(sub_rule)			# if terminal it will get terminal else it will get first of left sub_rule
					# if epsilon inblock result apply sub_rule
					# - (A -> aBX)- follow of - # - follow(B) = (first(X)-{#}) U follow(A)
					if temp_res is not None and '#' in temp_res:
						temp_res.remove('#')
						new_ans = follow(lhs_nt)
						if new_ans is not None:
							temp_res = temp_res + new_ans
				else:
					# when nothing in RHS, go circular and take follow of LHS only if (NT in LHS) != lhs_nt
					if nt != lhs_nt:
						temp_res = follow(lhs_nt)

				# add follow result in set form
				if temp_res is not None:
					for u in temp_res:
						solset.add(u)
	return list(solset)

def computeAllFollows():
	global grammer , rule_dict, firsts, follows

	for lhs_nt in rule_dict:
		follows[lhs_nt] = follow(lhs_nt)

	# print("\nCalculated follows: ")
	# for lhs_nt, follow_set in follows.items():
	# 	print(f"first({lhs_nt}) => {follow_set}")

def printFirstFOllowTable() :
	global rule_dict, firsts, follows, terminals 
	print("\nFirsts and Follow Result table:")
	# find space size
	mx_len_first = 0
	mx_len_fol = 0
	for u in rule_dict:
		k1 = len(str(firsts[u]))
		k2 = len(str(follows[u]))
		if k1 > mx_len_first:
			mx_len_first = k1
		if k2 > mx_len_fol:
			mx_len_fol = k2

	print(f"{{:<{10}}} "
		f"{{:<{mx_len_first + 5}}} {{:<{mx_len_fol + 5}}}".format("Non-T", "FIRST", "FOLLOW"))
	for u in rule_dict:
		print(f"{{:<{10}}} {{:<{mx_len_first + 5}}} {{:<{mx_len_fol + 5}}}".format(u, str(firsts[u]), str(follows[u])))
		
def printParseTable():
	global rule_dict, firsts, follows, grammer, parse_table
	# final state of parse table
	print("\nGenerated parsing table:\n")
	column_width = 0
	for nt in parse_table:
		for t in parse_table[nt] :
			column_width = max(column_width, len(parse_table[nt][t]))

	frmt = f"{{:>{max(15,column_width)}}}"* len(grammer["terminals"]) 
	print(frmt.format(*grammer["terminals"]))

	for nt in parse_table:
		print(nt, end = "")
		frmt = f"{{:>{max(15,column_width)}}}"* len(grammer["terminals"]) 
		print(frmt.format(*parse_table[nt].values()))

def createParseTable():
	global rule_dict, firsts, follows, garammer, table

	terminals = copy.deepcopy(grammer["terminals"])
	terminals.append('$')

	# create the initial empty state of ,matrix
	for nt in rule_dict :
		parse_table.setdefault(nt,{})
		for t in terminals :
			parse_table[nt].setdefault	(t,'')

	# Classifying grammar as LL(1) or not LL(1)
	grammar_is_LL = True

	# rules implementation
	for lhs_nt, rhs_rules in rule_dict.items():
		for sub_rule in rhs_rules:
			t_list = first(sub_rule)
			if t_list is not None and '#' in t_list: # epsilon is present, take union with follow
				t_list.remove('#')
				t_list = set(list(t_list) + list(follows[lhs_nt]))

			for t in t_list :
				if parse_table[lhs_nt][t] == '':
					parse_table[lhs_nt][t] = f"{lhs_nt}->{' '.join(sub_rule)}"
				else :
					# if rule already present
					if f",{lhs_nt}->{' '.join(sub_rule)}" in parse_table[lhs_nt][t]:
						continue
					else:
						grammar_is_LL = False
						parse_table[lhs_nt][t] = parse_table[lhs_nt][t] + f",{lhs_nt}->{' '.join(sub_rule)}"
	printParseTable()
	return grammar_is_LL

def LL1_PARSE(grammer, is_grammarll1, input_string, parse_table):
	print(f"\nValidate String => {input_string}\n")

	# for more than one entries in one cell of parsing table not LL1 grammer
	if is_grammarll1 == False:
		return f"\nInput String = \"{input_string}\"\n Grammar is not LL(1)"

	buffer = deque(input_string.split())
	buffer.append('$')

	stack = ['$', grammer["start_symbol"]]

	while(True) :
		if(buffer[0] == stack[-1] and stack[-1] == '$') :
			print("{:>20} {:>20} {:>20}".format(' '.join(buffer),' '.join(stack),"Valid"))
			return "\nValid String!"

		elif stack[-1] in grammer["terminals"] :
			if stack[-1] == buffer[0] :
				print("{:>20} {:>20} {:>20}".format(' '.join(buffer),' '.join(stack),f"Matched:{stack[-1]}"))
				buffer.popleft()
				stack.pop()
			else :
				return "\nInvalid String! Unmatched terminal symbols"
		else :
			next_sub_rule = parse_table.get(stack[-1],'')
			if(next_sub_rule != '') :
				next_sub_rule = next_sub_rule.get(buffer[0], '')

			if(next_sub_rule == '') :
				return f"\nInvalid String! No rule at Table[{stack[-1]}][{buffer[0]}]."
			else :
				print("{:>20} {:>20} {:>25}".format(' '.join(buffer),' '.join(stack), f"T[{stack[-1]}][{buffer[0]}] = {next_sub_rule}"))
				stack.pop()
				rhs = next_sub_rule.split('->')[1]
				rhs = rhs.replace('#', '').strip().split()
				stack += reversed(rhs)


# CODE BEGINS HERE
if __name__ == "__main__" :
	input_string = "id id + id )"  


	formatRules() 					#format rules in form of dictionary
	computeAllFirsts() 				# computes all FIRSTs for all non terminals
	computeAllFollows()     		# computes all FOLLOWs for all occurrences 
	printFirstFOllowTable()     	# generate formatted first and follow table
	result = createParseTable()     # then generate parse table 

	validity = LL1_PARSE(grammer, result, input_string, parse_table)
	print(validity)

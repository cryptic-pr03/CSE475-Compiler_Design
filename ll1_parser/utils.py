def print_rule_dict(rule_dict) :
    print(f"\nRules Dict: \n")
    for lhs, subrules in rule_dict.items():
        print(f"{lhs} -> {subrules}")

def print_FIRST(FIRST) :
    print("\nCalculated FIRST: ")
    for lhs_nt, first_set in FIRST.items():
        print(f"first({lhs_nt}) => {first_set}")

def print_FOLLOW(FOLLOW) :
	print("\nCalculated FOLLOW: ")
	for lhs, follow_set in FOLLOW.items():
		print(f"follow({lhs}) => {follow_set}")
          
def print_first_follow_table(FIRST, FOLLOW, rule_dict) :
	
	print("\nFirsts and Follow table:")
	# find space size
	mx_len_first = 0
	mx_len_fol = 0
	for u in rule_dict:
		k1 = len(str(FIRST[u]))
		k2 = len(str(FOLLOW[u]))
		if k1 > mx_len_first:
			mx_len_first = k1
		if k2 > mx_len_fol:
			mx_len_fol = k2

	print(f"{{:<{10}}} "
		f"{{:<{mx_len_first + 5}}} {{:<{mx_len_fol + 5}}}".format("Non-T", "FIRST", "FOLLOW"))
	for u in rule_dict:
		print(f"{{:<{10}}} {{:<{mx_len_first + 5}}} {{:<{mx_len_fol + 5}}}".format(u, str(FIRST[u]), str(FOLLOW[u])))

# rule = "E' -> . + T E'"
# item = ("E'", "0", "0")
def print_item(item, rule_dict):
    (lhs, subrule_no, pos) = item
    rule_token = rule_dict[lhs][subrule_no].copy()
    rule_token.insert(pos,".")
    if rule_token[-1] == "#" :
        rule_token.pop()
    itemm = lhs + " -> " + " ".join(rule_token)
    print(itemm)

def print_itemset(I, rule_dict) :
    for item in I:
        print_item(item, rule_dict)
    print("\n")

def print_subrule(lhs, subrule_no, rule_dict):
    subrule = rule_dict[lhs][subrule_no]
    print(f"{lhs} -> {' '.join(subrule)}")


def print_DFA(state,edges) :
    print("\nDFA:")
    for i in range(len(state)):
        print(f"[{i}]")
        print_itemset(state[i])
    
    for e in edges.items():
        print(e)
        print("-"*20)
        print_itemset(state[e[0][0]])
        print(f"\t|\n\t| {e[0][1]}\n\t|\n\t\/\n")
        print_itemset(state[e[1]])
        print("\n")

def print_parse_table(parse_table, G):
	# global rule_dict, firsts, follows, grammer, parse_table
	# final state of parse table
	print("\nGenerated parsing table:\n")
	column_width = 0
	for nt in parse_table:
		for t in parse_table[nt] :
			column_width = max(column_width, len(parse_table[nt][t]))

	frmt = f"{{:>{max(15,column_width)}}}"* len(G.terminals) 
	print(frmt.format(*G.terminals))

	for nt in parse_table:
		print(nt, end = "")
		frmt = f"{{:>{max(15,column_width)}}}"* len(G.terminals) 
		print(frmt.format(*parse_table[nt].values()))


def print_parse_state(state_stack, symbol_stack, input_buffer) :
    state_str = ' '.join([str(x) for x in state_stack]).ljust(25)
    symbol_str = ' '.join(symbol_stack).ljust(25)
    buffer_str = ' '.join(input_buffer).ljust(25)

    output = f"{state_str}{symbol_str}{buffer_str}"
    print(output, end = "")
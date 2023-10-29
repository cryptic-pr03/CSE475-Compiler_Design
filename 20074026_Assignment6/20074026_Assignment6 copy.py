# each grammar_symbol must be separated by exactly 1 space
# the arrow must be represented by "->"
# all terminals, non_terminals must be listed
# start symbol may be mentioned : by default(G[0].split()[0])


grammar = {
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

G = grammar["rules"]
'''
G = [
    rule0,
    rule1,
    .
    .
]
rule = "lhs -> rhs"
lhs = lhs_nt
rhs = "subrule0 | subrule1 | subrule2"
subrule = x0 x1 x2 ... 

e.g.
"E' -> + T E' | #"
rule = E' -> + T E' | #

lhs = E
rhs = + T E' | #
subrules = ["+ T E'", ["#"]]     -----> [['+', 'T', "E'"], ['#']]
'''

non_terminals =  grammar["non_terminals"]
terminals = grammar["terminals"]
start_symbol = grammar["start_symbol"]

# create augumented grammar
AG = []
AG = G
if(AG[0] != f"X -> {start_symbol}") :
    AG.insert(0, f"X -> {start_symbol}")

'''
rule_dict = {
	{lhs_nt1, [subrule11, subrule12, ... ]},
	{lhs_nt2, [subrule21, subrule22, ... ]},
	.
	.
	.
}
e.g.
"E' -> + T E' | #"
rule_dict {
	{E : [["+", "T", "E'"], ["#"]]}
}


'''
rule_dict = {} # store production rules inputted in formatted manner

def formatRules():
	# populating rule_dict
	for rule in AG:
		lhs, rhs = [r.strip() for r in rule.split("->")]	
		subrules = rhs.split('|')

		for i in range(len(subrules)):
			subrules[i] = subrules[i].strip()
			subrules[i] = subrules[i].split()

		rule_dict[lhs] = subrules

	print(f"\nRules Dict: \n")
	for lhs_nt, subrules in rule_dict.items():
		print(f"{lhs_nt} -> {subrules}")

formatRules()


#COMPUTE FIRST 
FIRST = {} # store computed FIRST

#e.g. subrule = ['+', 'T', "E'"] or ["#"] 

def first(subrule) -> None | list:
	# recursion base condition (for terminal or epsilon)
	if not subrule or len(subrule) == 0:
		return None
	
	if subrule[0] in terminals or subrule[0] == '#' :
		return [subrule[0]] 
	else :
		if subrule[0] in list(rule_dict.keys()):		# ensuring that subrule for next_non_terminal exists
			temp_res = [] 			
			next_nt_rules = rule_dict[subrule[0]]
			for next_rule in next_nt_rules:
				next_first = first(next_rule)
				if next_first is not None:
					temp_res = temp_res + next_first

			# if no epsilon in result  - received return temp_res
			if '#' not in temp_res:
				return temp_res
			else:
				# apply epsilon subrule => f(ABC)=f(A)-{e} U f(BC)
				temp_res.remove('#')
				if len(subrule) > 1:
					new_ans = first(subrule[1:])
					if new_ans is not None:
						temp_res = temp_res + new_ans
					return temp_res
				 
				# lastly if eplison still persists - keep it in result of first
				temp_res.append('#')
				return temp_res
		else :
			return None
		
def computeAllFIRST():
	# calculate first for each subrule - (call first() on all RHS)
	for lhs, subrules in rule_dict.items() : 
		first_set = set()
		for subrule in subrules:
			temp = first(subrule)
			if temp is not None:
				for t in temp:
					first_set.add(t)
		FIRST[lhs] = list(first_set)

	print("\nCalculated FIRST: ")
	for lhs_nt, first_set in FIRST.items():
		print(f"first({lhs_nt}) => {first_set}")

computeAllFIRST()

FOLLOW = {} # store computed FOLLOW

def follow(nt) -> list:
	
	solset = set()
	
	# for start symbol return $ (recursion base case)
	if nt == start_symbol:
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

def computeAllFOLLOW():
	global grammar , rule_dict, FIRST, FOLLOW

	for lhs in rule_dict:
		FOLLOW[lhs] = follow(lhs)

	print("\nCalculated FOLLOW: ")
	for lhs, follow_set in FOLLOW.items():
		print(f"follow({lhs}) => {follow_set}")
computeAllFOLLOW()

def printFirstFOllowTable() :
	print("\nFirsts and Follow Result table:")
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
		
printFirstFOllowTable()

# rule = "E' -> . + T E'"
# item = ("E'", "0", "0")
def print_item(item):
    (lhs, subrule_no, pos) = item
    rule_token = rule_dict[lhs][subrule_no].copy()
    rule_token.insert(pos,".")
    if rule_token[-1] == "#" :
        rule_token.pop()
    itemm = lhs + " -> " + " ".join(rule_token)
    print(itemm)

def print_itemset(I) :
    for item in I:
        print_item(item)
    print("\n")

def print_subrule(lhs, subrule_no):
    subrule = rule_dict[lhs][subrule_no]
    print(f"{lhs} -> {' '.join(subrule)}")

# I = itemset where each item = (lhs, subrule_number, after how many elements in rhs(term/non-term) does dot appear)
# closure(I) = for all item A -> alpha . B beta; add production B -> .subruleB1, .subruleB2, ... until no furthur addition possible
def closure(I : list) -> list :
    J = I
    added = set()
    while(True) : 
        count = 0
        for (lhs, subrule_no, pos) in J :
            subrule = rule_dict[lhs][subrule_no].copy()
            if len(subrule) == pos or subrule[pos] == '#':         # dot appears at end
                continue 
            B = subrule[pos]    
            if B in non_terminals:         # A -> aplha . B beta
                if B not in added:         # B -> . subrule[0], . subrule[1], ... not already added 
                    for subrule_i in range(len(rule_dict[B])):
                            J.append((B, subrule_i,0))
                            count += 1
                    added.add(B)
        if count == 0:
            break;
    return J

#  goto(I, X) is defied to be the closure of the set of all items [A -> alpha B . beta ] such that [A -> alpha . B beta] is in I .
def goto(I, x) -> list:
    J = [] 
    for (lhs, subrule_no, pos) in I:
        subrule = rule_dict[lhs][subrule_no].copy()
        if len(subrule) == pos or subrule[pos] == '#':          # dot appears at end or 
            continue 
        B = subrule[pos] 
        if B == x :
            J.append((lhs,subrule_no, pos + 1))
    return closure(J)    

state = [] # canonical collection of sets = set of states
edges = {} # edges of dfa edges[(state_number, element)] = next_state

def generate_dfa() :
    global state, edges
    state = [closure([('X',0,0)])]
    while(True):
        count = 0
        for i in range(len(state)):
            I = state[i]
            for x in terminals + non_terminals:
                next_state = goto(I,x) 
                if len(next_state):
                    if next_state not in state:
                        state.append(next_state) 
                        count += 1;
                    edges.setdefault((i,x), state.index(next_state))
        if count == 0:
            break;    
generate_dfa()

def print_DFA(CCS,edges) :

    for i in range(len(CCS)):
        print(f"[{i}]")
        print_itemset(CCS[i])
    
    for e in edges.items():
        print(e)
        print("-"*20)
        print_itemset(CCS[e[0][0]])
        print(f"\t|\n\t| {e[0][1]}\n\t|\n\t\/\n")
        print_itemset(CCS[e[1]])
        print("\n")

# print_DFA(state, edges)

ACTION = []
GOTO = []
import copy
def generate_parse_table ():
    is_lr0_grammar = True

    global ACTION, GOTO, terminals
    terminals = copy.deepcopy(terminals) 
    if('$' not in terminals) :
        terminals.append('$')
    # create the initial empty state of ,matrix
    action = []
    goto = []

    for i in range(len(state)) :
        action.append(['']*len(terminals))
        goto.append([0]*len(non_terminals))

        for (lhs, subrule_no, pos) in state[i]: 
            subrule = rule_dict[lhs][subrule_no].copy()
            if pos == len(subrule) or subrule[pos] =='#':       # dot at last position 
                if(lhs == "X") :
                    action[i][terminals.index('$')] =   f"ACCEPT, " + action[i][terminals.index('$')]         #ACCEPT
                else :
                    for t in FOLLOW[lhs]:
                        action[i][terminals.index(t)] = f"R {lhs} {subrule_no}, " + action[i][terminals.index(t)]          #REDUCE


        for ti in range(len(terminals)):
            if (i,terminals[ti]) in edges:
                if action[i][ti]:
                    is_lr0_grammar = False
                action[i][ti] = f"S {edges[(i,terminals[ti])]}, " + action[i][ti]
            if(action[i][ti]) :             # REMOVING last ", " 
                action[i][ti] = action[i][ti][:-2]

        for nti in range(len(non_terminals)):
            if (i,non_terminals[nti]) in edges:
                goto[i][nti] = edges[(i,non_terminals[nti])]



    ACTION = action
    GOTO = goto
    return is_lr0_grammar

generate_parse_table()

def print_table(at,gt):

    #print headers1
    print(" ".ljust(10),end="|")
    print(f"{'-'*(len(terminals)*5-5)}ACTION TABLE{'-'*(len(terminals)*5-5)}", end = "|")
    print(f"{'-'*len(non_terminals)*2}GOTO TABLE{'-'*len(non_terminals)*2}", end = "|")
    print()

    #print header2
    print("STATE".ljust(15),end="")
    for t in terminals:
        print(t.ljust(10),end="")
    print(" ".ljust(3),end="")
    for nt in non_terminals:
        print(str(nt).ljust(5),end="")
    print("\n");

    for i in range(len(at)) :
        print(str(i).ljust(15), end= "")
        for ti in range(len(at[0])) :
            print(at[i][ti].ljust(10), end = "")
        print(" ".ljust(3),end="")
        for ti in range(len(gt[0])) :
            print(str(gt[i][ti]).ljust(5), end = "")
        print()

print_table(ACTION, GOTO)
is_lr0_grammar = generate_parse_table()

def print_parse_state(st, syt, buffer) :
    state_str = ' '.join([str(x) for x in st]).ljust(25)
    symbol_str = ' '.join(syt).ljust(25)
    buffer_str = ' '.join(buffer).ljust(25)

    output = f"{state_str}{symbol_str}{buffer_str}"
    print(output, end = "")
    
from collections import deque
def canonical_lr_parse(input_string, ACTION, GOTO, is_lr0_grammar) :
    if not is_lr0_grammar:
        return False
    symbol_stack = []
    state_stack = []
    buffer = deque(input_string.split())
    buffer.append("$")

    print("STATE STACK".ljust(25), "SYMBOL STACK".ljust(25), "INPUT BUFFER".ljust(25), "ACTION")
    print("-"*100)
    state_stack.append(0)

    while(True) :
        print_parse_state(state_stack.copy(), symbol_stack.copy(), buffer.copy())
        act = ACTION[state_stack[-1]][terminals.index(buffer[0])].split()

        if not act :        #ERROR
            print("ERROR")
            return False
        
        if act[0] == 'S':
            print(f"Shift to {act[1]}")
            symbol_stack.append(buffer[0])
            state_stack.append(int(act[1]))
            buffer.popleft()


        elif act[0] == 'R':
            lhs = act[1]
            subrule_no = int(act[2])
            subrule = rule_dict[lhs][subrule_no]
            print("Reduce", end = " ")
            print_subrule(lhs,subrule_no)

            if subrule == ["#"] :
                pass
            else:
                for _ in range(len(subrule)):
                    symbol_stack.pop()
                    state_stack.pop()

            symbol_stack.append(lhs)
            state_stack.append(GOTO[state_stack[-1]][non_terminals.index(lhs)])
            pass

        else :
            print("ACCEPTED\n") 
            return True
    

if( canonical_lr_parse("id + ( id + id ) ", ACTION, GOTO, is_lr0_grammar)):
    print("Parsing Successful\n")
else :
    print("Parsing Unsuccessful\n")
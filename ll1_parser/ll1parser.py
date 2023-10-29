from collections import deque

def LL1_PARSE(G, is_grammarll1, input_string, parse_table):
	print(f"\nValidate String => {input_string}\n")

	# for more than one entries in one cell of parsing table not LL1 G
	if is_grammarll1 == False:
		return f"\nInput String = \"{input_string}\"\n Grammar is not LL(1)"

	buffer = deque(input_string.split())
	buffer.append('$')

	stack = ['$', G.start_symbol]

	while(True) :
		if(buffer[0] == stack[-1] and stack[-1] == '$') :
			print("{:>20} {:>20} {:>20}".format(' '.join(buffer),' '.join(stack),"Valid"))
			return "\nValid String!"

		elif stack[-1] in G.terminals :
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


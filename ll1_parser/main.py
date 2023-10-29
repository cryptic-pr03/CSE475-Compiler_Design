import os
from grammar import read_grammar, Grammar
from firsts import computeAllFIRST
from follows import computeAllFOLLOW
from parse_table import generate_parse_table
from ll1parser import LL1_PARSE
import utils as cout


def augument_grammar(G : Grammar) :
    AG = G
    AG.rules.insert(0, f"X->{G.start_symbol}")
    AG.terminals.append('$')
    return AG

def format_rules(G : Grammar):
	# populating rule_dict
    rule_dict = {}
    for rule in G.rules:
        lhs, rhs = [r.strip() for r in rule.split("->")]	
        subrules = rhs.split('|')
        for i in range(len(subrules)):
            subrules[i] = subrules[i].strip()
            subrules[i] = subrules[i].split()
        rule_dict[lhs] = subrules
    cout.print_rule_dict(rule_dict)
    print(f"{'-'*50}")
    return rule_dict 



def main():
    #read grammar
    path = input("Enter Relative Path to grammar.txt (Default = 'grammaer.txt'): ")
    if path == '':
        path = "grammar.txt"
    full_path = os.path.join(os.getcwd(),path)
    G = read_grammar(full_path)
    G.terminals.append("$")
    print("GRAMMAR:\n", G, f"{'-'*50}")
    
    rule_dict = format_rules(G)  # for effective implementation

    # 1. Compute FIRST and FOLLOW
    FIRST = computeAllFIRST(G, rule_dict)
    FOLLOW = computeAllFOLLOW(G, rule_dict)
    cout.print_first_follow_table(FIRST, FOLLOW,rule_dict)

    # 2. generate parse table
    is_grammar_LL1, parse_table = generate_parse_table(G, rule_dict, FIRST, FOLLOW)
    cout.print_parse_table(parse_table, G)

    # 3. parse the input string
    input_string = input("Enter string to be parsed: ")
    validity = LL1_PARSE(G, is_grammar_LL1, input_string, parse_table)
    print(validity)

if __name__ == "__main__" :
    main()
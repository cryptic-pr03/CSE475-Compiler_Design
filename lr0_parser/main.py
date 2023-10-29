import os
from grammar import read_grammar, Grammar
import utils as cout

from dfa import generate_dfa
from parse_table import generate_parse_table
from lrparser import canonical_lr_parse

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

    print("GRAMMAR:\n", G, f"{'-'*50}")
    
    # 1. augument the grammer and add $ symbol in terminals
    AG = augument_grammar(G)
    rule_dict = format_rules(AG)  # for effective implementation

    # 2. generate DFA, Canonical Closure of sets along with the transitions
    DFA = generate_dfa(AG, rule_dict)

    # 3. generate parse table 
    is_lr0_grammar, parse_table =  generate_parse_table(G, rule_dict, DFA)        

    # 4. parse the input string
    input_string = input("Enter string to be parsed: ")
    if( canonical_lr_parse(AG, input_string, parse_table, is_lr0_grammar, rule_dict)):
        print("Parsing Successful\n")
    else :
        print("Parsing Unsuccessful\n")

if __name__ == "__main__" :
    main()
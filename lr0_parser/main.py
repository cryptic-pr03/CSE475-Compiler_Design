import os
from grammar import read_grammar, Grammar, format_rules
import utils as cout

from dfa import generate_dfa
from parse_table import generate_parse_table
from paarser import slr1_parse

def augument_grammar(G : Grammar) :
    AG = G
    AG.rules.insert(0, f"X -> {G.start_symbol}")
    AG.terminals.append('$')
    AG.non_terminals.append('X')
    AG.start_symbol = "X"
    return AG

def main():
    #read grammar
    path = input("Enter Relative Path to grammar.txt (Default = 'grammaer.txt'): ").strip()
    if path == '':
        path = "grammar.txt"
    full_path = os.path.join(os.getcwd(),path)
    G = read_grammar(full_path)

    print("GRAMMAR:\n", G)
    
    # 1. augument the grammer and add $ symbol in terminals
    AG = augument_grammar(G)

    rule_dict = format_rules(AG)  # for effective implementation
    cout.print_rule_dict(rule_dict)

    # 2. generate DFA, Canonical Closure of sets along with the transitions
    DFA = generate_dfa(AG, rule_dict)
    cout.print_DFA(DFA, rule_dict)

    # 3. generate parse table 
    is_lr0_grammar, parse_table =  generate_parse_table(G, rule_dict, DFA)     
    cout.print_table(G, parse_table)   

    if not is_lr0_grammar:
        print("NOT LRO GRAMMAR")
        return
    
    # 4. parse the input string
    input_string = input("Enter string to be parsed: ")
    if( slr1_parse(AG, input_string, parse_table, is_lr0_grammar, rule_dict)):
        print("Parsing Successful\n")
    else :
        print("Parsing Unsuccessful\n")

if __name__ == "__main__" :
    main()
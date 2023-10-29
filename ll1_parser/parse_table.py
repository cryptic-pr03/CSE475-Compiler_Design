from grammar import Grammar
from firsts import first

def generate_parse_table (G: Grammar, rule_dict : dict, FIRST : list, FOLLOW : list):
    '''
    Returns: 
        tuple(is_lr0_grammar, action, goto)
        is_lr0_grammar (bool): if grammar is lr0
        ACTION (list) : ACTION[index_of_state][index_of_terminal]
        GOTO (list) : ACTION[index_of_state][index_of_non_terminal]
    '''
    parse_table = {}

	# create the initial empty state of ,matrix
    for nt in rule_dict :
        parse_table.setdefault(nt,{})
        for t in G.terminals :
            parse_table[nt].setdefault	(t,'')

	# Classifying grammar as LL(1) or not LL(1)
    grammar_is_LL = True

	# rules implementation
    for lhs_nt, rhs_rules in rule_dict.items():
        for sub_rule in rhs_rules:
            t_list = first(sub_rule, G, rule_dict)
            if t_list is not None and '#' in t_list: # epsilon is present, take union with follow
                t_list.remove('#')
                t_list = set(list(t_list) + list(FOLLOW[lhs_nt]))

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
    
    return grammar_is_LL, parse_table

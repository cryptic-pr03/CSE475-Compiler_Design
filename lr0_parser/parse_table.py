from grammar import Grammar
from dfa import DFA
import utils as cout
class Table :
    def __init__(self, ACTION, GOTO):
        self.ACTION = ACTION
        self.GOTO = GOTO

def generate_parse_table (G: Grammar, rule_dict : dict, dfa : DFA):
    '''
    Returns: 
        tuple(is_lr0_grammar, action, goto)
        is_lr0_grammar (bool): if grammar is lr0
        ACTION (list) : ACTION[index_of_state][index_of_terminal]
        GOTO (list) : ACTION[index_of_state][index_of_non_terminal]
    '''
    
    is_lr0_grammar = True
    # create the initial empty dfa.states of ,matrix
    action = []
    goto = []

    for i in range(len(dfa.states)) :
        action.append(['']*len(G.terminals))
        goto.append([0]*len(G.non_terminals))

        for (lhs, subrule_no, pos) in dfa.states[i]: 
            subrule = rule_dict[lhs][subrule_no].copy()
            if pos == len(subrule) or subrule[pos] =='#':       # dot at last position 
                if(lhs == "X") :
                    action[i][G.terminals.index('$')] =   f"ACCEPT, " + action[i][G.terminals.index('$')]         #ACCEPT
                else :
                    for t in G.terminals:
                        action[i][G.terminals.index(t)] = f"R {lhs} {subrule_no}, " + action[i][G.terminals.index(t)]          #REDUCE


        for ti in range(len(G.terminals)):
            if (i,G.terminals[ti]) in dfa.edges:
                if action[i][ti]:
                    is_lr0_grammar = False
                action[i][ti] = f"S {dfa.edges[(i,G.terminals[ti])]}, " + action[i][ti]
            if(action[i][ti]) :             # REMOVING last ", " 
                action[i][ti] = action[i][ti][:-2]

        for nti in range(len(G.non_terminals)):
            if G.non_terminals.index(G.start_symbol) is not nti:
                if (i, G.non_terminals[nti]) in dfa.edges:
                    goto[i][nti] = dfa.edges[(i, G.non_terminals[nti])]

    parse_table = Table(action, goto)
    return is_lr0_grammar, parse_table

# LR_0 DFA
from goto_closure import goto, closure
from grammar import Grammar

class DFA :
    def __init__(self, states, edges) :
        self.states = states
        self.edges = edges

    
def generate_dfa(G : Grammar, rule_dict : dict):
    '''
    Returns: 
        tuple(states, edges)
        states (list) : canonical collection of sets = set of states
        edges (dict(tuple(int,str), int)) : edges of dfa edges[(state_number, element)] = next_state
    '''
    states = [closure([('X',0,0)], G , rule_dict)] 
    edges = {}

    while(True):
        count = 0
        for i in range(len(states)):
            I = states[i]
            for x in G.terminals + G.non_terminals:
                next_state = goto(I,x, G, rule_dict) 
                if len(next_state):
                    if next_state not in states:
                        states.append(next_state) 
                        count += 1;
                    edges.setdefault((i,x), states.index(next_state))
        if count == 0:
            break;  
    return DFA(states,edges)

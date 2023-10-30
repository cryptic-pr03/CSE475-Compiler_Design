from grammar import Grammar

# I = itemset where each item = (lhs, subrule_number, after how many elements in rhs(term/non-term) does dot appear)
def closure(I : list, G : Grammar, rule_dict : dict) -> list :
    '''
    closure(I) = for all item A -> alpha . B beta; add production B -> .subruleB1, .subruleB2, ... until no furthur addition possible
    Args:
        I (list(tuple)): item set/ state in dfa
        G (Grammar) : CFG instance of Grammar class
        rule_dict (list) : Formatted Rules
    '''
    J = I
    added = set()
    while(True) : 
        count = 0
        for (lhs, subrule_no, pos) in J :
            subrule = rule_dict[lhs][subrule_no].copy()
            if len(subrule) == pos or subrule[pos] == '#':         # dot appears at end
                continue 
            B = subrule[pos]    
            if B in G.non_terminals:         # A -> aplha . B beta
                if B not in added:         # B -> . subrule[0], . subrule[1], ... not already added 
                    for subrule_i in range(len(rule_dict[B])):
                            J.append((B, subrule_i,0))
                            count += 1
                    added.add(B)
        if count == 0:
            break;
    return J

def goto(I : list[tuple], x : str, G : Grammar, rule_dict : dict) -> list:
    '''
    goto(I, X) is defied to be the closure of the set of all items [A -> alpha B . beta ] such that [A -> alpha . B beta] is in I .
    Args:
        I (list(tuple)): item set/ state in dfa
        x (str) : grammar symbol
        G (Grammar) : CFG instance of Grammar class
        rule_dict (list) : Formatted Rules
    '''
    J = [] 
    for (lhs, subrule_no, pos) in I:
        subrule = rule_dict[lhs][subrule_no].copy()
        if len(subrule) == pos or subrule[pos] == '#':          # dot appears at end or 
            continue 
        B = subrule[pos] 
        if B == x :
            J.append((lhs,subrule_no, pos + 1))
    return closure(J,G,rule_dict)    

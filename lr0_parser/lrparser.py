import utils as cout    
from collections import deque
from grammar import Grammar
from parse_table import Table

def canonical_lr_parse(G : Grammar, input_string : str, table : Table, is_lr0_grammar : bool, rule_dict : dict) :
    if not is_lr0_grammar:
        return False
    symbol_stack = []
    state_stack = []
    buffer = deque(input_string.split())
    buffer.append("$")
    print("parsing...")
    
    print("STATE STACK".ljust(25), "SYMBOL STACK".ljust(25), "INPUT BUFFER".ljust(25), "table.ACTION")
    print("-"*100)
    state_stack.append(0)

    while(True) :
        cout.print_parse_state(state_stack.copy(), symbol_stack.copy(), buffer.copy())
        act = table.ACTION[state_stack[-1]][G.terminals.index(buffer[0])].split()

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
            cout.print_subrule(lhs,subrule_no, rule_dict)

            if subrule == ["#"] :
                pass
            else:
                for _ in range(len(subrule)):
                    symbol_stack.pop()
                    state_stack.pop()

            symbol_stack.append(lhs)
            state_stack.append(table.GOTO[state_stack[-1]][G.non_terminals.index(lhs)])
            pass

        else :
            print("ACCEPTED\n") 
            return True
    

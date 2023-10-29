ACTION_TABLE = {}
GOTO_TABLE = {}
G = {}

def init_grammar():
    G[1] = ('E', 'TA')
    G[2] = ('A', '+TA')
    G[3] = ('A', 'epsilon')
    G[4] = ('T', 'FB')
    G[5] = ('B', '*FB')
    G[6] = ('B', 'epsilon')
    G[7] = ('F', '(E)')
    G[8] = ('F', 'i')

def init_action_table():
    ACTION_TABLE[(0, '(')] = "s4"
    ACTION_TABLE[(0, 'i')] = "s5" 
    ACTION_TABLE[(1, '$')] = "acc"
    ACTION_TABLE[(2, '+')] = "s7"
    ACTION_TABLE[(2, '$')] = "r3"
    ACTION_TABLE[(3, '+')] = "r6"
    ACTION_TABLE[(3, '*')] = "s9"
    ACTION_TABLE[(3, '$')] = "r6"
    ACTION_TABLE[(4, '(')] = "s13"
    ACTION_TABLE[(4, 'i')] = "s14"
    ACTION_TABLE[(5, '+')] = "r8"
    ACTION_TABLE[(5, '*')] = "r8"
    ACTION_TABLE[(5, '$')] = "r8"
    ACTION_TABLE[(6, '$')] = "r1"
    ACTION_TABLE[(7, '(')] = "s4"
    ACTION_TABLE[(7, 'i')] = "s5"
    ACTION_TABLE[(8, '+')] = "r4"
    ACTION_TABLE[(8, '$')] = "r4"
    ACTION_TABLE[(9, '(')] = "s4"
    ACTION_TABLE[(9, 'i')] = "s5"
    ACTION_TABLE[(10, ')')] = "s17"
    ACTION_TABLE[(11, '+')] = "s19"
    ACTION_TABLE[(11, ')')] = "r3"
    ACTION_TABLE[(12, '+')] = "r6"
    ACTION_TABLE[(12, '*')] = "s21"
    ACTION_TABLE[(12, ')')] = "r6"
    ACTION_TABLE[(13, '(')] = "s13"
    ACTION_TABLE[(13, 'i')] = "s14"
    ACTION_TABLE[(14, '+')] = "r8"
    ACTION_TABLE[(14, '*')] = "r8"
    ACTION_TABLE[(14, ')')] = "r8"
    ACTION_TABLE[(15, '+')] = "s7"
    ACTION_TABLE[(15, '$')] = "r3"
    ACTION_TABLE[(16, '+')] = "r6"
    ACTION_TABLE[(16, '*')] = "s9"
    ACTION_TABLE[(16, '$')] = "r6"
    ACTION_TABLE[(17, '+')] = "r7"
    ACTION_TABLE[(17, '*')] = "r7"
    ACTION_TABLE[(17, '$')] = "r7"
    ACTION_TABLE[(18, ')')] = "r1"
    ACTION_TABLE[(19, '(')] = "s13"
    ACTION_TABLE[(19, 'i')] = "s14"
    ACTION_TABLE[(20, '+')] = "r4"
    ACTION_TABLE[(20, ')')] = "r4"
    ACTION_TABLE[(21, '(')] = "s13"
    ACTION_TABLE[(21, 'i')] = "s14"
    ACTION_TABLE[(22, ')')] = "s27"
    ACTION_TABLE[(23, '$')] = "r2"
    ACTION_TABLE[(24, '+')] = "r5"
    ACTION_TABLE[(24, '$')] = "r5"
    ACTION_TABLE[(25, '+')] = "s19"
    ACTION_TABLE[(25, ')')] = "r3"
    ACTION_TABLE[(26, '+')] = "r6"
    ACTION_TABLE[(26, '*')] = "s21"
    ACTION_TABLE[(26, ')')] = "r6"
    ACTION_TABLE[(27, '+')] = "r7"
    ACTION_TABLE[(27, '*')] = "r7"
    ACTION_TABLE[(27, ')')] = "r7"
    ACTION_TABLE[(28, ')')] = "r2"
    ACTION_TABLE[(29, '+')] = "r5"
    ACTION_TABLE[(29, ')')] = "r5"

def init_goto_table():
    GOTO_TABLE[(0, 'E')] = 1
    GOTO_TABLE[(0, 'T')] = 2
    GOTO_TABLE[(0, 'F')] = 3
    GOTO_TABLE[(2, 'A')] = 6
    GOTO_TABLE[(3, 'B')] = 8
    GOTO_TABLE[(4, 'E')] = 10
    GOTO_TABLE[(4, 'T')] = 11
    GOTO_TABLE[(4, 'F')] = 12
    GOTO_TABLE[(7, 'T')] = 15
    GOTO_TABLE[(7, 'F')] = 3
    GOTO_TABLE[(9, 'F')] = 16
    GOTO_TABLE[(11, 'A')] = 18
    GOTO_TABLE[(12, 'B')] = 20
    GOTO_TABLE[(13, 'E')] = 22
    GOTO_TABLE[(13, 'T')] = 11
    GOTO_TABLE[(13, 'F')] = 12
    GOTO_TABLE[(15, 'A')] = 23
    GOTO_TABLE[(16, 'B')] = 24
    GOTO_TABLE[(19, 'T')] = 25
    GOTO_TABLE[(19, 'F')] = 12
    GOTO_TABLE[(21, 'F')] = 26
    GOTO_TABLE[(25, 'A')] = 28
    GOTO_TABLE[(26, 'B')] = 29

def print_state_symbol(st, syt, s, index):
    state_str = ' '.join((str(st.pop())[::-1]) for _ in range(len(st)))
    state_str = state_str[::-1]  # Reverse the state stack
    state_str = state_str.ljust(25)

    symbol_str = ''
    while len(syt) > 0:
        if syt[-1] == 'i':
            symbol_str += 'd'
        symbol_str += syt.pop()
    symbol_str = symbol_str[::-1]  # Reverse the symbol stack
    symbol_str = symbol_str.ljust(18)

    remaining_input = s[index:]
    remaining_input = remaining_input.ljust(20)

    output = f"{state_str}{symbol_str}{remaining_input}"
    print(output, end = "")


def canonical_lr_parser(s):
    state_stack = []
    symbol_stack = []

    symbol_stack.append('$')
    state_stack.append(0)
    print("STATE STACK".ljust(22), "SYMBOL STACK".ljust(18), "INPUT BUFFER".ljust(20), "ACTION".ljust(20))
    index = 0
    while True:
        print_state_symbol(state_stack.copy(), symbol_stack.copy(), s, index)
        tp = state_stack[-1]

        if (tp, s[index]) not in ACTION_TABLE:
            return False

        act = ACTION_TABLE[(tp, s[index])]

        if act[0] == 's':
            act = int(act[1:])
            state_stack.append(act)
            symbol_stack.append(s[index])
            index += 1
            print(f"Shift to {act}")
        elif act[0] == 'r':
            act = int(act[1:])
            red = G[act]

            len_red = len(red[1])
            if red[1] == "epsilon":
                len_red = 0

            for _ in range(len_red):
                state_stack.pop()
                symbol_stack.pop()

            t = state_stack[-1]

            if (t, red[0]) not in GOTO_TABLE:
                return False

            state_stack.append(GOTO_TABLE[(t, red[0])])
            symbol_stack.append(red[0])
            print(f"Reduce by {red[0]} --> {red[1]}")
        elif act == "acc":
            print("Accepted")
            return True
        else:
            return False

def main():
    init_grammar()
    init_action_table()
    init_goto_table()

    # exp = "id*(id+id)+id"
    exp = input("Enter the expression: ")
    exp = exp.replace(" ", "")
    exp = exp.replace("d", "")
    exp += '$'
    print(exp)

    if canonical_lr_parser(exp):
        print("\nParsing successful!!")
    else:
        print("\nError!!")

if __name__ == "__main__":
    main()

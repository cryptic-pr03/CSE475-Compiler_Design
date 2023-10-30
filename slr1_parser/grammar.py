def get_terminals(rules : list) -> list:
    terms = set()
    for rule in rules:
        lhs, rhs = rule.split('->')
        subrules = rhs.split("|")
        for subrule in subrules:
            subrule = subrule.strip()
            subrule = subrule.split()

            for x in subrule :
                if not x[0].isupper() and x!="#":
                    terms.add(x)
    return list(terms)

def get_non_terminals(rules : list) -> list:
    non_terminals = set()
    for rule in rules:
        lhs, rhs = rule.split('->')
        non_terminals.add(lhs.strip())
        subrules = rhs.split("|")
        for subrule in subrules:
            subrule = subrule.strip()
            subrule = subrule.split()

            for x in subrule :
                if x[0].isupper() and x != "#":
                    non_terminals.add(x)

    return list(non_terminals)

def get_start_symbol(rules: list) -> str :
    return rules[0].split()[0]


class Grammar:
    '''
    A class containing the grammar
    Members:
        rules (list) : contains the production rules
        no_of_terminals (int) : count of terminals of the grammar 
            (epsilon = # not a terminal, end_marker = $ not included)
        terminals (list) : contains the terminals of the grammar 
            (epsilon = # not a terminal, end_marker = $ not included)
        no_of_non_terminals (int) : count of non_terminals of the grammar 
        non_terminals (list) : contains the non_terminals of the grammar 
        start_symbol (str) : the start symbol of the grammar
    '''
    def __init__(self, rules : list) -> None :
        self.rules = rules
        self.terminals = get_terminals(rules)
        self.non_terminals = get_non_terminals(rules)
        self.start_symbol = get_start_symbol(rules)
        self.no_of_terminals = len(self.terminals)
        self.no_of_non_terminals = len(self.non_terminals)
    
    def __repr__(self):
        res = "rules = [\n" 
        for rule in self.rules :
            res +=  "\t" + rule + "\n"
        res += "]\n\n"
        res += "no_of_terminals = " + str(self.no_of_terminals) + "\n"
        res += "terminals = " + str(self.terminals) + "\n\n"
        res += "no_of_non_terminals = " + str(self.no_of_non_terminals) + "\n"
        res += "non_terminals = " + str(self.non_terminals) + "\n\n"
        res += "start_symbol = " + str(self.start_symbol) + "\n"
        return res

def read_grammar(full_path : str) :
    '''
    Reads the grammar into an object of Grammar class
    Args:
        full_path (str): absolute path to the grammar text file

    Returns :
        grammar object 
    '''
    rules = []
    with open(full_path, 'r') as fp:
        for i in fp.readlines():
            rules.append(i.strip())

    G = Grammar(rules)
    return G

def format_rules(G : Grammar):
	# populating rule_dict
    rule_dict = {}
    for rule in G.rules:
        lhs, rhs = [r.strip() for r in rule.split("->")]	
        subrules = rhs.split('|')
        for i in range(len(subrules)):
            subrules[i] = subrules[i].strip()
            subrules[i] = subrules[i].split()

        if(lhs not in rule_dict):
            rule_dict[lhs] = []
        for subrule in subrules:
            rule_dict[lhs].append(subrule)
    return rule_dict
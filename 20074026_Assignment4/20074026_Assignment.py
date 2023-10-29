# __AUTHOR__ = Priyanshu Raman
# Recursive descent parser
SUCCESS = True
FAILURE = False

class Parser :
    def __init__(self, input_string) -> None:
        self.s = input_string
        self.index = 0

    def match(self, c) -> bool:
        if(self.s[self.index] == c):
            self.index += 1
            return SUCCESS
        else:
            print(f"ERROR @index = {self.index}: Expected {c} found {self.s[self.index]}")
            return FAILURE
        
    def E(self) -> bool:
        return bool(
            self.T() and 
            self._E()
            )

    def _E(self) -> bool:
        if(self.s[self.index] == '+'):
            return bool(
                self.match('+') and 
                self.T() and 
                self._E()
                )
        else:
            return SUCCESS
        
    def T(self) -> bool:
        return bool(
            self.F() and 
            self._T()
            )

    def _T(self) -> bool:
        if(self.s[self.index] == '*'):
            return bool(
                self.match('*') and 
                self.F() and 
                self._T()
                )
        else :
            return SUCCESS

    def F(self) -> bool:
        if(self.s[self.index] == '('):
            return bool(
                self.match('(') and 
                self.E() and 
                self.match(')')
                )
        else :
            return bool(
                self.match('I')
                )

    def parse(self):
        self.s += '$'       #appending the terminating character
        self.s = self.s.replace("id",'I')       #replacing all id by I for match function compatibility
        print(f"Parsing {self.s} ...")

        result = self.E()    #parsing the expression

        if(result and self.index < len(self.s) and self.s[self.index] =='$'):
            print("PARSE SUCCESSFUL")
        else :
            print("PARSE UNSUCCESSFUL")


if __name__ == "__main__" :
    inp = input("Enter the expression:\n")
    p = Parser(inp)
    p.parse()
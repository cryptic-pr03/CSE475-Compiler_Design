# ALL COMMENTS ARE REMOVED ALREADY
# ASSUMING ONLY NON-STRING OPERATORS
# MISC OPERATORS AVOIDED

'''
TOKENS : 
    IDENTIFIERS 
    KEYWORDS
    OPERATORS
    SEPARATORS
    NUMBERS
'''
import re
import os

inputFilePath = ""
KEYWORDS_LIST = [
    "AddHandler", "AddressOf", "Alias", "AndAlso", "As", "Boolean", "ByRef", "Byte", "ByVal", "Call", "Case", "Catch", "CBool", "CByte", "CChar", "CDate", "CDec", "CDbl", "Char", "CInt", "Class", "CLng", "CObj", "Const", "Continue", "CSByte", "CShort", "CSng", "CStr", "CType", "Date", "Decimal", "Declare", "Default", "Delegate", "Dim", "DirectCast", "Do", "Double", "Each", "Else", "ElseIf", "End", "Enum", "Erase", "Error", "Event", "Exit", "False", "Finally", "For", "Friend", "Function", "Get", "GetType", "GetXMLNamespace", "Global", "GoTo", "Handles", "If", "Implements", "Imports", "In", "Inherits", "Integer", "Interface", "Is", "IsNot", "Let", "Lib", "Like", "Long", "Loop", "Me", "Mod", "Module", "MustInherit", "MustOverride", "MyBase", "MyClass", "Namespace", "Narrowing", "New", "Next", "Not", "Nothing", "NotInheritable", "NotOverridable", "Object", "Of", "On", "Operator", "Option", "Optional", "Or", "OrElse", "Out", "Overloads", "Overridable", "Overrides", "ParamArray", "Partial", "Private", "Property", "Protected", "Public", "RaiseEvent", "ReadOnly", "ReDim", "REM", "RemoveHandler", "Resume", "Return", "SByte", "Select", "Set", "Shadows", "Shared", "Short", "Single", "Static", "Step", "Stop", "String", "Structure", "Sub", "SyncLock", "Then", "Throw", "To", "True", "Try", "TryCast", "TypeOf", "UInteger", "ULong", "UShort", "Using", "Variant", "Wend", "When", "While", "Widening", "With", "WithEvents", "WriteOnly", "Xor"
]
#maxlen = 1
SEPARATORS_LIST = [
    ',',    # Used to separate items in a list, parameters in function calls, and elements in array initializers.
    ';',    # Rarely used; can be used to separate multiple statements on a single line.
    ':',    # Used to separate multiple statements on a single line or for the ternary conditional operator.
    '.',    # Used to access members (properties, methods, etc.) of objects and namespaces.
    '(',    # Used in function/method calls, grouping expressions, and defining method signatures.
    ')',    # Used in function/method calls, grouping expressions, and defining method signatures.
    '[',    # Used in arrays, attributes, and indexing operations.
    ']',    # Used in arrays, attributes, and indexing operations.
    '{',    # Used to define blocks of code, such as in control structures and method bodies.
    '}',    # Used to define blocks of code, such as in control structures and method bodies.
    '"',    # Used to define string literals.
    '#',    # Used for preprocessor directives (compiler directives) in some contexts.
]
#max_len = 3
OPERATORS_LIST= [
    "+",   # Addition
    "-",   # Subtraction
    "*",   # Multiplication
    "/",   # Division
    "\\",  # Integer Division
    "^",   # Exponentiation
    # "Mod",  # Modulus
    "=",   # Basic assignment
    "+=",  # Addition assignment: Adds the right-hand value to the left-hand variable and assigns the result to the variable.
    "-=",  # Subtraction assignment: Subtracts the right-hand value from the left-hand variable and assigns the result to the variable.
    "*=",  # Multiplication assignment: Multiplies the left-hand variable by the right-hand value and assigns the result to the variable.
    "/=",  # Division assignment: Divides the left-hand variable by the right-hand value and assigns the result to the variable.
    "\=",  # Integer division assignment: Performs integer division of the left-hand variable by the right-hand value and assigns the result to the variable.
    "^=",  # Exponentiation assignment: Raises the left-hand variable to the power of the right-hand value and assigns the result to the variable.
    "&=",  # Bitwise AND assignment: Performs bitwise AND between the left-hand variable and the right-hand value and assigns the result to the variable.
    "|=",  # Bitwise OR assignment: Performs bitwise OR between the left-hand variable and the right-hand value and assigns the result to the variable.
    "<<=", # Left shift assignment: Shifts the bits of the left-hand variable to the left by the number of positions specified in the right-hand value and assigns the result to the variable.
    ">>="  # Right shift assignment: Shifts the bits of the left-hand variable to the right by the number of positions specified in the right-hand value and assigns the result to the variable.
    "=",          # Equal to: Checks if two values are equal.
    "<>",         # Not equal to: Checks if two values are not equal.
    "<",          # Less than: Checks if the first value is less than the second value.
    ">",          # Greater than: Checks if the first value is greater than the second value.
    "<=",         # Less than or equal to: Checks if the first value is less than or equal to the second value.
    ">=",         # Greater than or equal to: Checks if the first value is greater than or equal to the second value.
    # "Is",         # Identity: Checks if two object references refer to the same object.
    # "IsNot"       # Non-identity: Checks if two object references do not refer to the same object.
    "&",       # Concats two strings.
    # "+",
    # "AndAlso",   # Logical AND operator with short-circuiting
    # "OrElse",    # Logical OR operator with short-circuiting
    # "Not",       # Logical NOT operator
    # "Xor",       # Logical XOR operator (exclusive OR)
    # "And",       # Bitwise AND operator
    # "Or",        # Bitwise OR operator
    # "Xor",       # Bitwise XOR operator (exclusive OR)
    # "Not",       # Bitwise NOT operator (bitwise complement)
    "<<",        # Left shift operator
    ">>"        # Right shift operator
]
#max_len = 4
WHITESPACES_LIST = [
    " ",
    "\n",
    "\t",
    " _\n"
]

OperatorsPresent = {}
SeparatorsPresent = {}
KeywordsPresent = {}
WrongStrPresent = {}
NumbersPresent = {}
LiteralsPresent = {}
IdentifiersPresent = {}

def isSeparator(str):
    return str in SEPARATORS_LIST
    
def isOperator(str):
    return str in OPERATORS_LIST

def isKeyword(str):
    return str in KEYWORDS_LIST

def isDigit(str):
    return re.match("[0-9]", str)

def isPunc(ch) :
    return not isDigit(ch) and not isAlpha(ch) and ch != '_';

def isIdentifier(str):
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    return re.match(pattern,str)

def isNumber(str):
    numberPattern = "^-?[0-9]+(\\.[0-9]+)?([eE][-+]?[0-9]+)?$"
    return re.match(numberPattern, str)

def parseTokens(str) :
    start = 0
    end = 0
    lenStr = len(str)
    print(lenStr)
    while end < lenStr and start <= end:
        print(start, end)
        ch = str[end]
        if isSeparator(ch) :
            end += 1
            if(ch == '"') :
                #check for literal
                closed = False
                while end < lenStr : 
                    if (str[end] == '"') :
                        closed = True
                        break
                    end += 1
                
                if not closed :
                    sub = str[start:end]
                    WrongLexeme[sub] = WrongLexeme.get(sub,0) + 1
                else :
                    sub = str[start +1 : end]
                    LiteralsPresent[sub] = LiteralsPresent.get(sub,0) + 1
                    SeparatorsPresent[sub] = SeparatorsPresent.get(ch,0) + 2 
                    end += 1
            else :
                SeparatorsPresent[ch] = SeparatorsPresent.get(ch,0) + 1
                end += 1
            start = end

        else :
            end += 1
            if isIdentifier(ch) :
                while( end < lenStr and isIdentifier(str[start: end])):
                    end += 1
                if(end != lenStr):
                    end -= 1
                sub = str[start : end]
                if isKeyword(sub) :
                    KeywordsPresent[sub] = KeywordsPresent.get(sub, 0) + 1
                else : 
                    IdentifiersPresent[sub] = IdentifiersPresent.get(sub, 0) + 1
                start = end

            elif isNumber(ch) :
                while ( end < lenStr and isNumber(str[start: end])):
                    end += 1
                if(end != lenStr):
                    end -= 1
                sub = str[start : end]
                NumbersPresent[sub] = NumbersPresent.get(sub, 0) + 1
                start = end

            else :
                while(end < lenStr and isOperator(str[start : end])) :
                    end += 1
                if(end != lenStr):
                    end -= 1       
                sub = str[start : end]
                OperatorsPresent[sub] = OperatorsPresent.get(sub, 0) + 1
                start = end
    pass
        

def printTokens():
    print(f"\n{len(KeywordsPresent)} - Keywords Present.")
    for keyword, count in KeywordsPresent.items():
        print(f"{keyword} : {count}")

    print(f"\n{len(IdentifiersPresent)} - Indentifiers Present.")
    for identifier, count in IdentifiersPresent.items():
        print(f"{identifier} : {count}")

    print(f"\n{len(NumbersPresent)} - Numbers Present.")
    for number, count in NumbersPresent.items():
        print(f"{number} : {count}")

    print(f"\n{len(OperatorsPresent)} - Operators Present.")
    for operator, count in OperatorsPresent.items():
        print(f"{operator} : {count}")

    print(f"\n{len(SeparatorsPresent)} - Separators Present.")
    for separator, count in SeparatorsPresent.items():
        print(f"{separator} : {count}")

    print(f"\n{len(WrongStrPresent)} - Wrong Lexemes Present.")
    for wrong, count in WrongStrPresent.items():
        print(f"{wrong} : {count}")

    print(f"\nPARSING SUCCESSFUL.")

if __name__ == "__main__":
    basePath = os.getcwd()
    inputFilePath = input("Enter the input relative path: ")
    path = os.path.join(basePath, inputFilePath)
    with open(path, 'r') as inputFile:
        for currentLine in inputFile:
            print(currentLine)
            parseTokens(currentLine)
    printTokens()

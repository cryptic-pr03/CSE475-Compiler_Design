from ply import lex
import re 
import os


# All tokens classes
tokens = [
    'LITERAL',
    'OPERATOR',
    'SEPARATOR',
    'NUMBER',
    'KEYWORD',
    'IDENTIFIER'
]

# List of all Keywords in descending order
KEYWORDS_LIST = ['Xor', 'WriteOnly', 'WithEvents', 'With', 'Widening', 'While', 'When', 'Wend', 'Variant', 'Using', 'UShort', 'ULong', 'UInteger', 'TypeOf', 'TryCast', 'Try', 'True', 'To', 'Throw', 'Then', 'SyncLock', 'Sub', 'Structure', 'String', 'Stop', 'Step', 'Static', 'Single', 'Short', 'Shared', 'Shadows', 'Set', 'Select', 'SByte', 'Return', 'Resume', 'RemoveHandler', 'ReadOnly', 'ReDim', 'RaiseEvent', 'REM', 'Public', 'Protected', 'Property', 'Private', 'Partial', 'ParamArray', 'Overrides', 'Overridable', 'Overloads', 'Out', 'OrElse', 'Or', 'Optional', 'Option', 'Operator', 'On', 'Of', 'Object', 'Nothing', 'NotOverridable', 'NotInheritable', 'Not', 'Next', 'New', 'Narrowing', 'Namespace', 'MyClass', 'MyBase', 'MustOverride', 'MustInherit', 'Module', 'Mod', 'Me', 'Loop', 'Long', 'Like', 'Lib', 'Let', 'IsNot', 'Is', 'Interface', 'Integer', 'Inherits', 'In', 'Imports', 'Implements', 'If', 'Handles', 'GoTo', 'Global', 'GetXMLNamespace', 'GetType', 'Get', 'Function', 'Friend', 'For', 'Finally', 'False', 'Exit', 'Event', 'Error', 'Erase', 'Enum', 'End', 'ElseIf', 'Else', 'Each', 'Double', 'Do', 'DirectCast', 'Dim', 'Delegate', 'Default', 'Declare', 'Decimal', 'Date', 'Continue', 'Const', 'Class', 'Char', 'Catch', 'Case', 'Call', 'CType', 'CStr', 'CSng', 'CShort', 'CSByte', 'CObj', 'CLng', 'CInt', 'CDec', 'CDbl', 'CDate', 'CChar', 'CByte', 'CBool', 'Byte', 'ByVal', 'ByRef', 'Boolean', 'As', 'AndAlso', 'Alias', 'AddressOf', 'AddHandler']

#List of all separators in desending order
SEPARATORS_LIST = [ ',', ';', ':', '.', '(', ')', '[', ']', '{', '}', '"', '#' ]

#List of all operators in desending order
OPERATORS_LIST= ['>>=', '<<=', '/=', '*=', '\\=', '^=', '&=', '|=', '<>=', '<=', '>=', '!=', '+=', '-=', '**', '//', '==', '+', 
'-', '*', '/', '\\', '^', '=', '<>', '<', '>', '&', '|', '%', # "Mod", # "Is", # "IsNot", # "+", # "AndAlso", # "OrElse",   # "Not", # "Xor", # "And", # "Or", # "Xor", # "Not"
]

# Regular expressions for tokens
def t_LITERAL(t):
    r'"[^"]*"'
    return t

t_OPERATOR = r"|".join(re.escape(op) for op in OPERATORS_LIST)
t_SEPARATOR = r"|".join(re.escape(sep) for sep in SEPARATORS_LIST)
t_NUMBER = r"[-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?"

def t_IDENTIFIER(t) :
    r'[a-zA-Z_][a-zA-Z0-9_]*' 
    t.type = 'KEYWORD'  if t.value in KEYWORDS_LIST else t.type
    return t

# Ignored characters (whitespace)
t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character: ", t.value[0])
    t.lexer.skip(1)

def t_COMMENT(t):
    r"\'.*"
    pass


if __name__ == "__main__" :
    basePath = os.getcwd()
    inputFilePath = input("Enter the input relative path: ")
    if inputFilePath == '' :
        inputFilePath = "test.vb"
    path = os.path.join(basePath, inputFilePath)
    with open(path, 'r') as inputFile:
        global vb_code
        vb_code = inputFile.read()

    #Building the lexer
    lexer = lex()

    # Reset the lexer and store a new input string.
    lexer.input(vb_code)

    while True:
        # Return the next token. Returns a special LexToken instance on success or None if the end of the input text has been reached.
        token = lexer.token()
        if not token:
            break
        print(token)

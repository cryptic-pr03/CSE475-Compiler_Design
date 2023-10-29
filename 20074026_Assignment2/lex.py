import re
import os

inputFilePath = ""
KEYWORDS_LIST = [
"AddHandler", "AddressOf", "Alias", "And", "AndAlso", "As", "Boolean", "ByRef", "Byte", "ByVal", "Call", "Case", "Catch", "CBool", "CByte", "CChar", "CDate", "CDbl", "CDec", "Char", "CInt", "Class", "CLng", "CObj", "Const", "Continue", "CSByte", "CShort", "CSng", "CStr", "CType", "CUInt", "CULng", "CUShort", "Date", "Decimal", "Declare", "Default", "Delegate", "Dim", "DirectCast", "Do", "Double", "Each", "Else", "ElseIf", "End", "Enum", "Erase", "Error", "Event", "Exit", "False", "Finally", "For", "Friend", "Function", "Get", "GetType", "GoSub", "GoTo", "Handles", "If", "Implements", "Imports", "In", "Inherits", "Integer", "Interface", "Is", "IsNot", "Let", "Lib", "Like", "Long", "Loop", "Me", "Mod", "Module", "MustInherit", "MustOverride", "MyBase", "MyClass", "Namespace", "Narrowing", "New", "Next", "Not", "Nothing", "NotInheritable", "NotOverridable", "Object", "Of", "On", "Operator", "Option", "Optional", "Or", "OrElse", "Out", "Overloads", "Overridable", "Overrides", "ParamArray", "Partial", "Private", "Property", "Protected", "Public", "RaiseEvent", "ReadOnly", "ReDim", "REM", "RemoveHandler", "Resume", "Return", "SByte", "Select", "Set", "Shadows", "Shared", "Short", "Single", "Static", "Step", "Stop", "String", "Structure", "Sub", "SyncLock", "Then", "Throw", "To", "True", "Try", "TryCast", "TypeOf", "UInteger", "ULong", "UShort", "Using", "Variant", "Wend", "When", "While", "Widening", "With", "WithEvents", "WriteOnly", "Xor"
]
PUNCTUATIONS_LIST = [' ', '+', '-', '*', '/', ',', ';', '>', '<', '=', '(', ')', '[', ']', '{', '}', '&', '|', '\n', '"', '!', '$', ':']
OPERATORS_LIST = ['+', '-', '*', '/', '>', '<', '=', '|', '&', '%', ':']

OperatorsPresent = {}
KeywordsPresent = {}
WrongStrPresent = {}
NumbersPresent = {}
IdentifiersPresent = {}

def isPunctuator(ch):
    if ch in PUNCTUATIONS_LIST:
        return True
    else :
        return False

def isOperator(ch):
    if ch in OPERATORS_LIST:
        return True
    else :
        return False

def isKeyword(str):
    if str in KEYWORDS_LIST:
        return True
    else :
        return False

def isDigit(ch):
    return re.match("[0-9]", ch)

def isIdentifierValid(str):
    if isPunctuator(str[0]) or isDigit(str[0]):
        return False
    if len(str) == 1:
        return True
    else:
        i = len(str) - 1
        while i >= 0:
            if isOperator(str[i]):
                return False
            i -= 1
    return True

def isNumber(str):
    numberPattern = "^-?[0-9]+(\\.[0-9]+)?([eE][-+]?[0-9]+)?$"
    return bool(re.match(numberPattern, str))

def parseTokens(str):
    start = 0
    end = 0
    lenStr = len(str)
    while end < lenStr and start <= end:
        ch = str[end]
        if not isPunctuator(ch):
            end += 1
        if (isPunctuator(ch) and start != end) or (end == lenStr and start != end):
            sub = str[start:end]
            if isKeyword(sub):
                KeywordsPresent[sub] = KeywordsPresent.get(sub, 0) + 1
            elif isNumber(sub):
                NumbersPresent[sub] = NumbersPresent.get(sub, 0) + 1
            elif isIdentifierValid(sub):
                IdentifiersPresent[sub] = IdentifiersPresent.get(sub, 0) + 1
            else:
                WrongStrPresent[sub] = WrongStrPresent.get(sub, 0) + 1
            start = end
        elif isPunctuator(ch) and start == end:
            if isOperator(ch):
                OperatorsPresent[ch] = OperatorsPresent.get(ch, 0) + 1
            end += 1
            start = end

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

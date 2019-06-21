#verify patterns with regular expression
import re
#keywords table
kwords = ['AND', 'ARRAY',
            'BOOLEAN',
            'CASE', 'CHAR','CONST',
            'DIV', 'DO', 'DOWNTO',
            'ELSE', 'END', 'FOR',
            'FUNCTION', 'GOTO',
            'IF','INTEGER',
            'LABEL', 'MOD',
            'NIL', 'NOT',
            'OF', 'OR',
            'POINTER','PROCEDURE','PROGRAM',
            'REAL', 'RECORD', 'REPEAT',
            'SET', 'STRING',
            'THEN', 'TO', 'TOKEN',
            'UNTIL', 'VAR', 'WHILE', 'WITH']
#functions of language
functions = ['WRITELN', 'READLN']
#tokens of language
tokens = {':=':'assign_op', '..':'dotdot', '.':'dot',
        ':':'colon', ';':'semicolon', ',':'comma',
        '[':'lb', ']':'rg', '(':'lp', ')':'rp',
        '=':'equal', '<=':'le', '>=':'ge','<>':'ne',
        '>':'gt', '<':'lt', '/':'divide', '-':'minus',
        '+':'plus', '*':'times','^':'simb_pointer','@':'ender'}

#here is the symbol table to store the ids values
symbol_table = {}
#used to store the lexemes
lexemes = []
lexemes2 = []

def removeComment(line):
    line = re.sub('\(\*.*\*\)', '', line)
    return line

def verifyAttrib(index, line):
    ver, li = verifyFloat(index, line)
    if(ver):
        line = li
        return line

    ver, li = verifyIntAttrib(index, line)
    if(ver):
        line = li

    ver, li = verifyId(index, line)
    if(ver):
        line = li

    verifyOther(index, line)
    return line


def hasPrintString(index, line):
    stri = 0 #qty of strings
    if(line.lower().find('writeln') > 0):
        if(re.search("'.*'", line)):
            aux = re.search("'.*'", line)
            line = re.sub("'.*'", '', line)
            stri += 1
            symbol_table['string{}:{}'.format(index+1,stri)] = 'line: {}, Lexeme: {} , token(string, {})\n'.format(index+1, 'string{}:{}'.format(index+1,stri),aux.group())
            return (True, '')
    return(False, None)

def verifyIntAttrib(index, line):
    if(line.find(':=')):
        if(re.search('(\d)+', line)):
            aux = line.split(':=')
            symbol_table[aux[0].strip(' ')] = 'line: {}, Lexeme: {} , token(integer, {})\n'.format(index+1, 'integer', aux[1].strip('\n'))
            return(True, '')
    return(False, None)

def verifyFloat(index, line):
    if(re.search('(\d)+.(\d)+', line)):
        if(line.find(':=')):
            symbol_table[line.split(':=')[0].strip(' ')] = 'line: {}, Lexeme: {} , token(real, {})\n'.format(index+1, 'real', line.split(':=')[1].strip('\n'))
            return(True, '')
    return(False, None)

def verifyId(index, line):
    if(re.search('[_a-zA-Z]\w*', line)):
        if(line.find(':=') > 0):
            aux = line.split(':=')
            if(aux[0].strip(' ') not in symbol_table):
                symbol_table[aux[0].strip(' ')] = 'line: {}, Lexeme: {} , token(id, {}), type: {}\n'.format(index+1,aux[0].strip(' '),aux[1].strip('\n'), 'ID')
                return(True, '')
        elif(line.find(':') > 0):
            aux = line.replace('Var ', '').split(':')
            if(aux[0].strip(' ') not in symbol_table.keys()):
                symbol_table[aux[0].strip(' ')] = 'line: {}, Lexeme: {} , token(id, {}), type: {}\n'.format(index+1,aux[0].strip(' '),'nil', aux[1].strip())
                return(True, line)
    return (False, None)

def verifyOther(index, line):
    line = line.split()
    for l in line:
        if(re.search('[_a-zA-Z]\w*', l)):
            aux = re.search('[_a-zA-Z]\w*', l)
            # print(aux.group())
            if(aux.group().upper() in kwords and aux.group() not in symbol_table.keys()):
                symbol_table[aux.group()+str(index)] = 'line: {}, Lexeme: {} , token(Keyword, {}), type: {}\n'.format(index+1,aux.group(),'', 'Keyword')
            elif(aux.group().upper() in functions and aux.group() not in symbol_table.keys()):
                symbol_table[aux.group()+str(index)] = 'line: {}, Lexeme: {} , token(Function, {}), type: {}\n'.format(index+1,aux.group(),'', 'Function')
            else:
                symbol_table[aux.group()] = 'line: {}, Lexeme: {} , token(ID, {}), type: {}\n'.format(index+1,aux.group(),'', 'ID')
def verifyStringAttrib(index, line):
    if(line.find("'") > 1):
        if(line.find(':=') > 0):
            aux = line.split(':=')
            symbol_table[aux[0].strip(' ')] = 'line: {}, Lexeme: {} , token(id, {}), type: {}\n'.format(index+1,aux[0].strip(' '),aux[1].strip('\n'), 'string')
            return(True, '')
    return(False, None)
with open('arquivo.txt','r') as file:
    lines = file.readlines()
    for index, line in enumerate(lines):

        line = removeComment(line)
        ver, li = verifyStringAttrib(index, line)
        if(ver):
            line = li

        ver, li = hasPrintString(index, line)
        if(ver):
            line = li

        lines[index] = line

    for line in lines:
        line = line.replace(';', ' ; ')
        line = line.replace(':', ' : ')
        line = line.replace(' : =', ' := ')
        line = line.replace(' > =', ' >= ')
        line = line.replace(' < =', ' <= ')
        line = line.replace(".", " . ")
        line = line.replace(' . .', ' .. ')
        line = line.replace(' . ', '.')
        line = line.replace(' < >', ' <> ')
        line = line.replace('(', ' ( ')
        line = line.replace("'", " ' ")
        line = line.replace(')', ' ) ').split()
        #adding lexeme to lexemes list
        lexemes.append(line)

    for index, line in enumerate(lexemes):
        #print(line)
        li = ''
        for l in line:
            li = li+' '+l

        line = verifyAttrib(index, li)
        lexemes[index] = line

with open('result.txt', 'w') as file:
    for symb in symbol_table:
        file.write(symb+' ----> '+symbol_table[symb])

print('terminou a primeira parte')
lexemes = []

with open('arquivo.txt','r') as file:
    text = file.readlines()

    for line in lines:
        line = line.replace(';', ' ; ')
        line = line.replace(':', ' : ')
        line = line.replace(' : =', ' := ')
        line = line.replace(' > =', ' >= ')
        line = line.replace(' < =', ' <= ')
        line = line.replace(".", " . ")
        line = line.replace(' . .', ' .. ')
        if(re.search('\d+ . \d+', line)):
            line = line.replace(re.search('\d+ . \d+', line).group(), '')
        line = line.replace(' < >', ' <> ')
        line = line.replace('(', ' ( ')
        line = line.replace("'", " ' ")
        line = line.replace(')', ' ) ').split()
        #adding lexeme to lexemes list
        lexemes.append(line)

    for index, lexeme in enumerate(lexemes):
        for lex in lexeme:
            try:
                if(lex+str(index) not in symbol_table.keys() and lex not in symbol_table.keys()):
                    lexemes2.append('line: {}, Lexeme: {} , token({}, {}), type: {}\n'.format(index+1, lex, tokens[lex], '', tokens[lex]))
            except:
                pass

with open('result.txt', 'w') as file:
    file.write('Symbol Table bellow:\n')
    for symbol in symbol_table:
        file.write('--->'+' '+symbol_table[symbol])
    file.write('Lexemes not in symbol table bellow:\n')
    for lexeme in lexemes2:
        file.write('--->'+' '+lexeme)

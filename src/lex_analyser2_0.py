#verify patterns with regular expression
import re
#keywords table
kwords = ['AND', 'ARRAY',
            'BOOLEAN', "BEGIN",
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
symbols = 1

def removeComment(line):
    line = re.sub('\(\*.*\*\)', '', line)
    return line

with open('arquivo.txt','r') as file:
    lines = file.readlines()

    for line in lines:
        line = removeComment(line)
        if re.search("'.*'", line):
            line = re.sub("'.*'", re.search("'.*'", line).group().replace(' ', '$'), line)
        line = line.replace(';', ' ; ')
        line = line.replace(':', ' : ')
        line = line.replace(' : =', ' := ')
        line = line.replace(' > =', ' >= ')
        line = line.replace(' < =', ' <= ')
        if(not re.search('\d+.\d+', line)):
            line = line.replace(".", " . ")
        line = line.replace(' . .', ' .. ')
        # line = line.replace(' . ', '.')
        line = line.replace(' < >', ' <> ')
        line = line.replace('(', ' ( ')
        line = line.replace(')', ' ) ').split()
        #adding lexeme to lexemes list
        lexemes.append(line)

    for index, lexeme in enumerate(lexemes):
        # print(lexeme)
        for lex in lexeme:
            if lex.find("'") != -1:
                if(lex.count("'")%2 != 0):
                    lexemes2.append('STRING ERROR IN LINE {}.\n'.format(index+1))
                    lex = ''
                else:
                    lexemes2.append('line: {}, Lexeme: {} , token( String, {} )\n'.format(index+1, lex.replace('$', ' '), lex.replace('$', ' ')))
            elif lex.upper() in kwords:
                lexemes2.append('line: {}, Lexeme: {} , token( Keyword , {} )\n'.format(index+1, lex, ''))
            elif lex.upper() in functions:
                lexemes2.append('line: {}, Lexeme: {} , token( Function, {} )\n'.format(index+1, lex, ''))
            elif lex in tokens.keys():
                lexemes2.append('line: {}, Lexeme: {} , token( {} , {} )\n'.format(index+1, lex, lex, tokens[lex]))
            elif re.search('[_a-zA-Z]\w*', lex):
                if lex not in symbol_table.keys():
                    symbol_table[lex] = ['line: {}, Lexeme: {} , token: {} , address: {} )\n'.format(index+1, lex, 'ID', symbols), symbols]
                    lexemes2.append('line: {}, Lexeme: {} , token( {} , {} )\n'.format(index+1, lex, 'ID', symbols))
                    symbols += 1
                else:
                    lexemes2.append('line: {}, Lexeme: {} , token( {} , {} )\n'.format(index+1, lex, 'ID', symbol_table[lex][1]))
            elif re.search('\d+.\d+', lex):
                lexemes2.append('line: {}, Lexeme: {} , token( {} , {} )\n'.format(index+1, lex, 'real', lex))
            elif re.search('\d+', lex):
                lexemes2.append('line: {}, Lexeme: {} , token( {} , {} )\n'.format(index+1, lex, 'integer', lex))
            else:
                print('LEXICAL ERROR, LINE {}\n'.format(index+1))

with open('result.txt', 'w') as file:
    file.write("LEXEMES BELLOW: \n")
    for lex in lexemes2:
         file.write('----->'+lex)

    file.write('SYMBOL_TABLE BELLOW: \n')
    for key in symbol_table:
        file.write('----->'+symbol_table[key][0])

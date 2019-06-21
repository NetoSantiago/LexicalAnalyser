#importing re to verify the identifies pattern
import re
#used somewhere to verify comments
isComment = False
#kwords = the language keywords
kwords = ['AND', 'ARRAY',
            'BEGIN', 'BOOLEAN',
            'CASE', 'CHAR,CONST',
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
            'THEN', 'TO', 'token',
            'UNTIL', 'VAR', 'WHILE', 'WITH']
#The language functions
functions = ['WRITELN', 'READLN']

#Other tokens..
tokens = {':=':'assign_op', '..':'dotdot', '.':'dot',
        ':':'colon', ';':'semicolon', ',':'comma',
        '[':'lb', ']':'rg', '(':'lp', ')':'rp',
        '=':'equal', '<=':'le', '>=':'ge','<>':'ne',
        '>':'gt', '<':'lt', '/':'divide', '-':'minus',
        '+':'plus', '*':'times','^':'simb_pointer','@':'ender' }

#here is the symbol table to store the ids values
symbol_table = {}
#used to store the lexemes
lexemes = []
#here we store the lexemes in their respectives lines

with open("arquivo.txt","r") as file:
    string = file.readlines()
    #separating possible tokens to use split in future.
    for line in string:
        line = line.replace(';', ' ; ')
        line = line.replace(':', ' : ')
        line = line.replace(' : =', ' := ')
        line = line.replace(' > =', ' >= ')
        line = line.replace(' < =', ' <= ')
        line = line.replace(' . .', ' .. ')
        line = line.replace(' < >', ' <> ')
        line = line.replace('(', ' ( ')
        line = line.replace("'", " ' ")
        line = line.replace(".", " . ")
        line = line.replace(')', ' ) ')
        line = line.replace('( *', '(*')
        line = line.replace('* )', '*)').split()
        #storing the lines of lexemes

        lexemes.append(line)

    for lexeme in lexemes:
        print(lexeme)

    with open("results.txt",'w') as res:
        #doing for to take each index line and the respective line.
        for index, line in enumerate(lexemes):
            #jump is just to verify how many tokens i'll need to jump because of comments.
            jump = 0
            #print(index)
            for lex in line:
                if(jump > 0):
                    jump -= 1
                    continue
                #print()
                if(lex == '(*'):
                    jump = 1
                    ind = line.index(lex)+1
                    try:
                        while(line[ind] and line[ind] != "*)"):
                            lex = lex+' '+line[ind]
                            ind += 1
                            jump += 1
                        lex = lex+' '+line[ind]
                        print(lex)
                        continue
                    except:
                        res.write("The ' character is missing. Lexical error line {}\n".format(str(lexemes.index(line)+1)))
                        continue

                if(lex.upper() in kwords):
                    res.write("line: {}, Lexeme: '{}'' , token(Keyword, )\n".format(str(index+1), lex))
                    continue
                    #< número da linha , lexema , padrão , token(nome_atributo,valor_associado) >
                elif(lex.upper() in functions):
                    res.write("line: {}, Lexeme: '{}'' , token(Function, )\n".format(str(index+1), lex))
                    continue

                elif(lex in tokens.keys()):
                    res.write("line: {}, Lexeme: '{}', Token('{}' , {})\n".format(str(index+1), lex, lex ,tokens[lex]))
                    continue

                elif(lex.find("'") >= 0):
                    jump = 1
                    ind = line.index(lex)+1
                    try:
                        while(line[ind] and line[ind] != "'"):
                            lex = lex+' '+line[ind]
                            ind += 1
                            jump += 1
                        lex = lex+' '+line[ind]
                    except:
                        res.write("The ' character is missing. Lexical error line {}\n".format(str(lexemes.index(line)+1)))
                        continue

                    res.write("line: {}, Lexeme: {} , token(String, {})\n".format(str(index+1), lex, lex))
                else:
                    if(re.match('[_a-zA-Z]\w', lex)):
                        #Here i need to ref symbol-table

                        ind = line.index(lex)+1
                        if(line[ind] == ':'):
                            symbol_table[lex] = [index, lex, None, line[ind+1]]
                            print(symbol_table[lex])
                            res.write("line: {}, Lexeme: '{}'' , token(id, {})\n".format(str(index+1), lex, symbol_table[lex][2]))
                            continue
                        if(line[ind] == ':='):
                            if(line[ind+1][0] == "'"):#VERIFY IF IT'S A STRING
                                symbol_table[lex] = [index, lex, line[ind+1], 'string'] #type(symbol_table[line[ind+1]][1])
                                print(symbol_table[lex])
                                res.write("line: {}, Lexeme: '{}'' , token(id, {})\n".format(str(index+1), lex, symbol_table[lex][2]))
                                continue

                            elif(line[ind+1] and re.match('(\d)+.(\d)+', line[ind+1])):
                                symbol_table[lex] = [index, lex, float(line[ind+1]), 'float']
                                print(symbol_table[lex])
                                res.write("line: {}, Lexeme: '{}'' , token(id, {})\n".format(str(index+1), lex, symbol_table[lex][2]))
                                continue

                            elif(line[ind+1] and re.match('(\d)+', line[ind+1])):
                                symbol_table[lex] = [index, lex, int(line[ind+1]), 'int']
                                print(symbol_table[lex])
                                res.write("line: {}, Lexeme: '{}'' , token(id, {})\n".format(str(index+1), lex, symbol_table[lex][2]))
                                continue

                            else:
                                value = symbol_table[ind+1]
                                symbol_table[lex] = [index, lex, symbol_table[line[ind+1]][1], type(symbol_table[lex][2])]
                                print(symbol_table[lex])
                                res.write("line: {}, Lexeme: '{}'' , token(id, {})\n".format(str(index+1), lex, symbol_table[lex][2]))
                                continue

                        res.write("line: {}, Lexeme: '{}'' , token(id, )\n".format(str(index+1), lex))
                    else:
                        res.write("error in line {} '{}'\n".format(str(index+1), lex))
                #print(("line: "+str(lexemes.index(line))+" Lemexe: "+lex))

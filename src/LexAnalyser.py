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
symbol_table = []
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
        line = line.replace(')', ' ) ').split()
        #storing the lines of lexemes
        lexemes.append(line)
    #print(lexemes)

    with open("results.txt",'w') as res:
        #doing for to take each index line and the respective line.
        for index, line in enumerate(lexemes):
            #jump is just to verify how many tokens i'll need to jump because of comments.
            jump = 0
            for lex in line:
                if(jump > 0):
                    jump -= 1
                    continue
                #print()
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
                        res.write("line: {}, Lexeme: '{}'' , token(id, )\n".format(str(index+1), lex))
                    else:
                        res.write("error in line {} '{}'\n".format(str(index+1), lex))
                #print(("line: "+str(lexemes.index(line))+" Lemexe: "+lex))

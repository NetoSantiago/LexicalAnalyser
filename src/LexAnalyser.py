import re

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
            'THEN', 'TO', 'TYPE',
            'UNTIL', 'VAR', 'WHILE', 'WITH']

tokens = {':=':'assign_op', '..':'dotdot', '.':'dot',
        ':':'colon', ';':'semicolon', ',':'comma',
        '[':'lb', ']':'rg', '(':'lp', ')':'rp',
        '=':'equal', '<=':'le', '>=':'ge','<>':'ne',
        '>':'gt', '<':'lt', '/':'divide', '-':'minus',
        '+':'plus', '*':'times','^':'simb_pointer','@':'ender' }

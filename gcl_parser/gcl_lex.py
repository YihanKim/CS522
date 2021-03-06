# CS522 프로젝트 #1
# 20130143 김이한

# Dijkstra의 Guarded Command Language를 parse tree로 변환하기
# Linux에서 작성, Python 3.5.2
# http://www.dabeaz.com/ply/ply.html
# PLY 사이트 가보면 엄청 자세한 사용법이 나와 있음
# lex 기본 골격을 가져와 작성함


# 문법

# Statement <S> ::= skip
#		| abort
#		| <V>[,<V>] := <E>[,<E>]
#		| <S> ; <S>[;<S>]
#		| if <E> -> <S> [| <E> -> <S>] fi
#		| do <E> -> <S> [| <E> -> <S>] od

# 동시 할당(a,b:=3,4)시 양 변의 수를 비교하는 것은 컴파일로 미룸
# 여기서 if, do는 조건문 E가 0이 아닐 때 그에 대응하는 S가 실행된다.

# Variable <V> is string

# Expression <E> ::= <integer>
#		| <V>
#               | !<E>
#		| <E> <BINOP> <E>
#		| (<E>)

# 정수 연산만 허용한다고 가정하자.
# 앞에서 정의된 variable로 expression을 대체할 수 있다.




# 사용한 라이브러리 : Python Lex-Yacc(ply)의 lex, yacc
# 설치 방법 : 리눅스에서 pip3 install ply

import ply.lex as lex
import ply.yacc as yacc


# 토큰 : 
tokens = [
   'NUMBER',
   'VARIABLE',
   'SEMICOLON',
   'ASSIGN',
   'ARROW',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'SPLIT',
   'COMMA',
   'AND',
   'OR',
   'NOT',
   'XOR',
   'LESS',
   'GREATER',
   'EQUAL',
   'NOTEQUAL',
   'GEQUAL',
   'LEQUAL',
]

# 변수 기능이 있으므로, 스트링을 포함하는 토큰은 별도 관리
reserved = {
	'if': 'IF',
	'fi': 'FI',
	'do': 'DO',
	'od': 'OD',
	'skip': 'SKIP',
	'abort': 'ABORT',
}

# 토큰에 예약어 추가
tokens = tokens + list(reserved.values());

t_ASSIGN = r':='
t_ARROW = r'->'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMICOLON = r';'
t_SPLIT = r'\|'
t_COMMA = r'\,'
t_AND   = r'&&'
t_OR    = r'\|\|'
t_NOT   = r'!'
t_XOR   = r'\^'
t_LESS  = r'<'
t_GREATER = r'>'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GEQUAL = r'>='
t_LEQUAL = r'<='

# 자연수 처리 
def t_NUMBER(t):
    r'[-+]?\d+'
    t.value = int(t.value)    
    return t

# 변수 처리 - 예약어 제외
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out

def main():
    print("Project 1-1. GCL lexer test")
    print("Guarded Command를 바탕으로 한 입력을 받아 토큰화 작업을 진행합니다.")
    print("종료하려면 입력 없이 Enter를 누르세요")
    while True:
        try:
            data = input("GCL_TOKENIZE > ")
        except KeyboardInterrupt:
            print()
            print('bye')
            break

        if not data:
            print("bye")
            break

        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input
            print(tok)

if __name__ == "__main__":
    main()

# CS522 프로젝트 #1
# 20130143 김이한

# 1. 개요
# Dijkstra의 Guarded Command Language를 parse tree로 변환하기
# Linux에서 작성, Python 3.5.2
# http://www.dabeaz.com/ply/ply.html
# PLY 사이트 가보면 엄청 자세한 사용법이 나와 있음
# lex 기본 골격을 가져와 작성함

# 2. 문법

# Statement <S> ::= skip
#				| abort
#				| <V>[,<V>] := <E>[,<E>]
#				| <S> ; <S>[;<S>]
#				| if <E> -> <S> [| <E> -> <S>] fi
#				| do <E> -> <S> [| <E> -> <S>] od

# 동시 할당(a,b:=3,4)시 양 변의 수를 비교하는 것은 컴파일로 미룸
# 여기서 if, do는 조건문 E가 0이 아닐 때 그에 대응하는 S가 실행된다.

# Variable <V> is string

# Expression <E> ::= <integer>
#					| <V>
#					| <E> + <E>
#					| <E> - <E>
#					| <E> * <E>
#					| <E> / <E>
#					| (<E>)

# 정수 연산만 허용한다고 가정하자.
# 앞에서 정의된 variable로 expression을 대체할 수 있다.


# 방법
# lex를 이용하여 토큰화
# yacc을 이용하여 파싱 트리를 형성


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
   'OR',
   'COMMA',
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
t_OR = r'\|'
t_COMMA = r'\,'

# 자연수 처리 
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# 변수 처리 - 예약어 제외
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

# Define a rule so we can track line numbers
#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)




# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
x,y,z,w := 3 > 4,6,7,8;
if 10<20-> 132;x> 2 ->skip fi;
do 1*y = 1 -> (3 > 5);(25 -> 8) < 11 + 3 od
'''
data = '''
a, b, x, y, u, v := A, B, 1, 0, 0, 1;
do b > 0 ->
q, r := a / b, a - (a / b);
a, b, x, y, u, v := b, r, u, v, x - q*u, y - q*v
od
'''

#data = "if 1 -> 3 fi"


if __name__ == "__main__":
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)


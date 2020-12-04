# TinyAda

#### A simple TinyAda syntax checker with Python  

Yonsei University (South Korea)  
Fall 2020  
CSI3103-01 Programming Language Structures  
Went public on Dec. 5, 2020  



### Developers
[Hajin Kim](https://github.com/hajin-kim)  
[H. J.](https://github.com/Ownfos)  
[S. L.](https://github.com/hunny7434)  



### 개발 환경
운영 체제: Windows 10, MacOS Catalina  
개발 언어: Python 3.7.3  
별도의 외부 모듈은 이용하지 않는다.  



### 실행 방법
1. Comand line shell(CMD, Terminal 등)을 실행해 working directory를 이 문서가 위치한 directory로 설정한다.
2. 다음 명령어를 실행한다.  
  `python main.py`
3. 입력 파일의 이름을 입력한다. 확장자까지 입력해야 한다. 파일이 working directory에 있지 않다면 파일의 경로를 포함시켜 입력해야 한다.



### 실행 결과
1. Syntax error가 있다면 발견된 error에 대한 message를 출력하고 종료된다. Error message가 여러 개 있을 경우 한 줄을 공백으로 두고 다음 error message를 이어서 출력한다.
2. Semantic error가 있다면 발견된 error에 대한 message를 출력하고 syntax 분석을 계속한다. 오류가 여러 개 있을 경우 다음 줄에 이어서 error message를 출력한다.
3. Print 함수를 만날 경우 파라미터로 넘긴 식의 계산 값을 출력한다. 만약 print가 중첩된 proc 선언문에 있더라도 결과 출력은 예외 없이 일어난다. 만약 식의 값이 계산 불가능하면(e.g. 값이 대입되지 않은 변수를 사용) None을 출력한다.



### 모듈 설명 및 핵심 알고리즘

#### [main.py](./main.py)
***프로젝트의 entry driver이다.*** 테스트에 사용하는 코드와 제출용 코드를 모두 작성하고 필요한 부분을 제외하고 주석 처리하는 방식으로 사용하였다.

#### [Chario.py](./Chario.py)
파일 이름을 생성자에서 받아 해당 파일에서 문자를 하나씩 읽으며 소문자로 변환한다. 전체적인 입출력을 담당하며 오류 메시지의 출력 또한 Chario 클래스의 멤버 함수를 사용해 처리한다.

#### [Const.py](./Const.py)
Token의 종류, Role의 종류 등 프로그램의 여러 곳에 사용되는 상수를 한 곳에 모은 파일이다. Magic number를 없애고 연관된 상수를 한 튜플로 묶어 제공하는 등의 기능을 한다(e.g. 비교 연산자들, 선언 키워드들).

#### [Parser.py](./Parser.py)
Scanner에서 제공하는 Token을 TinyAda의 문법에 맞게 syntax 및 semantics 분석을 수행한다. P1에서 syntax 구현을 마친 후 P2에서 P1의 구현체를 건드리지 않고 role analysis 및 print 함수 구현을 독립적으로 추가하는 방식을 택했다. 각 BNF expression에 해당하는 함수와 더불어 편의를 위한 accept, fatalError 등의 함수를 포함한다. 분석 도중 오류가 생길 경우 해당 줄의 토큰을 전부 버리고 다음 줄으로 넘어가 분석을 계속하므로 다른 줄에 있는 오류를 모두 검출할 수 있다.

#### [Scanner.py](./Scanner.py)
Chario에서 문자를 연속적으로 받아 TinyAda의 Token으로 변환한다. Token의 종류마다 변환 규칙이 달라서(e.g. integer는 숫자가 아닌 문자를 만날 때까지 읽음, 연산자는 최대 두 자리만 읽고 valid한지 판단) 총 네 개의 분류로 나눠서 함수를 구현하였다.

#### [SymbolEntry.py](./SymbolEntry.py)
각 identifier의 이름에 대응하는 role과 value를 저장한다.
Value는 print 함수의 구현을 위해 추가한 멤버 변수로, 상수의 선언이나 대입문을 만날 때 계산된 값으로 업데이트된다.

#### [SymbolTable.py](./SymbolTable.py)
SymbolEntry의 리스트의 스택을 관리한다. 새로운 Scope에 들어갈 때 스택에 빈 리스트를 추가하고, 해당 scope에서 선언된 모든 identifier를 그 리스트에 저장한다. 현재 상태에서 주어진 이름에 해당하는 SymbolEntry가 있는지 검색하거나 새 SymbolEntry를 추가할 수 있다. 만약 검색 또는 추가가 실패하면 오류 메시지를 출력한다.

#### [Token.py](./Token.py)
TinyAda에서 사용되는 Token의 type과 value(이름 또는 상수 값)를 저장한다.



### 오류 출력 형식

####Syntax error
만약 A라는 토큰이 와야 하는데 B라는 토큰이 왔다면, "E: expected [A] but [B] was detected"라는 문구가 먼저 출력된다. 에러가 발생한 줄은 더 이상 올바르게 해석할 수 없다고 가정하고 개행문자를 만날 때까지 토큰을 계속 스캔하며 버린다. 그렇게 discard된 토큰들은 "trailing tokens: \[A\] \[B\] \[C\] were discarded"라는 메시지로 확인할 수 있다. 바로 다음 줄에는 에러가 발생한 후 다음으로 오는 토큰을 어떻게 해석할지 알려주는 문장이 나온다. 예를 들어, 프로시저 선언 부분에서 is 토큰이 사라졌다면, 그 뒤에 오는 선언부를 계속 파싱하려고 한다는 것을 알려주기 위해 "continue parsing from declarative part of subprogram body"라는 문장을 출력한다.  
다음은 <u>프로시저의 이름을 지워버린 경우</u>의 출력 예시이다.  

1. identifier가 와야 할 자리에 is가 옴
2. is 부터 개행문자를 만날 때까지 모든 토큰을 버림
3. 프로시저의 선언부에서 파싱을 이어간다는 것을 차례로 출력한다.

오류가 여럿 발견되면 한 줄 공백을 간격으로 차례대로 출력된다.  

이상한 코드를 파싱하는 경우 expected token의 종류가 예상과 다를 수도 있는데, 이는 파싱을 시도할 때 특정한 토큰이 없는 경우 아예 다른 종류의 문장으로 해석하려 해서 발생하는 현상이다.  
예를 들어, assignment의 경우 identifier다음에 :=가 와야 하는데 여기서 :=를 >로 바꿔버리면 이 문장을 assignment가 아닌 비교 연산식으로 해석하려 해서 ":=가 오지 않았다"가 아닌 다른 오류가 뜨게 된다.  

위와 비슷한 사례로, 가장 파싱이 꼬이는 경우 중 하나는 반복문에서 end 키워드가 생략된 상황이다. 만약 이 키워드가 오지 않으면 sequence of statement에서 다음에 오는 모든 키워드를 계속 statement로 해석하려 하기 때문에 "end 토큰이 생략되었다"가 아닌 "문장으로 해석하는데 실패했다"라는 오류가 뜨게 되므로 이 점은 주의해야 한다.  

#### Semantic error
(1)role이 일치하지 않는 경우, (2)선언되지 않은 identifier를 사용한 경우, (3)identifier를 재정의한 경우, (4)procedure 선언 마지막 end 토큰 뒤에 procedure의 이름과 다른 identifier가 온 경우가 있다. 각 케이스의 출력 형식은 다음과 같다.  

1. `(오류 발생한 identifier) : expected (예상된 role) identifier, not (오류 발생한 identifier의 role)`
2. `undefined identifier [(오류 발생한 identifier)] was used`
3. `redefinition of already defined identifier [(오류 발생한 identifier)]`
4. `unexpected name [(오류 발생한 identifier)] was used after END keyword in procedure [(오류 발생한 proc 이름)]`

만약 procedure의 이름이 없어서 비교가 불가능 한 경우 (4) 대신 다음과 같은 메시지가 출력된다.  
`failed to check if [(오류 발생한 identifier)] is valid after procedure’s END keyword, because …`



### 주의 사항
Scanner는 교재에 적힌 EBNF에 등장하는 키워드들과 identifier, numeric literal, 그리고 개행 문자를 토큰으로 변환한다.
개행 문자에서 "\r"은 무시하고 오로지 "\n"만 newline으로 간주하며, 모든 공백은 무시한다.
identifier는 모두 첫 글자가 알파벳으로 시작한다고 가정했다. 예를 들어, \_ABC의 경우 \_가 먼저 unexpected symbol로 처리되고 뒤에 있는 ABC가 정상적인 identifier로 해석된다.
identifier를 구분하는 기준으로 연산자에 사용되는 기호들도 사용했으므로 A+B처럼 둘 사이에 공백이 없더라도 A, +, B 3개의 토큰으로 잘 인식한다.
연산자(및 기호)의 경우 +처럼 무조건 한 글자인 연산자들은 공백 없이 연속으로 등장했을 때 오류 없이 여러 개의 한 글자 연산자로 처리된다. 예를 들어, ++-:=:는 +, +, -, :=, : 총 5개의 연산자로 해석된다.  

Scanner는 토큰을 총 3개의 유형으로 구분해서 읽어들인다:

1. 알파벳으로 시작하는 alphabeticToken
2. 숫자로 시작하는 integerToken
3. 그 외의 연산자들

여기서 1과 2에서는 예상치 못한 토큰 오류가 발생하지 않는다. 1의 경우 is처럼 정해진 키워드가 아니면 무조건 identifier로 처리하기 때문이다. 하지만 3에서는 UET(UnExpected Token)를 token code로 갖는 결과가 리턴될 수 있으며, 무조건 한 글자씩 처리된다. 예를 들어, &&는 두 개의 unexpected token으로 처리된다. 이는 1과 2가 아닌 경우 유효한 토큰이 한 글자 연산자(e.g. +)와 두 글자 연산자(e.g. \*\*)밖에 없어서, 한 번에 최대 두 글자까지만 읽기 때문이다.  

예상치 못한 토큰을 만난 것 만으로는 exception을 raise하지 않는다. 만약 &처럼 존재해서는 안 되는 문자가 온전한 문장 사이에 혼자 있을 경우, 단순히 &가 스캔되었다는 문구만 출력되고 파싱에는 영향을 주지 않는다. 하지만 유효한 토큰이 와야 할 자리에 unexpected token이 오는 경우, 정상적인 방법으로 오류가 처리된다. 예를 들어, procedure & is 와 procedure null is는 모두 같은 방식으로 "expected \[identifier\] but ..."이라는 에러가 출력되며 다음 줄을 파싱하기 시작한다.  

Print 및 matrix는 predefined identifier로 인식한다. 그러므로 이 둘을 선언하지 않고 사용하더라도 undefined identifier 오류가 발생하지 않는다. 또한, print문은 TinyAda 코드 내부에 작성하여야 하며, 일반 procedure call statement와 동일하게 세미콜론으로 끝난다고 가정한다. 파싱 도중에 syntax, semantic 에러가 생겨도 print는 실행된다. 이때 에러로 인해 값이 assign되지 않아 실행된 print로 전달된 매개변수 값이 None 또는 존재하지 않을 경우, print의 결과로 None 또는 빈 줄이 출력될 수 있다.  


---

### 과제 수행 결과
P1은 if문을 제외하면 모두 통과했고, P2는 모든 경우에 대해 정상적으로 처리를 할 수 있었다. 결과적으로 보면 아주 성공적이라고 할 수 있다. 단순히 점수를 잘 받은 것을 넘어 프로젝트를 하며 쌓은 지식과 경험 또한 값진 결과라고 생각한다. 프로젝트를 진행하며 버전 관리 도구를 사용하는 방법을 익히며 협업해서 개발하는 경험을 쌓을 수 있었고, syntax analyzer를 구현하며 recursive descent parser의 구조와 작동 원리를 세부적으로 파악할 수 있었으며 이 방식의 한계를 느끼며 현대의 컴파일러들이 스택을 사용하는 다른 방법을 채택했는지 느낄 수 있었다. Role analyzer를 구현하는 과정에서는 symbol table로 scope를 관리하고 변수의 attribute를 검사하는 방법을 익혔고 print 함수를 만들 때는 EBNF를 수정해서 연산의 precedence와 associativity를 정할 수 있다는 것을 테스트하며 확인할 수 있었다.  
제안서에 작성한 프로젝트 수행 계획은 차질 없이 준수되었다. Syntax analyzer와 static semantic analyzer 모두 마감 기한 4일 이전에 프로토타입이 산출되었다. 이 덕분에 산출물 테스트 및 추가적인 의사 결정 기간에 여유를 둘 수 있었고, 각 최종 결과물들을 원활하게 제출할 수 있었다.



### 문제점 및 미흡한 부분
코딩으로 들어가기 전에 문제를 충분히 분석하지 않아서 설계 오류를 자주 겪었다. 예를 들어, P2를 해결할 때 SymbolTable에서 findSymbol함수를 호출하면 오류가 생겼을 때 무조건 메시지가 출력돼서 중복된 출력을 막기 위해 findSymbol의 호출을 하나로 제한하기 위한 조치를 많은 곳에서 취해야 했다. 만약 설계를 충분히 하고 구현했다면 findSymbol의 오류 출력을 다른 함수로 분리해서 이런 문제를 피할 수 있었을 것이다. 다음으로 어려움을 겪은 부분은 구현이 끝난 후 제대로 작동하는지 테스트하는 과정이었다. 문법의 수가 많고 그만큼 테스트 케이스도 많이 필요한데 이를 매번 수동으로 확인하다 보니 일부 문법의 검사를 생략하거나 올바른 오류 출력을 실수라고 생각해서 분석하느라 시간을 다소 낭비하는 일이 있었다. 실제로 P1에서는 if문에 해당하는 테스트 케이스를 확인하지 않아서 오류가 있다는 것을 발견하지 못했다. 만약 유닛 테스트를 작성하며 자동화된 검증을 했더라면 테스트 시간도 절약하고 실수도 줄일 수 있었을 것이다.



### 결론
6장과 7장에서 배운 내용을 활용해 직접 코드 분석기를 만드는 작업은 아주 흥미로웠다. 처음에는 이걸 과연 만들 수 있는 것인가 의심하기도 했고 실제로 구현 과정에서 많은 고민과 시행착오를 거쳤지만 결국엔 원하는 기능을 모두 완성해내는 것을 보며 자부심, 성취감 등을 느낀 것 같다. 비록 앞에서 언급했듯이 구현이 완벽하지도 않았고 오히려 후회되는 부분도 상당수 있었지만, 이번 경험을 통해 다른 프로젝트를 하게 되면 지금의 실수를 기억하고 보완해서 전보다 더 발전된 모습으로 나아갈 수 있으리라 생각한다.





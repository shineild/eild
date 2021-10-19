# PEBOOK.py 개발

```
이 프로그램은 저처럼 공부하는 학생분들이 책과 tool을 이용하여 공부하는 번거로움을
조금이라도 줄여보고자 만든 CLI환경의 프로그램입니다.
공부하면서 배운 내용을 정리하고 실습하는 겸 만들어 보았으며 저 또한 만들면서 많이 도움이 되었던 것 같습니다.
현재는 DOS, NT header 전반적인 내용들, IAT, EAT, Section 정보 정도만 확인 할 수 있고 도움말이 적혀있으며
추후에 심화 분석과 도움말을 추가할 예정입니다.
기존 뷰어들과의 차이점은 상세한 정보를 보여주고 있지는 않지만 PE를 처음 배우시는 분들이 접근하기 쉬운 개념들을 보여주고 있으며
궁금한 개념들을 바로 확인 할 수 있게 도움말을 넣어 두었습니다.
그래서 자신이 현재 보고 있는 내용이 어떠한 의미를 뜻하는지 바로바로 확인 할 수 있게 만들어서
책과 viewer를 합쳐둔 느낌의 프로그램입니다.
그래서 학습을 위한 책과 같은 역할이 되었으면 하는 바램으로
pebook 이라는 이름을 지었습니다.
 
현재는 x84버전만 지원하고 있으며 64비트의 버전을 확인하려고 하면 에러가 뜰 것임으로 주의하시기 바랍니다.
그리고 패킹된 파일은 분석을 지원하고 있지 않으므로 해당 파일의 pe를 분석한다는 초점보다는
예시 파일을 이용하여 pe 포맷을 공부한다는 느낌으로 만들었습니다
```

## 실행 화면

![https://k.kakaocdn.net/dn/SwtPi/btqDHrUVSuM/3BdCY1ia3YYpJzBidjRQLK/img.png](https://k.kakaocdn.net/dn/SwtPi/btqDHrUVSuM/3BdCY1ia3YYpJzBidjRQLK/img.png)

파일 경로를 입력을 통해 받아낸 후 NT Header → File Header 정보를 출력한 화면입니다.

![https://k.kakaocdn.net/dn/Es9Xj/btqDIocpmVB/SNFT27Q59o1PpkbgPA9k00/img.png](https://k.kakaocdn.net/dn/Es9Xj/btqDIocpmVB/SNFT27Q59o1PpkbgPA9k00/img.png)

File Header 정보 출력 후 "도움말 - File header"로 들어온 화면입니다.



## 블로그에 적은 개발 과정

[나만의 PE 분석툴 제작기(1) - 목표 설정](https://shineild-security.tistory.com/37?category=1042860)

[나만의 PE 분석툴 제작기(2) - PyQt5 명령어 모음](https://shineild-security.tistory.com/44?category=1042860)

처음에는 목표를 설정할 때 GUI로 개발을 하려 했습니다.

하지만 PyQt5를 처음 사용하다 보니 개발이 어려웠고 조금 주춤하게 되었습니다.

그렇게 잠시 GUI 개발은 미루게 되었고 PE 공부를 먼저 하는 것으로 진행 방향을 바꾸었습니다.

['Knowledge/Reversing' 카테고리의 글 목록](https://shineild-security.tistory.com/category/Knowledge/Reversing)

리버싱 핵심원리 책을 참고로 공부하며 실습한 내용을 블로그에 정리하고 그 자료를 토대로 CLI 버전의 프로그램을 우선 만들어 보자는 생각에 다시 개발을 시작하였습니다.

GUI 개발 실력이 부족하다는 걸 깨달은 저는 이번엔 CLI로 개발했습니다.

그렇게 4월 10일에 개발을 완성하였습니다.

[나만의 PE 분석툴 제작기(3) - CLI 환경 Tool 제작 완성 후기](https://shineild-security.tistory.com/118?category=1042860)

[PE 구조를 공부하는 학생들을 위해 만든 pebook.exe](https://shineild-security.tistory.com/121?category=1042860)

# PEBOOK.py 개발

**실행 화면**

![https://k.kakaocdn.net/dn/SwtPi/btqDHrUVSuM/3BdCY1ia3YYpJzBidjRQLK/img.png](https://k.kakaocdn.net/dn/SwtPi/btqDHrUVSuM/3BdCY1ia3YYpJzBidjRQLK/img.png)

파일 경로를 입력을 통해 받아낸 후 NT Header → File Header 정보를 출력한 화면입니다.

![https://k.kakaocdn.net/dn/Es9Xj/btqDIocpmVB/SNFT27Q59o1PpkbgPA9k00/img.png](https://k.kakaocdn.net/dn/Es9Xj/btqDIocpmVB/SNFT27Q59o1PpkbgPA9k00/img.png)

File Header 정보 출력 후 "도움말 - File header"로 들어온 화면입니다.



**블로그에 적은 개발 과정**

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

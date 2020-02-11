# BookTable

## 실행방법
`BookTable` 폴더에 들어가 `display.py`를 실행시킨다. 

### `PyCharm`을 사용할 경우 
별다른 수정 없이 `display.py`를 실행하면 된다.

### `python` 명령어를 사용할 경우
`display.py` 맨 앞부분에 다음 코드를 추가한다.
```
import sys
sys.path.extend(["C:\\Users\\...\\DJIVF", "C:/Users/.../DJIVF"])
```
위의 경로는 DJIVF 폴더가 위치한 경로이다. 이제
`python display.py` 명령어를 이용해 프로그램을 실행시킬 수 있다.

## 실행파일 만들기
pyinstaller를 이용하여 exe 파일을 만들 때 명령어
```
pyinstaller --onefile --noconsole --hidden-import=sqlite3 --hidden-import=pandas display.py
```
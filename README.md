# SSF
SSF의 서버 코드</br>

## 개발환경
### 파이썬 3.8
  Flask</br>
  Pandas</br>
  Selenium
### 라즈베리파이 3b+
  라즈비안 Lite OS

## 파일 설명
### app.py
app.py는 각 api에 맞추어 기능 개발 </br>
api 목록: https://www.notion.so/582aa49a0aaa439495d3473aa18bde4b?v=c8c71ba71abf497d8055d87545c23e16
</br>
### Database.py
데이터베이스의 초기설정 담당</br>
all_data, all_data_Exist, all_data_Like, Person, Person_Like, Comment의 테이블 생성 및 데이터 세팅 담당
</br>
### Final_youth_selenium.py
데이터 크롤링 담당</br>
웹페이지에서 제목, 지원금 유형, 나이, 학력, 지역, 내용, 링크, 주체기관 등을 크롤링해온다.

import pymysql
import time
from datetime import datetime

login = 0
login_id = 0
status = 0

#=============================================================================
#============================함수 정의=========================================

def check():
    while True:
        exit = input("완료 시 0을 입력해주세요 : ")
        if exit == '0':
            print("============이전화면으로 돌아갑니다.============")
            time.sleep(1.0)
            break

def log_in(usrId): # 로그인 기능
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "select count(회원ID) from member where 회원ID = %s"
    curs.execute(sql, (usrId))
    rows = curs.fetchall()
    print(rows)
    if rows[0][0] == 1:
        print("반갑습니다. %s님" % usrId)
    else:
        print("등록되지 않은 회원ID입니다")
    
    conn.close()

def sign_up(enterID,enterName,enterCall,enterAge): # 회원가입 기능
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = """insert into member(회원ID, 이름, 연락처, 나이) values (%s, %s, %s, %s)"""
    curs.execute(sql, (enterID,enterName,enterCall,enterAge))
    conn.commit()
    conn.close()
    print("회원가입이 완료되었습니다.")

def book_list(): # 도서 목록 출력
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "select * from book"
    curs.execute(sql)
    rows = curs.fetchall()
    for i in rows:
        print(i)
    conn.close()
    check()

def book_insert(isrtISBN, isrtBook, isrtWriter, isrtPub, isrtGenre, isrtDate): # 도서 추가 기능
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = """insert into book(ISBN, 도서명, 저자, 출판사, 장르, 출간일자) values (%s, %s, %s, %s, %s, %s)"""
    curs.execute(sql, (isrtISBN, isrtBook, isrtWriter, isrtPub, isrtGenre, isrtDate))
    conn.commit()
    conn.close()
    print("도서가 추가되었습니다")
    check()

def book_search(searchBook): # 도서 검색
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "select * from book where 도서명 like %s"
    curs.execute(sql, ('%'+searchBook+'%'))
    rows = curs.fetchall()
    for i in rows:
        print(i)
    conn.close()
    check()

def book_delete(delBook):
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "delete from book where ISBN = %s"
    curs.execute(sql, (delBook))
    conn.commit()
    conn.close()
    print("삭제되었습니다.")
    check()
    
def member_list(): # 회원 목록 출력
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "select * from member"
    curs.execute(sql)
    rows = curs.fetchall()
    for i in rows:
        print(i)
    conn.close()

def member_class_update(targetID, chGrade):
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "update member set 등급 = %s where 회원ID = %s"
    curs.execute(sql, (chGrade, targetID))
    conn.commit()
    conn.close()
    print("등급이 변경되었습니다.")
    check()

def book_lend(lendBook):
    status = 0
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "select 도서번호 from lend"                                                                                                            

    curs.execute(sql)
    rows = curs.fetchall()
    lendList = list(rows)
    for i in range(0, len(lendList)):
        if lendBook in lendList[i]:
            status = 1
    if status == 1:
        print("이미 대여중인 도서입니다.")
        conn.close()
        check()
    else:
        sql = """insert into lend(도서번호, 대여자ID) values(%s, %s)"""
        curs.execute(sql, (lendBook, login_id))
        conn.commit()
        conn.close()
        print("대여가 완료되었습니다. 대여기간은 일주일 입니다.")
        check()
    status = 0

def book_lend_delete(returnBook):
    status = 0
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = "select 도서번호, 대여자ID from lend where 도서번호 = %s and 대여자ID = %s"
    curs.execute(sql, (returnBook, login_id))
    rows = curs.fetchall()
    rowsList = list(rows)
    for i in range(0, len(rowsList)):
        if returnBook in rowsList[i] and login_id in rowsList[i]:
            status = 1
    if status == 1:
        sql = "delete from lend where 도서번호 = %s"
        curs.execute(sql, (returnBook))
        conn.commit()
        conn.close()
        print("반납 되었습니다.")
        check()
    else:
        print("%s님이 대여하신 책이 아닙니다." % login_id)
        conn.close()
        check()
    status = 0

def book_lend_overdue(delayBook):
    conn = pymysql.connect(host="127.0.0.1", user="min", password="1234", db="book_db", charset="utf8")
    curs = conn.cursor()
    sql = """select ISBN, 도서명, 대여일, 반납예정일, 회원ID, 이름, 등급, 연락처 
    from book inner join lend
    on book.ISBN = lend.도서번호 inner join member on lend.대여자ID = member.회원ID
    where 반납예정일 < %s"""
    curs.execute(sql, (delayBook))
    rows = curs.fetchall()
    for i in rows:
        print(i)
    conn.close()
    check()

#=============================================================================
#====================로그인창=================================================

while True:
    if login != 1:
        print("1. 로그인")
        print("2. 회원가입")
        print("3. 프로그램 종료")
        time.sleep(0.5)
        logNum = input("번호를 입력해주세요 : ")
        login = 1

    if logNum == '1': # 로그인
        print("============로그인을 진행합니다.============")
        time.sleep(1.0)
        usrId =  input("아이디를 입력해주세요 : ")
        a = log_in(usrId)
        login_id = usrId
        

    if logNum == '2': # 회원가입
        print("============회원가입을 진행합니다.============")
        time.sleep(1.0)
        enterID = input("아이디를 입력해주세요 : ")
        enterName = input("이름을 입력해주세요 : ")
        enterCall = input("연락처를 입력해주세요 : ")
        enterAge = input("나이를 입력해주세요 : ")

        sign_up(enterID,enterName,enterCall,enterAge)
    if logNum == '3': # 프로그램 종료
        print("============시스템을 종료합니다.============")
        time.sleep(1.0)
        break

#=============================================================================
#==========================사용자 기능=========================================

    if login == 1: # 사용자 기능
        while True:
            print("1. 도서 목록")
            print("2. 도서 검색")
            print("3. 도서 대여")
            print("4. 도서 반납")
            print("5. 관리자 기능")
            print("6. 되돌아가기")
            time.sleep(0.5)
            option = input("번호를 선택해 주세요 : ")

            if option == '1' : # 도서 목록 출력
                book_list()

            elif option== '2': # 도서 검색
                print("============<도서 검색>============")
                time.sleep(1.0)
                searchBook = input("검색할 도서명을 입력하세요 : ")
                book_search(searchBook)


            elif option== '3': # 도서 대여
                print("============<도서 대여>============")
                time.sleep(1.0)
                lendBook = input("대여할 책의 ISBN을 입력해주세요 : ")
                book_lend(lendBook)

            elif option== '4': # 도서 반납
                print("============<도서 반납>============")
                time.sleep(1.0)
                returnBook = input("반납할 책의 ISBN을 입력해주세요 : ")
                book_lend_delete(returnBook)

#=============================================================================
#============================관리자 기능=======================================

            elif option== '5': # 관리자 기능
                manager_pw = input("관리자 비밀번호 입력 : ")
                if manager_pw == "12345":
                    print("============관리자 기능으로 전환됩니다.============")
                    time.sleep(1.0)
                    while True:
                        print("1. 도서 추가")
                        print("2. 도서 삭제")
                        print("3. 회원정보 수정")
                        print("4. 도서 연체 정보 ")
                        print("5. 돌아가기")
                        time.sleep(0.5)
                        managerOption = input("번호를 선택해 주세요 : ")
                        if managerOption =='1': # 도서 추가
                            print("============<도서 추가>============")
                            time.sleep(1.0)
                            isrtISBN = input("ISBN 입력 : ")
                            isrtBook = input("도서명 : ")
                            isrtWriter = input("저자명 : ")
                            isrtPub = input("출판사명 : ")
                            isrtGenre = input("장르 : ")
                            isrtDate = input("출간일자 : ")

                            book_insert(isrtISBN, isrtBook, isrtWriter, isrtPub, isrtGenre, isrtDate)

                        if managerOption =='2': # 도서 삭제
                            print("============<도서 삭제>============")
                            time.sleep(1.0)
                            delBook = input("삭제할 도서의 ISBN을 입력하세요 : ")
                            book_delete(delBook)

                        if managerOption =='3': # 회원정보 수정 (등급)
                            print("============<회원정보수정>============")
                            time.sleep(1.0)
                            member_list()
                            targetID = input("등급을 변경할 회원의 ID를 입력하세요 : ")
                            chGrade = input("변경할 등급을 입력해주세요 : ")
                            member_class_update(targetID, chGrade)

                        if managerOption =='4':
                            print("============<도서연체정보>============")
                            time.sleep(1.0)
                            delayBook = datetime.today().strftime('%Y-%m-%d')
                            book_lend_overdue(delayBook)

                        if managerOption =='5': # 되돌아가기
                            print("============관리자기능을 종료합니다.============")
                            time.sleep(1.0)
                            break
                else:
                    print("접속이 불가능합니다.")
                    time.sleep(0.5)
                
            elif option== '6': # 되돌아가기
                print("============첫 화면으로 돌아갑니다.============")
                time.sleep(1.0)
                login = 0
                break
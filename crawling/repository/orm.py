from sqlalchemy import Column, Integer, Index, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, INTEGER
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

"""
ORM 모델들이 정의되어 있습니다.
이들의 주요 공통 특징은 다음과 같습니다.
1. 객체를 그대로 출력해도 의미있는 정보를 출력합니다. (repr 함수가 재정의되어있음)
2. 객체를 반복문에 넣으면 해당 객체의 필드를 순서대로 출력합니다. (iter 함수가 재정의되어있음)
"""

class User(Base):
    """
    User 테이블
    name (str): 이름
    corrects (int): 맞은 문제 수
    submissions (int): 제출 수
    solution (int): 마지막 제출 번호
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False, unique=True)
    corrects = Column(Integer, nullable=False)
    submissions = Column(Integer, nullable=False)
    solution = Column(INTEGER(unsigned=True), nullable=False)

    # __table_args__ = (
    #     Index('name', 'name', unique=True),
    # )

    def __repr__(self):
        return f'<User(name={self.name}, corrects={self.corrects}, submissions={self.submissions}, solution={self.solution})>'

    def __iter__(self):
        yield self.name; yield self.corrects; yield self.submissions; yield self.solution

class Member(Base):
    """
    Member 테이블 (하루 하나에 참여하는 User)
    name (str): 이름
    bias (int): 바이어스
    """
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False, unique=True)
    bias = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Member(name={self.name}, bias={self.bias})>'

    def __iter__(self):
        yield self.name; yield self.bias

class Problem(Base):
    """
    Problem 테이블
    name (str): 푼 사람 이름 (외래키 user.name)
    problem (int): 문제 번호
    time (datetime): 푼 시간
    level (int): 푼 사람의 레이팅과 문제 등급의 차이
    repeatation (int): 같은 문제 반복 횟수
    """
    __tablename__ = 'problem'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(50), ForeignKey('user.name', name='FK_problem_user'), nullable=False)
    problem = Column(Integer, nullable=False)
    time = Column(DATETIME, nullable=False)
    level = Column(Integer, nullable=False)
    repeatation = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Problem(name={self.name}, problem={self.problem}, time={self.time}, level={self.level}, repeatation={self.repeatation})>'

    def __iter__(self):
        yield self.name; yield self.problem; yield self.time; yield self.level; yield self.repeatation

class Event(Base):
    """
    Event 테이블
    description (str): 이벤트 이름
    start_time (datetime): 시작 시간
    end_time (datetime): 종료 시간
    problem_id (int): 문제 번호
    """
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description = Column(VARCHAR(50), nullable=False)
    start_time = Column(DATETIME, nullable=False)
    end_time = Column(DATETIME, nullable=False)
    problem_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Event(description={self.description}, start_time={self.start_time}, end_time={self.end_time}, problem_id={self.problem_id})>'

    def __iter__(self):
        yield self.description; yield self.start_time; yield self.end_time; yield self.problem_id
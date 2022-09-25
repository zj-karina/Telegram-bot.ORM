
from sqlalchemy import create_engine, Integer, Text, Enum
from sqlalchemy import (Column, String, ForeignKey)
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql+mysqldb://root@127.0.0.1:3306/new_university')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Consultant_teacher(Base):
    __tablename__ = "consultant_teacher"

    id_consultant_teacher = Column(Integer, primary_key=True)
    Full_name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    institute = Column(String(255), nullable=False)

class Enrollee(Base):
    __tablename__ = 'enrollee'

    id_enrollee = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    sum_exam_points = Column(Integer, nullable=False)
    sum_IA_points = Column(Integer, nullable=False)
    passport_numbers = Column(String(10), nullable=False)
    certificate_numbers = Column(String(14), nullable=False)
    direction = Column(Integer, nullable=False)
    photos = Column(Enum('да', 'нет'), nullable=False)
    medical_certificate = Column(Enum('да', 'нет'), nullable=False)
    original_certificate = Column(Enum('да', 'нет'), nullable=False)
    passes = Column(Enum('да', 'нет'), nullable=False)
    consultant_teacher_id_consultant_teacher = Column(Integer, ForeignKey('consultant_teacher.id_consultant_teacher'), nullable=False)

class Admission_officer(Base):
    __tablename__ = 'admission_officer'

    id_admission_officer = Column(Integer, primary_key=True)
    employment = Column(Enum('да', 'нет'), nullable=False)
    signature = Column(Integer, nullable=False)

class Filling_out_an_application(Base):
    __tablename__ = 'filling_out_an_application'

    id_application = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    erollee_signature = Column(Integer, nullable=False)
    admission_officer_id_admission_officer = Column(Integer, ForeignKey('admission_officer.id_admission_officer'),
                                                      nullable=False)
    enrollee_id_enrollee = Column(Integer, ForeignKey('enrollee.id_enrollee'), nullable=False)

class Contest(Base):
    __tablename__ = 'contest'

    direction_number = Column(Integer, primary_key=True)
    budget_number = Column(Integer, nullable=False)
    enrollee_count = Column(Integer, nullable=False)
    passing_score = Column(Integer, nullable=False)
    filling_out_an_application_id_application = Column(Integer, ForeignKey('filling_out_an_application.id_application'), nullable=False)


Base.metadata.create_all(engine)

teacher1 = Consultant_teacher(Full_name='Иван Иванович Кузьмин', department='МОСИТ', institute='ИТ')
enrollee1 = Enrollee(full_name='Романова Карина Витальевна', sum_exam_points=234, sum_IA_points=4, passport_numbers='1749324592',
                     certificate_numbers='46295419432134', direction=30301, photos='да', medical_certificate='нет',
                     original_certificate='нет', passes='да', consultant_teacher_id_consultant_teacher=1)
admission_officer1 = Admission_officer(employment='нет', signature=11111)
filling_out_an_application1 = Filling_out_an_application(text='прошу дать мне возможность поучавствовать в конкурсе на бюджетную основу обучения',
                                                         erollee_signature=26473,admission_officer_id_admission_officer=1, enrollee_id_enrollee=1)
contest1 = Contest(direction_number=30301, budget_number=10, enrollee_count=0, passing_score=0, filling_out_an_application_id_application=1)


session.add_all([teacher1, enrollee1, admission_officer1])

contests = session.query(Contest)
for contest in contests:
    print(contest.direction_number)
session.commit()


#print(Consultant_teacher.__table__.columns.keys())
#query = 'select * from consultant_teacher'
#print(engine.execute(query).keys())
import telebot  # импорт pyTelegramBotAPI
from telebot import types
import random
import xlrd  # библиотка чтения экселевских файлов
import numpy as np

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
    consultant_teacher_id_consultant_teacher = Column(Integer, ForeignKey('consultant_teacher.id_consultant_teacher'),
                                                      nullable=False)


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


Base.metadata.create_all(engine)


def view_CT(Consultant_teacher):
    teachers = session.query(Consultant_teacher)
    ls = []
    for teacher in teachers:
        ls.append(teacher.id_consultant_teacher)
        ls.append(teacher.Full_name)
        ls.append(teacher.department)
        ls.append(teacher.institute)
    n = int(len(ls) / 4)
    ls = np.array(ls)
    ls = np.reshape(ls, (n, 4))
    ls = str(ls)
    return ls


def view_CT_orderby(Consultant_teacher):
    teachers = session.query(Consultant_teacher).order_by(Consultant_teacher.Full_name)
    ls = []
    for teacher in teachers:
        ls.append(teacher.id_consultant_teacher)
        ls.append(teacher.Full_name)
        ls.append(teacher.department)
        ls.append(teacher.institute)
    n = int(len(ls) / 4)
    ls = np.array(ls)
    ls = np.reshape(ls, (n, 4))
    ls = str(ls)
    return ls


def view_E(Enrollee):
    enrollees = session.query(Enrollee)
    ls = []
    for enrollee in enrollees:
        ls.append(enrollee.id_enrollee)
        ls.append(enrollee.full_name)
        ls.append(enrollee.sum_exam_points)
        ls.append(enrollee.sum_IA_points)
        ls.append(enrollee.passport_numbers)
        ls.append(enrollee.certificate_numbers)
        ls.append(enrollee.direction)
        ls.append(enrollee.photos)
        ls.append(enrollee.medical_certificate)
        ls.append(enrollee.original_certificate)
        ls.append(enrollee.passes)
    n = int(len(ls) / 11)
    ls = np.array(ls)
    ls = np.reshape(ls, (n, 11))
    ls = str(ls)
    return ls


def view_AO(Admission_officer):
    officers = session.query(Admission_officer)
    ls = []
    for officer in officers:
        ls.append(officer.id_admission_officer)
        ls.append(officer.employment)
        ls.append(officer.signature)
    n = int(len(ls) / 3)
    ls = np.array(ls)
    ls = np.reshape(ls, (n, 3))
    ls = str(ls)
    return ls


def view_F(Filling_out_an_application):
    applics = session.query(Filling_out_an_application)
    ls = []
    for applic in applics:
        ls.append(applic.id_application)
        ls.append(applic.text)
        ls.append(applic.erollee_signature)
    n = int(len(ls) / 3)
    ls = np.array(ls)
    ls = np.reshape(ls, (n, 3))
    ls = str(ls)
    return ls


def view_C(Contest):
    contests = session.query(Contest)
    ls = []
    for contest in contests:
        ls.append(contest.direction_number)
        ls.append(contest.budget_number)
        ls.append(contest.enrollee_count)
        ls.append(contest.passing_score)
    n = int(len(ls) / 4)
    ls = np.array(ls)
    ls = np.reshape(ls, (n, 4))
    ls = str(ls)
    return ls


def ins_CT(Consultant_teacher, Full_name, department, institute):
    teacher1 = Consultant_teacher(Full_name=Full_name, department=department, institute=institute)
    session.add_all([teacher1])


bot = telebot.TeleBot("5276778256:AAG247b8YEHMdJpdzasFIJmfHhcH-TRLWi4")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # клавиатура
    markup = types.ReplyKeyboardMarkup(True)  # меняем клавиатуру, подгоняя под размеры
    but1 = types.KeyboardButton('посмотреть, что в таблицах')
    but2 = types.KeyboardButton('вставить значение')
    markup.add(but1, but2)

    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}\n"
                          "Сегодня я буду помогать тебе управлять базой данных. Что бы ты хотел сделать?"
                     .format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def level1(message):
    if message.text == 'посмотреть, что в таблицах':
        markup = types.ReplyKeyboardMarkup(True)
        but1 = types.KeyboardButton('посмотреть таблицу')
        but2 = types.KeyboardButton('посмотреть таблицу с упорядоченным столбцом по именам')
        markup.add(but1, but2)

        bot.send_message(message.chat.id,
                         text="Выбери один из вариантов того, что будешь смотреть"
                         , reply_markup=markup)

    elif message.text == 'посмотреть таблицу':
        markup = types.ReplyKeyboardMarkup(True)
        but1 = types.KeyboardButton('Консультант-преподаватель')
        but2 = types.KeyboardButton('Абитуриент')
        but3 = types.KeyboardButton('Сотрудник приемной комиссии')
        but4 = types.KeyboardButton('Заявление')
        markup.add(but1, but2, but3, but4)

        bot.send_message(message.chat.id,
                         text="Посмотреть таблицу под названием"
                         , reply_markup=markup)

    elif message.text == 'Консультант-преподаватель':
        bot.send_message(message.chat.id, view_CT(Consultant_teacher))

    elif message.text == 'Абитуриент':
        bot.send_message(message.chat.id, view_E(Enrollee))

    elif message.text == 'Сотрудник приемной комиссии':
        bot.send_message(message.chat.id, view_AO(Admission_officer))

    elif message.text == 'Заявление':
        bot.send_message(message.chat.id, view_F(Filling_out_an_application))

    elif message.text == 'посмотреть таблицу с упорядоченным столбцом по именам':
        bot.send_message(message.chat.id, view_CT_orderby(Consultant_teacher))

    elif message.text == 'вставить значение':
        bot.send_message(message.from_user.id, "Введи имя преподавателя")
        bot.register_next_step_handler(message, get_full_name)


def get_full_name(message):
    global Full_name
    Full_name = message.text
    bot.send_message(message.from_user.id, "Введи кафедру")
    bot.register_next_step_handler(message, get_department)


def get_department(message):
    global department
    department = message.text
    bot.send_message(message.from_user.id, "Введи институт")
    bot.register_next_step_handler(message, get_institute)


def get_institute(message):
    global institute
    institute = message.text
    ins_CT(Consultant_teacher, Full_name, department, institute)


session.commit()
bot.polling(none_stop=True)

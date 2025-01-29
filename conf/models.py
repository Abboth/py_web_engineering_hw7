from sqlalchemy import Integer, String, ForeignKey, Date, Column
from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Teachers(Base):
    __tablename__ = "teacher"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)

    subject = relationship("Subjects", secondary="teacher_subject", back_populates="teacher")
    grades = relationship("GradesBook", back_populates="teacher")

    def __repr__(self):
        return f"\nTeacher name - {self.name}, id - {self.id} teaching subjects {self.subject}"

    @hybrid_property
    def average_grade(self):
        pass


class Students(Base):
    __tablename__ = "student"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    group_id: Mapped[int] = Column(Integer, ForeignKey("group.id"), nullable=False)

    subject = relationship("Subjects", secondary="student_subject", back_populates="student")
    grades = relationship("GradesBook", back_populates="student")
    group = relationship("Groups", back_populates="students")

    def __repr__(self):
        return f"\nStudent name - {self.name}, id - {self.id} member of group: {self.group_id}"


class Subjects(Base):
    __tablename__ = "subject"
    id: Mapped[int] = Column(Integer, primary_key=True)
    subject: Mapped[str] = Column(String(60), nullable=False)

    teacher = relationship("Teachers", secondary="teacher_subject", back_populates="subject")
    student = relationship("Students", secondary="student_subject", back_populates="subject")
    grades = relationship("GradesBook", back_populates="subject")

    def __repr__(self):
        return f"\n{self.subject} id - {self.id}"


class TeacherSubjects(Base):
    __tablename__ = "teacher_subject"
    id: Mapped[int] = Column(Integer, primary_key=True)
    teacher_id: Mapped[int] = Column(Integer, ForeignKey("teacher.id", ondelete="CASCADE"))
    subject_id: Mapped[int] = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"))



class StudentSubjects(Base):
    __tablename__ = "student_subject"
    id: Mapped[int] = Column(Integer, primary_key=True)
    student_id: Mapped[int] = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"))
    subject_id: Mapped[int] = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"))


class GradesBook(Base):
    __tablename__ = "grades_book"
    id: Mapped[int] = Column(Integer, primary_key=True)
    date: Mapped[Date] = Column(Date)
    subject_id: Mapped[int] = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"))
    student_id: Mapped[int] = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"))
    grade: Mapped[int] = Column(Integer)
    teacher_id: Mapped[int] = Column(Integer, ForeignKey("teacher.id", ondelete="CASCADE"))

    student = relationship("Students", back_populates="grades")
    subject = relationship("Subjects", back_populates="grades")
    teacher = relationship("Teachers", back_populates="grades")


class Groups(Base):
    __tablename__ = "group"
    id: Mapped[int] = Column(Integer, primary_key=True)
    group_name: Mapped[str] = Column(String)

    students = relationship("Students", back_populates="group")

    def __repr__(self):
        return f"\nGroups name {self.group_name} id {self.id}"

from sqlalchemy import Integer, String, ForeignKey, Date, Column
from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Teachers(Base):
    __tablename__ = "teacher"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)

    subject = relationship("Subjects", secondary="teacher_subject", back_populates="teacher")
    grades = relationship("GradesBook", back_populates="teacher")

    def __repr__(self):
        return f"\nTeacher name - {self.name}, id - {self.id} teaching subjects {self.subject}"


class Students(Base):
    __tablename__ = "student"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    group_id: Mapped[int] = Column(Integer, ForeignKey("group.id"), nullable=False)

    subject = relationship("Subjects", secondary="student_subject",
                           back_populates="student", passive_deletes=True)
    grades = relationship("GradesBook", back_populates="student", passive_deletes=True)
    group = relationship("Groups", back_populates="students", passive_deletes=True)

    def __repr__(self):
        return f"\nStudent name - {self.name}, id - {self.id} member of group: {self.group_id}"


class Subjects(Base):
    __tablename__ = "subject"
    id: Mapped[int] = Column(Integer, primary_key=True)
    subject: Mapped[str] = Column(String(60), nullable=False)

    teacher = relationship("Teachers", secondary="teacher_subject",
                           back_populates="subject", passive_deletes=True)
    student = relationship("Students", secondary="student_subject",
                           back_populates="subject", passive_deletes=True)
    grades = relationship("GradesBook", back_populates="subject", passive_deletes=True)

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

    student = relationship("Students", back_populates="grades", passive_deletes=True)
    subject = relationship("Subjects", back_populates="grades", passive_deletes=True)
    teacher = relationship("Teachers", back_populates="grades", passive_deletes=True)


class Groups(Base):
    __tablename__ = "group"
    id: Mapped[int] = Column(Integer, primary_key=True)
    group_name: Mapped[str] = Column(String)

    students = relationship("Students", back_populates="group", passive_deletes=True)

    def __repr__(self):
        return f"\nGroups name {self.group_name} id {self.id}"

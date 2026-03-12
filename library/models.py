from datetime import datetime, timedelta

from sqlalchemy import String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("authors.id"), nullable=False
    )
    published_year: Mapped[int] = mapped_column(Integer)
    isbn: Mapped[str | None] = mapped_column(String(13), unique=True, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="book")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="student")


class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("students.id"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id"), nullable=False
    )
    borrowed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(days=14), nullable=False
    )
    returned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    student: Mapped["Student"] = relationship("Student", back_populates="borrows")
    book: Mapped["Book"] = relationship("Book", back_populates="borrows")

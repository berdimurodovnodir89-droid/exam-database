from library.db import engine, SessionLocal, Base
from library import models

# Tables yaratish
Base.metadata.create_all(engine)

# Session ochish
session = SessionLocal()

# Author yaratish
author = models.Author(name="Test Author", bio="Test bio")

# Book yaratish
book = models.Book(
    title="Test Book", author=author, published_year=2024, isbn="1234567890123"
)

# Student yaratish
student = models.Student(
    full_name="Test Student", email="test@example.com", grade="10th"
)

# Borrow yaratish
borrow = models.Borrow(student=student, book=book)

# Database ga qo'shish
session.add(author)
session.add(book)
session.add(student)
session.add(borrow)

# Saqlash
session.commit()

# Tekshirish
print("Author:", author.name)
print("Book:", book.title)
print("Student:", student.full_name)
print("Borrow ID:", borrow.id)

# Session yopish
session.close()

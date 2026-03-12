from sqlalchemy import select
from .db import SessionLocal
from .models import Author


def create_author(name: str, bio: str | None = None) -> Author:
    """
    Yangi muallif yaratadi.

    Args:
        name (str): Muallifning ismi.
        bio (str | None): Muallif haqida qisqacha ma'lumot.

    Returns:
        Author: Yaratilgan muallif obyektini qaytaradi.
    """
    with SessionLocal() as session:
        author = Author(name=name, bio=bio)
        session.add(author)
        session.commit()
        session.refresh(author)
        return author


def get_author_by_id(author_id: int) -> Author | None:
    """
    ID orqali muallifni topadi.

    Args:
        author_id (int): Muallif identifikatori.

    Returns:
        Author | None: Agar muallif topilsa Author obyektini,
        aks holda None qaytaradi.
    """
    with SessionLocal() as session:
        stmt = select(Author).where(Author.id == author_id)
        author = session.execute(stmt).scalar_one_or_none()
        return author


def get_all_authors() -> list[Author]:
    """
    Barcha mualliflarni qaytaradi.

    Returns:
        list[Author]: Mualliflar ro'yxati.
    """
    with SessionLocal() as session:
        stmt = select(Author)
        authors = session.execute(stmt).scalars().all()
        return authors


def update_author(
    author_id: int, name: str | None = None, bio: str | None = None
) -> Author | None:
    """
    Muallif ma'lumotlarini yangilaydi.

    Args:
        author_id (int): Muallif identifikatori.
        name (str | None): Yangi ism.
        bio (str | None): Yangi bio.

    Returns:
        Author | None: Yangilangan muallif yoki None agar topilmasa.
    """
    with SessionLocal() as session:
        stmt = select(Author).where(Author.id == author_id)
        author = session.execute(stmt).scalar_one_or_none()

        if author is None:
            return None

        if name is not None:
            author.name = name

        if bio is not None:
            author.bio = bio

        session.commit()
        session.refresh(author)

        return author


def delete_author(author_id: int) -> bool:
    """
    Muallifni o'chiradi.

    Agar muallifga tegishli kitoblar mavjud bo'lsa,
    o'chirish amalga oshirilmaydi.

    Args:
        author_id (int): Muallif identifikatori.

    Returns:
        bool: True agar muvaffaqiyatli o'chirilsa,
        False agar muallif topilmasa yoki kitoblari mavjud bo'lsa.
    """
    with SessionLocal() as session:
        stmt = select(Author).where(Author.id == author_id)
        author = session.execute(stmt).scalar_one_or_none()

        if author is None:
            return False

        if author.books:
            return False

        session.delete(author)
        session.commit()

        return True

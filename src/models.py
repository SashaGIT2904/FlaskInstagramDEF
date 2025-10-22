from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    followers: Mapped[list["Follower"]] = relationship(
        back_populates="to_user", foreign_keys="Follower.user_to_id"
    )
    following: Mapped[list["Follower"]] = relationship(
        back_populates="from_user", foreign_keys="Follower.user_from_id"
    )


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class Follower(db.Model):
    __tablename__ = "follower"
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, nullable=False)

    from_user: Mapped["User"] = relationship(
        back_populates="following", foreign_keys=[user_from_id])
    to_user: Mapped["User"] = relationship(
        back_populates="followers", foreign_keys=[user_to_id])

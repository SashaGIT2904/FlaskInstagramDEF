from __future__ import annotations
from datetime import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, DateTime, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

db = SQLAlchemy()

# --------- Enums ---------
class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

# --------- User ---------
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str | None] = mapped_column(String(80))
    lastname: Mapped[str | None] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    followers: Mapped[list["Follower"]] = relationship(
        back_populates="to_user", cascade="all, delete-orphan", foreign_keys="Follower.user_to_id"
    )
    following: Mapped[list["Follower"]] = relationship(
        back_populates="from_user", cascade="all, delete-orphan", foreign_keys="Follower.user_from_id"
    )

# --------- Post ---------
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    caption: Mapped[str | None] = mapped_column(String(2200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")

# --------- Media ---------
class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(SAEnum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")

# --------- Comment ---------
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

# --------- Follower (who follows whom) ---------
class Follower(db.Model):
    __tablename__ = "follower"
    __table_args__ = (
        UniqueConstraint("user_from_id", "user_to_id", name="uq_follow_pair"),
    )

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    from_user: Mapped["User"] = relationship(back_populates="following", foreign_keys=[user_from_id])
    to_user: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[user_to_id])

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return "<User {}>".format(self.name)

# class Post(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     body: so.Mapped[str] = so.mapped_column(sa.String(140))
#     timestamp: so.Mapped[datetime] = so.mapped_column(
#         index=True, default=lambda: datetime.now(timezone.utc)
#     )
#     user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     author: so.Mapped[User] = so.relationship(back_populates="posts")

#     def __repr__(self):
#         return "<Post {}>".format(self.body)

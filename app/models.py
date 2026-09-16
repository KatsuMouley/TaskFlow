from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    created_tasks = db.relationship(
        "Task", foreign_keys="Task.created_by_id", back_populates="creator"
    )
    assigned_tasks = db.relationship(
        "Task", foreign_keys="Task.assigned_to_id", back_populates="assignee"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Task(db.Model):
    STATUSES = {
        "pending": "Pendente",
        "in_progress": "Em andamento",
        "completed": "Concluída",
    }

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    creator = db.relationship("User", foreign_keys=[created_by_id], back_populates="created_tasks")
    assignee = db.relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tasks")

    @property
    def status_label(self):
        return self.STATUSES.get(self.status, self.status)

    def can_edit(self, user):
        return user.id in (self.created_by_id, self.assigned_to_id)

    def can_delete(self, user):
        return user.id == self.created_by_id

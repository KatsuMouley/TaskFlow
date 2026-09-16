from flask import Blueprint, render_template
from flask_login import login_required

from ..models import Task, User

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
@login_required
def dashboard():
    counts = {
        key: Task.query.filter_by(status=key).count() for key in Task.STATUSES
    }
    recent_tasks = Task.query.order_by(Task.updated_at.desc()).limit(6).all()
    return render_template(
        "dashboard.html",
        counts=counts,
        recent_tasks=recent_tasks,
        total_tasks=Task.query.count(),
        total_users=User.query.count(),
    )

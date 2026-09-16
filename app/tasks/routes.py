from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Task, User
from .forms import TaskForm

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def _fill_user_choices(form):
    users = User.query.order_by(User.name).all()
    form.assigned_to_id.choices = [(user.id, user.name) for user in users]


@tasks_bp.get("")
@login_required
def list_tasks():
    selected_status = request.args.get("status", "all")
    query = Task.query
    if selected_status in Task.STATUSES:
        query = query.filter_by(status=selected_status)
    tasks = query.order_by(Task.updated_at.desc()).all()
    return render_template(
        "tasks/list.html",
        tasks=tasks,
        statuses=Task.STATUSES,
        selected_status=selected_status,
    )


@tasks_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    _fill_user_choices(form)
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=(form.description.data or "").strip(),
            status=form.status.data,
            assigned_to_id=form.assigned_to_id.data,
            created_by_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash("Tarefa criada com sucesso.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, heading="Nova tarefa")


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    if not task.can_edit(current_user):
        abort(403)

    form = TaskForm(obj=task)
    _fill_user_choices(form)
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = (form.description.data or "").strip()
        task.status = form.status.data
        task.assigned_to_id = form.assigned_to_id.data
        db.session.commit()
        flash("Tarefa atualizada com sucesso.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, heading="Editar tarefa", task=task)


@tasks_bp.post("/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    if not task.can_delete(current_user):
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Tarefa excluída.", "info")
    return redirect(url_for("tasks.list_tasks"))

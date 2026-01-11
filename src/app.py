from __future__ import annotations

from flask import Flask, jsonify, request

from .models import connect, init_db, create_task, list_tasks, get_task, update_task, delete_task


def create_app(test_db_path: str | None = None) -> Flask:
    app = Flask(__name__)

    # Inicializa DB
    conn = connect(test_db_path)
    init_db(conn)
    conn.close()

    def _conn():
        c = connect(test_db_path)
        init_db(c)
        return c

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    @app.get("/tasks")
    def tasks_list():
        status = request.args.get("status")
        conn = _conn()
        try:
            tasks = list_tasks(conn, status=status)
            return jsonify([t.__dict__ for t in tasks]), 200
        finally:
            conn.close()

    @app.post("/tasks")
    def tasks_create():
        payload = request.get_json(silent=True) or {}
        title = payload.get("title", "")
        description = payload.get("description", "")

        conn = _conn()
        try:
            task = create_task(conn, title=title, description=description)
            return jsonify(task.__dict__), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        finally:
            conn.close()

    @app.get("/tasks/<int:task_id>")
    def tasks_get(task_id: int):
        conn = _conn()
        try:
            task = get_task(conn, task_id)
            return jsonify(task.__dict__), 200
        except KeyError:
            return jsonify({"error": "task not found"}), 404
        finally:
            conn.close()

    @app.put("/tasks/<int:task_id>")
    def tasks_update(task_id: int):
        payload = request.get_json(silent=True) or {}
        conn = _conn()
        try:
            task = update_task(
                conn,
                task_id=task_id,
                title=payload.get("title"),
                description=payload.get("description"),
                status=payload.get("status"),
            )
            return jsonify(task.__dict__), 200
        except KeyError:
            return jsonify({"error": "task not found"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        finally:
            conn.close()

    @app.delete("/tasks/<int:task_id>")
    def tasks_delete(task_id: int):
        conn = _conn()
        try:
            delete_task(conn, task_id)
            return "", 204
        except KeyError:
            return jsonify({"error": "task not found"}), 404
        finally:
            conn.close()

    return app


if __name__ == "__main__":
    # Execução local
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

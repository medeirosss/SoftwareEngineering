from __future__ import annotations

import json
import os
import tempfile

from src.app import create_app


def test_health_ok():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        app = create_app(test_db_path=db)
        client = app.test_client()

        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "ok"


def test_create_task_and_get_task():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        app = create_app(test_db_path=db)
        client = app.test_client()

        create = client.post("/tasks", data=json.dumps({"title": "Criar tela", "description": "Tela de cadastro"}),
                             content_type="application/json")
        assert create.status_code == 201
        task = create.get_json()
        assert task["id"] > 0
        assert task["status"] == "todo"

        gett = client.get(f"/tasks/{task['id']}")
        assert gett.status_code == 200
        assert gett.get_json()["title"] == "Criar tela"


def test_validation_title_min_length():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        app = create_app(test_db_path=db)
        client = app.test_client()

        resp = client.post("/tasks", json={"title": "ab"})
        assert resp.status_code == 400
        assert "at least 3" in resp.get_json()["error"]


def test_update_status():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        app = create_app(test_db_path=db)
        client = app.test_client()

        create = client.post("/tasks", json={"title": "Configurar CI"})
        task_id = create.get_json()["id"]

        upd = client.put(f"/tasks/{task_id}", json={"status": "in_progress"})
        assert upd.status_code == 200
        assert upd.get_json()["status"] == "in_progress"


def test_delete_task():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test.db")
        app = create_app(test_db_path=db)
        client = app.test_client()

        create = client.post("/tasks", json={"title": "Apagar tarefa"})
        task_id = create.get_json()["id"]

        delete = client.delete(f"/tasks/{task_id}")
        assert delete.status_code == 204

        gett = client.get(f"/tasks/{task_id}")
        assert gett.status_code == 404

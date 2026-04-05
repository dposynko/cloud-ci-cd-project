from app.main import app

def test_home():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200

def test_healthz():
    client = app.test_client()
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json["status"] == "ok"

def test_version_default():
    client = app.test_client()
    r = client.get("/version")
    assert r.status_code == 200
    assert "version" in r.json


def test_version_exists():
    client = app.test_client()
    r = client.get("/version")
    assert r.status_code == 200
    assert "version" in r.json

import pytest
from orphan_finder.core import delete_resource


@pytest.mark.parametrize(
    "rtype, expected_method",
    [
        ("server", "compute.delete_server"),
        ("volume", "block_storage.delete_volume"),
        ("network", "network.delete_network"),
        ("router", "network.delete_router"),
        ("port", "network.delete_port"),
        ("security_group", "network.delete_security_group"),
    ],
)
def test_delete_resource_dispatch(monkeypatch, rtype, expected_method):
    """Check, if delete_resource uses"""

    called = {}

    def fake_delete(id, **kwargs):
        called["ok"] = (id, kwargs)

    parts = expected_method.split(".")
    obj = type("Fake", (), {})()
    setattr(obj, parts[-1], fake_delete)
    conn = type("Conn", (), {parts[0]: obj})()

    res = {"id": "123", "resource_type": rtype}
    delete_resource(conn, res)

    assert called["ok"][0] == "123"
    assert called["ok"][1].get("ignore_missing") is True

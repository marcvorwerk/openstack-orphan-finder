from orphan_finder.core import delete_orphans


def test_delete_orphans_interactive(monkeypatch):
    deleted_resources = []

    def mock_delete_resource(conn, res):
        deleted_resources.append(res)

    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setattr("orphan_finder.core.delete_resource", mock_delete_resource)

    resources = [
        {"id": "abc", "name": "srv-abc", "project_id": "123", "resource_type": "server"}
    ]

    deleted = delete_orphans(conn=None, resources=resources, require_confirmation=True)

    assert len(deleted) == 1
    assert deleted[0]["id"] == "abc"

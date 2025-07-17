from orphan_finder.core import find_all_orphans


def test_find_all_orphans_empty(monkeypatch):
    monkeypatch.setattr("orphan_finder.core.create_connection", lambda: None)
    monkeypatch.setattr("orphan_finder.core.get_existing_project_ids", lambda _: set())
    monkeypatch.setattr("orphan_finder.core.RESOURCE_MODULES", {})

    result = find_all_orphans()
    assert result == []

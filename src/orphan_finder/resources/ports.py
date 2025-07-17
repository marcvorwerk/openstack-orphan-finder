def find_orphans(conn, known_projects, filter_project_id=None):
    orphans = []
    for port in conn.network.ports():
        if not port.project_id:
            continue
        if filter_project_id and port.project_id != filter_project_id:
            continue
        if port.project_id not in known_projects:
            orphans.append(
                {
                    "id": port.id,
                    "name": port.name,
                    "project_id": port.project_id,
                    "resource_type": "port",
                }
            )
    return orphans


def get_all(conn):
    return [
        {
            "id": port.id,
            "name": port.name,
            "project_id": port.project_id,
            "resource_type": "port",
        }
        for port in conn.network.ports(all_projects=True)
    ]

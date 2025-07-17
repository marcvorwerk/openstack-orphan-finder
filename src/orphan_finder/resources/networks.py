def find_orphans(conn, known_projects, filter_project_id=None):
    orphans = []
    for net in conn.network.networks():
        if not net.project_id:
            continue
        if filter_project_id and net.project_id != filter_project_id:
            continue
        if net.project_id not in known_projects:
            orphans.append(
                {
                    "id": net.id,
                    "name": net.name,
                    "project_id": net.project_id,
                    "resource_type": "network",
                }
            )
    return orphans


def get_all(conn):
    return [
        {
            "id": net.id,
            "name": net.name,
            "project_id": net.project_id,
            "resource_type": "network",
        }
        for net in conn.network.networks(all_projects=True)
    ]

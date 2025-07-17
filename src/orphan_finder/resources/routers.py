def find_orphans(conn, known_projects, filter_project_id=None):
    orphans = []
    for router in conn.network.routers():
        if not router.project_id:
            continue
        if filter_project_id and router.project_id != filter_project_id:
            continue
        if router.project_id not in known_projects:
            orphans.append(
                {
                    "id": router.id,
                    "name": router.name,
                    "project_id": router.project_id,
                    "resource_type": "router",
                }
            )
    return orphans


def get_all(conn):
    return [
        {
            "id": router.id,
            "name": router.name,
            "project_id": router.project_id,
            "resource_type": "router",
        }
        for router in conn.network.routers(all_projects=True)
    ]

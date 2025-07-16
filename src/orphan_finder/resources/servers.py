def find_orphans(conn, known_projects, filter_project_id=None):
    orphans = []
    for server in conn.compute.servers(all_projects=True):
        if filter_project_id and server.project_id != filter_project_id:
            continue
        if server.project_id not in known_projects:
            orphans.append({
                "id": server.id,
                "name": server.name,
                "project_id": server.project_id,
                "resource_type": "server",
            })
    return orphans

def get_all(conn):
    return [{
        "id": server.id,
        "name": server.name,
        "project_id": server.project_id,
        "resource_type": "server",
    } for server in conn.compute.servers(all_projects=True)]

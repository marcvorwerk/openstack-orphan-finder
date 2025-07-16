def find_orphans(conn, known_projects, filter_project_id=None):
    orphans = []
    for sg in conn.network.security_groups():
        if not sg.project_id:
            continue
        if filter_project_id and sg.project_id != filter_project_id:
            continue
        if sg.project_id not in known_projects:
            orphans.append({
                "id": sg.id,
                "name": sg.name,
                "project_id": sg.project_id,
                "resource_type": "security_group",
            })
    return orphans

def get_all(conn):
    return [{
        "id": sg.id,
        "name": sg.name,
        "project_id": sg.project_id,
        "resource_type": "security_group",
    } for sg in conn.network.security_groups(all_projects=True)]

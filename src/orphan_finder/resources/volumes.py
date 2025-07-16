def find_orphans(conn, known_projects, filter_project_id=None):
    orphans = []
    for volume in conn.block_storage.volumes(details=True, all_projects=True):
        if filter_project_id and volume.project_id != filter_project_id:
            continue
        if volume.project_id not in known_projects:
            orphans.append({
                "id": volume.id,
                "name": volume.name,
                "project_id": volume.project_id,
                "resource_type": "volume",
            })
    return orphans

def get_all(conn):
    return [{
        "id": volume.id,
        "name": volume.name,
        "project_id": volume.project_id,
        "resource_type": "volume",
    } for volume in conn.block_storage.volumes(details=True, all_projects=True)]

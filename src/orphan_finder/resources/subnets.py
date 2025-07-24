def get_all(conn):
    return list(conn.network.subnets())

def find_orphans(conn, existing_projects, filter_project_id=None):
    orphans = []
    for subnet in get_all(conn):
        if subnet.project_id not in existing_projects:
            if filter_project_id and subnet.project_id != filter_project_id:
                continue
            orphans.append({
                "id": subnet.id,
                "name": subnet.name,
                "project_id": subnet.project_id,
                "resource_type": "subnet",
            })
    return orphans

#def delete(conn, resource_id):
#    conn.network.delete_subnet(resource_id)


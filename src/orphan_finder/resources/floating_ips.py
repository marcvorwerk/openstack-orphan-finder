def get_all(conn):
    return list(conn.network.ips())

def find_orphans(conn, existing_projects, filter_project_id=None):
    orphans = []
    for fip in get_all(conn):
        if fip.project_id not in existing_projects:
            if filter_project_id and fip.project_id != filter_project_id:
                continue
            orphans.append({
                "id": fip.id,
                "name": fip.floating_ip_address,
                "project_id": fip.project_id,
                "resource_type": "floating_ip",
            })
    return orphans

#def delete(conn, resource_id):
#    conn.network.delete_ip(resource_id)


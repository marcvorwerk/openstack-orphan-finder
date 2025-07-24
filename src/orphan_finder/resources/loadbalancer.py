def get_all(conn):
    return list(conn.load_balancer.load_balancers())

def find_orphans(conn, existing_projects, filter_project_id=None):
    orphans = []
    for lb in get_all(conn):
        if lb.project_id not in existing_projects:
            if filter_project_id and lb.project_id != filter_project_id:
                continue
            orphans.append({
                "id": lb.id,
                "name": lb.name,
                "project_id": lb.project_id,
                "resource_type": "loadbalancer",
            })
    return orphans

#def delete(conn, resource_id):
#    conn.load_balancer.delete_load_balancer(resource_id, cascade=True)

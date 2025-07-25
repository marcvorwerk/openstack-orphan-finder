import openstack

from orphan_finder.resources import (
    networks,
    subnets,
    ports,
    routers,
    security_groups,
    loadbalancer,
    servers,
    volumes,
    floating_ips
)

RESOURCE_MODULES = {
    "servers": servers,
    "volumes": volumes,
    "networks": networks,
    "subnets": subnets,
    "routers": routers,
    "ports": ports,
    "floating_ips": floating_ips,
    "security_groups": security_groups,
    "loadbalancer": loadbalancer
}


def create_connection() -> openstack.connection.Connection:
    return openstack.connect()


def get_existing_project_ids(conn) -> set[str]:
    return {project.id for project in conn.identity.projects()}


def find_all_orphans(
    project_id: str | None = None, only_resources: list[str] | None = None
) -> list[dict]:
    conn = create_connection()
    existing_projects = get_existing_project_ids(conn)

    modules = RESOURCE_MODULES
    if only_resources:
        modules = {name: mod for name, mod in modules.items() if name in only_resources}

    result = []
    for name, mod in modules.items():
        result += mod.find_orphans(
            conn, existing_projects, filter_project_id=project_id
        )
    return result


def collect_stats(
    project_id: str | None = None,
    only_resources: list[str] | None = None,
) -> dict:
    conn = create_connection()
    existing_projects = get_existing_project_ids(conn)

    modules = RESOURCE_MODULES
    if only_resources:
        modules = {name: mod for name, mod in modules.items() if name in only_resources}

    stats = {}
    for name, mod in modules.items():
        all_resources = mod.get_all(conn)
        filtered_resources = (
            [r for r in all_resources if r.get("project_id") == project_id]
            if project_id
            else all_resources
        )

        orphans = mod.find_orphans(
            conn,
            existing_projects,
            filter_project_id=project_id,
        )

        stats[name] = {
            "total": len(filtered_resources),
            "orphans": len(orphans),
        }

    return stats


# Funktion nicht vollstaendig, da wir keine Abhaenigkeiten wie z.B. Subnetze pruefen
# sollten das eh in die resoources auslagern
def delete_resource(conn, res: dict):
    typ = res["resource_type"]
    rid = res["id"]

    if typ == "server":
        conn.compute.delete_server(rid, ignore_missing=True)
    elif typ == "volume":
        conn.block_storage.delete_volume(rid, ignore_missing=True)
    elif typ == "network":
        conn.network.delete_network(rid, ignore_missing=True)
    elif typ == "router":
        conn.network.delete_router(rid, ignore_missing=True)
    elif typ == "port":
        conn.network.delete_port(rid, ignore_missing=True)
    elif typ == "security_group":
        conn.network.delete_security_group(rid, ignore_missing=True)
    else:
        raise ValueError(f"Unknown resource typ: {typ}")


def delete_orphans(conn, resources: list[dict], require_confirmation: bool = True):
    deleted = []

    for res in resources:
        if require_confirmation:
            confirm = input(
                f"Delete {res['resource_type']} '{res['name']}' ({res['id']})? [y/N]: "
            )
            if confirm.lower() != "y":
                continue

        try:
            delete_resource(conn, res)
            deleted.append(res)
        except Exception as e:
            print(f"❌ Error during delete of {res['id']}: {e}")

    return deleted

import json
from typing import Any, Dict, List

import yaml


def print_json(resources: List[Dict[str, Any]]) -> None:
    print(
        json.dumps(
            {
                "orphan_resources": resources,
                "total": len(resources),
            },
            indent=2,
        )
    )


def print_yaml(resources: List[Dict[str, Any]]) -> None:
    data = {
        "orphan_resources": resources,
        "total": len(resources),
    }
    print(yaml.safe_dump(data, sort_keys=False))


def print_markdown(resources: List[Dict[str, Any]]) -> None:
    if not resources:
        print("✅ No orphan resources found.")
        return

    print(f"# Found orphan resources\n\nFindings: **{len(resources)}**\n")

    grouped = {}
    for res in resources:
        grouped.setdefault(res["resource_type"], []).append(res)

    for rtype, entries in grouped.items():
        print(f"## {rtype.capitalize()} ({len(entries)})\n")
        print("| ID | Name | Project ID |")
        print("|----|------|------------|")
        for res in entries:
            print(f"| `{res['id']}` | {res['name']} | `{res['project_id']}` |")
        print()

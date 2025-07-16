import typer
from typing import Optional, List
from orphan_finder.core import find_all_orphans, collect_stats, RESOURCE_MODULES
from orphan_finder.report import print_json, print_yaml, print_markdown

app = typer.Typer(help="OpenStack Orphan Resource Finder")

@app.command()
def find(
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Search by Project ID"),
    resource: Optional[List[str]] = typer.Option(None, "--resource", "-r", help=f"Limit to given Resource. Available: {', '.join(RESOURCE_MODULES.keys())}"),
    output: str = typer.Option("markdown", "--output", "-o", help="Output format: markdown (default), json, yaml", case_sensitive=False),
):
    """Search orphan resources"""
    if resource:
        invalid = [r for r in resource if r not in RESOURCE_MODULES]
        if invalid:
            typer.echo(f"❌ Unknown resource type: {', '.join(invalid)}")
            raise typer.Exit(1)

    orphans = find_all_orphans(project_id=project, only_resources=resource)

    if output == "json":
        print_json(orphans)
    elif output == "yaml":
        print_yaml(orphans)
    elif output == "markdown":
        print_markdown(orphans)
    else:
        typer.echo("❌ Unknown output format. Supported formats: markdown, json, yaml")


@app.command()
def stats(
    resource: Optional[List[str]] = typer.Option(None, "--resource", "-r", help="Limit to given resource type")
):
    """Show statistics of all resources and their orphan share"""
    stats = collect_stats(only_resources=resource)

    total = sum(x["total"] for x in stats.values())
    total_orphans = sum(x["orphans"] for x in stats.values())

    print(f"# Resource Statistic\n")
    print(f"| Resource Typ     | Total | Orphan |")
    print(f"|------------------|-------|--------|")

    for res, data in stats.items():
        print(f"| {res.capitalize():<17} | {data['total']:>6} | {data['orphans']:>8} |")

    print(f"| {'**Total**':<17} | **{total}** | **{total_orphans}** |")


@app.command()
def delete(
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Limit to project ID"),
    resource: Optional[List[str]] = typer.Option(None, "--resource", "-r", help="Limit to given resource type"),
    force: bool = typer.Option(False, "--force", help="Delete without project limitation (⚠️)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Automatically approve all delete requests"),
):
    """Delete orphan resources"""
    if not project and not force:
        typer.echo("❌ You must provide either --project or --force")
        raise typer.Exit(1)

    if resource:
        invalid = [r for r in resource if r not in RESOURCE_MODULES]
        if invalid:
            typer.echo(f"❌ Invalid resource type: {', '.join(invalid)}")
            raise typer.Exit(1)

    conn = create_connection()
    existing_projects = get_existing_project_ids(conn)

    orphans = find_all_orphans(
        project_id=project,
        only_resources=resource
    )

    if not orphans:
        typer.echo("✅ No orphan resource found.")
        raise typer.Exit()

    typer.echo(f"💥 {len(orphans)} resources will be deleted.")

    if not yes:
        confirm = input("⚠️ Are you sure you want to continue? [y/N]: ")
        if confirm.lower() != "y":
            typer.echo("❌ Abort ...")
            raise typer.Exit()

    from orphan_finder.core import delete_orphans
    deleted = delete_orphans(conn, orphans, require_confirmation=not yes)

    typer.echo(f"✅ {len(deleted)} resources deleted.")


@app.command()
def validate():
    """Evaluates whether a given resource (in the project) is really orphan"""
    print("Function not implemented yet")

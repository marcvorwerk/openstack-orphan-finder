from orphan_finder.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Orphan Resource Finder" in result.output

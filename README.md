# 🧹 OpenStack Orphan Finder

CLI tool to find, list, and optionally delete orphaned OpenStack resources (servers, volumes, ports, routers, etc.).

---

## 🚀 Features

- Find orphaned resources not linked to any project
- Output formats: `markdown` (default), `json`, `yaml`
- Optional deletion with confirmation
- Per-project filtering and resource-type filtering
- Stats for orphaned resource types

---

## ⚙️ Requirements

- Python ≥ 3.10  
- OpenStack clouds.yaml or env var (`OS_CLOUD`)

---

## 📦 Install (with Poetry)

```bash
poetry install
```

Use a specific Python version?

```bash
pyenv install 3.12.6
pyenv local 3.12.6
poetry env use $(pyenv which python)
```

## Run Tests

```bash
poetry run pytest
```

## License

MIT

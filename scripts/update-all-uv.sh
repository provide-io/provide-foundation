for i in *; do (cd $i; deactivate; source .venv/bin/activate; uv sync --all-groups --dev --upgrade;); done;

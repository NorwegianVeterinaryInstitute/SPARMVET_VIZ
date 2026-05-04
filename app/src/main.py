# @deps
# provides: app (Shiny App instance, entry point)
# consumes: shiny, app.src.ui, app.src.server
# consumed_by: Shiny runner (uvicorn/shiny run), __main__
# @end_deps
# app/src/app.py
from shiny import App
from app.src.ui import app_ui
from app.src.server import server

# Concatenate UI Scaffolding and Reactive Server Logic
app = App(app_ui, server)

if __name__ == "__main__":
    # Internal execution hook
    import os
    print(f"--- SPARMVET DASHBOARD INITIALIZED ---")
    print(f"Mode: pipeline")
    print(f"Venv: ./.venv/bin/python")

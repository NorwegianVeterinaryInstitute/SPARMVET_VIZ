# app.py
from shiny import App
from app.src.ui import create_ui
from app.src.server import server_logic

# The Orchestrator and Display are wired together here
app = App(create_ui(), server_logic)

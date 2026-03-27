# --- Auto-Load Strategy ---
# We explicitly import the sub-packages here.
# Importing them executes their code, which triggers the @register_action decorators
# defined in base.py, safely populating the AVAILABLE_WRANGLING_ACTIONS dictionary
# at system boot-up.
from transformer.actions import advanced
from transformer.actions import core

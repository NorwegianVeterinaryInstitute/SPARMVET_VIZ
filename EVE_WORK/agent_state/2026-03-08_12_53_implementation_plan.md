# Transformer Plugin Architecture & Wrangling Documentation

## Goal Description
The current [registry.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/help_registry.py) in the Transformer module is a monolithic file. As the dashboard grows and more specific wrangling actions are needed (e.g. specialized bio-math), this file will become difficult to maintain. The goal is to refactor this into an extensible `actions/` submodule using a Python decorator registration pattern. Additionally, a new Quarto cheatsheet will be created to formally document the YAML syntax for all available wrangling actions.

## User Review Required
> [!IMPORTANT]
> **Decorator Pattern vs Dynamic Globbing**
> I propose using an explicit Decorator Pattern for registering actions rather than "magic" dynamic file loading (using `importlib`). The decorator pattern is substantially safer, standard in Python (e.g. Flask/FastAPI), and prevents unexpected code execution if malicious files are dropped into the directory. Let me know if you agree with this design!

## Proposed Changes

### Transformer Actions Submodule
We will create a deeply nested directory structure for actions. Rather than having a single `core.py` file that could eventually grow to 1000+ lines, `core/` and `advanced/` will be their own sub-packages.

#### [NEW] `libs/transformer/src/actions/core/`
A directory containing small, single-purpose Python files (or logical groups) for basic manipulations.
- `libs/transformer/src/actions/core/null_handling.py` (e.g. [fill_nulls](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#6-16), [drop_nulls](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#42-47))
- `libs/transformer/src/actions/core/renaming.py` (e.g. [rename](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#30-40))
- `libs/transformer/src/actions/core/__init__.py` (Exposes/imports the files above)

#### [NEW] `libs/transformer/src/actions/advanced/`
A directory for complex bio-math or domain-specific logic.
- `libs/transformer/src/actions/advanced/categories.py` (e.g. [derive_categories](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#69-104), [split_and_explode](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#18-28))
- `libs/transformer/src/actions/advanced/__init__.py` (Exposes/imports the files above)

#### [NEW] `libs/transformer/src/actions/__init__.py`
This root file will define the `@register_action` decorator and hold the central `AVAILABLE_WRANGLING_ACTIONS` dictionary. It will explicitly import the `core` and `advanced` sub-packages, triggering the decorators and registering all actions safely at boot time.

#### [MODIFY] [libs/transformer/src/registry.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py)
This file will be completely rewritten to act purely as a lightweight interface that imports `AVAILABLE_WRANGLING_ACTIONS` and [get_action_function](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#122-129) from the new `actions/` submodule, ensuring we do not break any existing imports in [data_wrangler.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/data_wrangler.py).

### Documentation

#### [NEW] `docs/cheatsheets/wrangling_actions.qmd`
A dedicated Quarto cheatsheet detailing exactly how to use the wrangling YAML arrays, including complete examples for the [derive_categories](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#69-104) action.

#### [MODIFY] [docs/_quarto.yml](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/docs/_quarto.yml)
Update the sidebar configuration to include the new `wrangling_actions.qmd` file under the Cheatsheets section.

## Verification Plan

### Automated Tests
- Run `python libs/transformer/tests/test_wrangler.py --yaml config/manifests/pipelines/1_Abromics_general_pipeline.yaml --data test_data/` to verify that the newly refactored plugin registry successfully loads the [derive_categories](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#69-104) action defined in [ResFinder_wrangling.yaml](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/config/manifests/pipelines/1_Abromics_general_pipeline/ResFinder_wrangling.yaml) and executes it exactly as before, without throwing `ActionNotFound` errors.

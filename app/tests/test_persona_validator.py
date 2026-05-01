"""Unit tests for PersonaValidator (25-B)."""
import pytest
from app.modules.persona_validator import PersonaValidator

V = PersonaValidator()

_FULL_FEATURES = {
    "interactivity_enabled": True,
    "developer_mode_enabled": False,
    "gallery_enabled": False,
    "comparison_mode_enabled": False,
    "session_management_enabled": False,
    "import_helper_enabled": False,
    "export_bundle_enabled": True,
    "export_graph_enabled": False,
    "metadata_ingestion_enabled": False,
    "data_ingestion_enabled": False,
}


def _tmpl(overrides=None, ms_visible=True, ms_fixed=None, testing_mode=True, persona_id=None, path="developer_template"):
    t = {
        "persona_id": persona_id or path.replace("_template", ""),
        "features": {**_FULL_FEATURES, **(overrides or {})},
        "manifest_selector": {"visible": ms_visible, "fixed_manifest": ms_fixed},
        "testing_mode": testing_mode,
    }
    return t, path


# --- Rule 1: persona_id must match filename ---

def test_persona_id_matches_filename_valid():
    t, path = _tmpl(path="developer_template", persona_id="developer")
    assert V.validate(t, path) == []


def test_persona_id_mismatch_raises_error():
    t, path = _tmpl(path="developer_template", persona_id="qa")
    errors = V.validate(t, path)
    assert any("does not match filename" in e for e in errors)


# --- Rule 2: persona_id must use hyphens ---

def test_persona_id_underscore_raises_error():
    t, path = _tmpl(path="pipeline_exploration_advanced_template",
                    persona_id="pipeline_exploration_advanced")
    errors = V.validate(t, path)
    assert any("underscores" in e for e in errors)


def test_persona_id_hyphen_is_valid():
    t, path = _tmpl(path="pipeline-exploration-advanced_template",
                    persona_id="pipeline-exploration-advanced")
    assert V.validate(t, path) == []


# --- Rule 3: missing flags produce warnings only (not errors) ---

def test_missing_flag_no_error(capsys):
    t = {
        "persona_id": "developer",
        "features": {},  # all missing
        "manifest_selector": {"visible": True, "fixed_manifest": None},
        "testing_mode": True,
    }
    errors = V.validate(t, "developer_template")
    assert errors == []
    captured = capsys.readouterr()
    assert "WARNING" in captured.out


# --- Rule 4: manifest_selector.visible=false requires fixed_manifest ---

def test_manifest_selector_hidden_no_fixed_manifest_errors():
    t, path = _tmpl(path="pipeline-static_template",
                    persona_id="pipeline-static",
                    ms_visible=False, ms_fixed=None)
    errors = V.validate(t, path)
    assert any("fixed_manifest is null" in e for e in errors)


def test_manifest_selector_hidden_with_fixed_manifest_ok():
    t, path = _tmpl(path="pipeline-static_template",
                    persona_id="pipeline-static",
                    ms_visible=False, ms_fixed="/data/manifests/project.yaml")
    assert V.validate(t, path) == []


def test_manifest_selector_visible_no_fixed_manifest_ok():
    t, path = _tmpl(path="developer_template", persona_id="developer",
                    ms_visible=True, ms_fixed=None)
    assert V.validate(t, path) == []


# --- validate_file: real template files ---

def test_validate_real_developer_template():
    errors = V.validate_file("config/ui/templates/developer_template.yaml")
    assert errors == [], f"developer_template errors: {errors}"


def test_validate_real_pipeline_static_template():
    errors = V.validate_file("config/ui/templates/pipeline-static_template.yaml")
    # pipeline-static has manifest_selector.visible=false + fixed_manifest=null → expected error
    assert any("fixed_manifest" in e for e in errors), \
        "Expected fixed_manifest error for pipeline-static (null is intentional — operator fills this)"


def test_validate_real_qa_template():
    errors = V.validate_file("config/ui/templates/qa_template.yaml")
    assert errors == [], f"qa_template errors: {errors}"


def test_validate_missing_file():
    errors = V.validate_file("config/ui/templates/nonexistent_template.yaml")
    assert any("not found" in e for e in errors)

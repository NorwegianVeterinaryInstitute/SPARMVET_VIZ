# libs/utils/src/utils/blueprint_mapper.py
import re
from pathlib import Path
from typing import Dict, List, Optional


class BlueprintMapper:
    """
    [ADR-039] Generates a DAG-based 'TubeMap' visualization for SPARMVET manifests.

    Parses the full manifest structure (data_schemas, additional_datasets_schemas,
    metadata_schema, assembly_manifests, and plots flattened by ConfigManager from
    analysis_groups) and outputs correct Mermaid.js DAG code with high-density styling.

    IMPORTANT: Pass raw_config from ConfigManager (not yaml.safe_load) so that:
      - !include tags are resolved
      - analysis_groups plots are flattened into raw_config['plots'] with target_dataset

    Node types per schema (shown as a mini-chain inside each section):
      source   (blue)   — the raw data source node for data_schemas
      wrangle  (yellow) — wrangling step, labelled "<schema_id>\\nWrangling"
      assembly (purple) — assembly_manifests join node
      plot     (green)  — terminal plot node
      ref      (grey)   — additional_datasets_schemas
      meta     (orange) — metadata_schema
    """

    def __init__(self, raw_config: Dict, active_node: Optional[str] = None):
        self.cfg = raw_config
        self.nodes: List[str] = []
        self.edges: List[str] = []
        self.style_classes: List[str] = []
        self.active_node = active_node

    def _get_label(self, node_id: str, details) -> str:
        """Safely extracts a short display label from node details."""
        if not isinstance(details, dict):
            return node_id
        info = details.get("info", {})
        if isinstance(info, str):
            return info[:35] if len(info) > 35 else info
        elif isinstance(info, dict):
            return info.get("display_name", info.get("sub_category", info.get("title", node_id)))
        return details.get("description", node_id)[:35] if isinstance(
            details.get("description"), str) else node_id

    def _safe_node_id(self, raw_id: str) -> str:
        """Sanitize node IDs for Mermaid compatibility."""
        return re.sub(r'[^A-Za-z0-9_]', '_', raw_id)

    def _n(self, sid: str, suffix: str) -> str:
        """Build a composite Mermaid node ID: <safe_schema_id>__<suffix>"""
        return f"{self._safe_node_id(sid)}__{suffix}"

    def generate_mermaid(self) -> str:
        """
        Build a fully structure-aware Mermaid LR DAG.

        Each data schema is rendered as a mini-chain:
            [Source] --> [Wrangling] --> (Assembly) --> [[Plot]]

        All nodes are clickable and emit their schema_id to the Shiny bridge.
        """
        self.nodes = []
        self.edges = []
        self.style_classes = []
        _clickable: list = []   # (mermaid_node_id, schema_id) pairs
        all_known: set = set()

        def _add_node(mermaid_id: str, defn: str, css_class: str, schema_id: str):
            self.nodes.append(defn)
            self.style_classes.append(f'class {mermaid_id} {css_class}')
            all_known.add(mermaid_id)
            _clickable.append((mermaid_id, schema_id))

        def _add_edge(a: str, b: str):
            self.edges.append(f'{a} --> {b}')

        # ── 1. Data Schemas ────────────────────────────────────────────────────
        schemas = self.cfg.get("data_schemas", {})
        for sid, details in schemas.items():
            safe = self._safe_node_id(sid)
            label = self._get_label(sid, details)
            # Source node
            _add_node(safe, f'{safe}(["{label}\\nSource"])', "trunk", sid)
            # Wrangling node (always present — may be inline or file)
            has_wrn = isinstance(details, dict) and bool(
                details.get("wrangling") or details.get("recipe"))
            wrn_id = self._n(sid, "wrn")
            if has_wrn:
                _add_node(wrn_id, f'{wrn_id}["{sid}\\nWrangling"]', "wrangle", sid)
                _add_edge(safe, wrn_id)
            else:
                # passthrough — source connects directly downstream
                wrn_id = safe

        # ── 2. Additional Datasets ─────────────────────────────────────────────
        add_schemas = self.cfg.get("additional_datasets_schemas", {})
        for aid, details in add_schemas.items():
            safe = self._safe_node_id(aid)
            label = self._get_label(aid, details)
            _add_node(safe, f'{safe}(["{label}\\nRef Data"])', "ref", aid)
            has_wrn = isinstance(details, dict) and bool(
                details.get("wrangling") or details.get("recipe"))
            wrn_id = self._n(aid, "wrn")
            if has_wrn:
                _add_node(wrn_id, f'{wrn_id}["{aid}\\nWrangling"]', "wrangle", aid)
                _add_edge(safe, wrn_id)

        # ── 3. Metadata Schema ─────────────────────────────────────────────────
        meta = self.cfg.get("metadata_schema", {})
        if meta:
            _add_node("metadata_schema",
                      'metadata_schema(["Metadata\\nSchema"])', "meta", "metadata_schema")
            has_wrn = isinstance(meta, dict) and bool(
                meta.get("wrangling") or meta.get("recipe"))
            if has_wrn:
                wrn_id = self._n("metadata_schema", "wrn")
                _add_node(wrn_id, f'{wrn_id}["metadata_schema\\nWrangling"]',
                          "wrangle", "metadata_schema")
                _add_edge("metadata_schema", wrn_id)

        # ── 4. Assembly Manifests ──────────────────────────────────────────────
        assemblies = self.cfg.get("assembly_manifests", {})

        def _upstream_node(parent_raw: str) -> str:
            """Return the last node in the parent schema's chain."""
            safe = self._safe_node_id(parent_raw)
            wrn_id = self._n(parent_raw, "wrn")
            return wrn_id if wrn_id in all_known else safe

        for asid, details in assemblies.items():
            safe = self._safe_node_id(asid)
            _add_node(safe, f'{safe}{{"{asid}\\nAssembly"}}', "branch", asid)

            ingredients = []
            if isinstance(details, dict):
                raw_ing = details.get("ingredients", [])
                for ing in raw_ing:
                    if isinstance(ing, dict):
                        did = ing.get("dataset_id", "")
                        if did:
                            ingredients.append(did)
                    elif isinstance(ing, str):
                        ingredients.append(ing)

            for parent_raw in ingredients:
                up = _upstream_node(parent_raw)
                _add_edge(up, safe)

            # Assembly wrangling/recipe node
            has_wrn = isinstance(details, dict) and bool(
                details.get("wrangling") or details.get("recipe"))
            if has_wrn:
                wrn_id = self._n(asid, "wrn")
                _add_node(wrn_id, f'{wrn_id}["{asid}\\nAssembly Wrangling"]',
                          "wrangle", asid)
                _add_edge(safe, wrn_id)

        # ── 5. Plots ───────────────────────────────────────────────────────────
        analysis_groups = self.cfg.get("analysis_groups", {})
        plots_flat = self.cfg.get("plots", {})

        plot_to_group: dict = {}
        for group_name, group_spec in analysis_groups.items():
            if isinstance(group_spec, dict):
                for pid in group_spec.get("plots", {}).keys():
                    plot_to_group[pid] = group_name

        # Also pick up target_dataset from analysis_groups directly (inline manifests
        # don't go through ConfigManager flattening so plots_flat may be empty)
        inline_plots: dict = {}
        for group_name, group_spec in analysis_groups.items():
            if isinstance(group_spec, dict):
                for pid, pspec in group_spec.get("plots", {}).items():
                    if pid not in plots_flat:
                        inline_plots[pid] = pspec if isinstance(pspec, dict) else {}

        all_plots = {**plots_flat, **inline_plots}

        subgraphs: dict = {}
        for pid, pspec in all_plots.items():
            safe_pid = self._safe_node_id(pid)
            label = pid.replace("_", " ").title()
            node_def = f'{safe_pid}[["{label}\\nPlot"]]'
            self.style_classes.append(f'class {safe_pid} plot')
            all_known.add(safe_pid)
            _clickable.append((safe_pid, pid))

            group_name = plot_to_group.get(pid, "Ungrouped")
            subgraphs.setdefault(group_name, []).append(node_def)

            target_raw = None
            if isinstance(pspec, dict):
                target_raw = (pspec.get("target_dataset")
                              or pspec.get("assembly_id"))

            if target_raw:
                # Connect from assembly wrangling output if present, else assembly
                asm_wrn = self._n(target_raw, "wrn")
                up = asm_wrn if asm_wrn in all_known else self._safe_node_id(target_raw)
                self.edges.append(f'{up} --> {safe_pid}')
            else:
                info_id = f"INFO_{safe_pid}"
                self.nodes.append(
                    f'{info_id}["ℹ️ {pid}\\nSet target_dataset"]')
                self.style_classes.append(f"class {info_id} info")
                self.edges.append(f"{info_id} -.-> {safe_pid}")

        # ── Build Mermaid string ───────────────────────────────────────────────
        lines = [
            "graph LR",
            "%% Styling",
            "classDef trunk   fill:#0d6efd,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef ref     fill:#6c757d,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef meta    fill:#fd7e14,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef wrangle fill:#ffc107,stroke:#555,stroke-width:1px,color:#212529",
            "classDef branch  fill:#9c27b0,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef plot    fill:#198754,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef info    fill:#e3f2fd,stroke:#1976d2,stroke-width:1px,color:#1a1a1a",
            "classDef activeNode stroke:#212529,stroke-width:4px,stroke-dasharray:5 5",
            "%% Nodes",
        ]
        lines.extend(self.nodes)

        for group_name, group_nodes in subgraphs.items():
            safe_group = self._safe_node_id(group_name)
            lines.append(f'subgraph {safe_group}["{group_name}"]')
            lines.extend(f'  {n}' for n in group_nodes)
            lines.append("end")

        lines.append("%% Edges")
        lines.extend(self.edges)
        lines.append("%% Classes")
        lines.extend(self.style_classes)

        if self.active_node:
            safe_active = self._safe_node_id(self.active_node)
            lines.append(f'class {safe_active} activeNode')
            # Also highlight wrangling sub-node if it exists
            wrn_active = self._n(self.active_node, "wrn")
            if wrn_active in all_known:
                lines.append(f'class {wrn_active} activeNode')

        lines.append("%% Interactions")
        for mermaid_id, schema_id in _clickable:
            lines.append(f'click {mermaid_id} call mermaidClick("{schema_id}")')

        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    from utils.config_loader import ConfigManager

    parser = argparse.ArgumentParser(
        description="Generate a TubeMap (Mermaid) for a manifest.")
    parser.add_argument("manifest", help="Path to the manifest YAML")
    args = parser.parse_args()

    cm = ConfigManager(args.manifest)
    mapper = BlueprintMapper(cm.raw_config)
    print(mapper.generate_mermaid())

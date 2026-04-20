# libs/utils/src/utils/blueprint_mapper.py
import yaml
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
            # Truncate long info strings
            return info[:40] if len(info) > 40 else info
        elif isinstance(info, dict):
            return info.get("display_name", info.get("sub_category", info.get("title", node_id)))
        return details.get("description", node_id)[:40] if isinstance(
            details.get("description"), str) else node_id

    def _safe_node_id(self, raw_id: str) -> str:
        """Sanitize node IDs: replace spaces with underscores for Mermaid compatibility."""
        return raw_id.replace(" ", "_").replace("-", "_")

    def generate_mermaid(self) -> str:
        """
        Constructs a fully structure-aware Mermaid DAG of the project lineage.

        Node types:
          trunk  (blue)   — data_schemas sources
          ref    (grey)   — additional_datasets_schemas
          meta   (orange) — metadata_schema
          branch (purple) — assembly_manifests
          plot   (green)  — plots (flattened from analysis_groups by ConfigManager)
          info   (light blue) — placeholder when target_dataset is missing
        """
        self.nodes = []
        self.edges = []
        self.style_classes = []
        # All clickable node IDs (safe_schema_id strings) — populated below
        _clickable: list = []

        # Track all known node IDs for edge validation
        all_known: set = set()

        # ── 1. Data Schemas (blue trunk sources) ──────────────────────────────
        schemas = self.cfg.get("data_schemas", {})
        for sid, details in schemas.items():
            safe_id = self._safe_node_id(sid)
            label = self._get_label(sid, details)
            self.nodes.append(f'{safe_id}(["{label}\\nSource"])')
            self.style_classes.append(f'class {safe_id} trunk')
            all_known.add(safe_id)
            _clickable.append(safe_id)

        # ── 2. Additional Datasets (grey ref data) ────────────────────────────
        add_schemas = self.cfg.get("additional_datasets_schemas", {})
        for aid, details in add_schemas.items():
            safe_id = self._safe_node_id(aid)
            label = self._get_label(aid, details)
            self.nodes.append(f'{safe_id}(["{label}\\nRef Data"])')
            self.style_classes.append(f'class {safe_id} ref')
            all_known.add(safe_id)
            _clickable.append(safe_id)

        # ── 3. Metadata Schema (orange — single special node) ─────────────────
        meta = self.cfg.get("metadata_schema", {})
        if meta:
            self.nodes.append(
                'metadata_schema(["metadata_schema\\nMetadata"])')
            self.style_classes.append('class metadata_schema meta')
            all_known.add("metadata_schema")
            _clickable.append("metadata_schema")

        # ── 4. Assembly Manifests (purple branch junctions) ───────────────────
        assemblies = self.cfg.get("assembly_manifests", {})
        for asid, details in assemblies.items():
            safe_id = self._safe_node_id(asid)
            self.nodes.append(f'{safe_id}{{"{asid}\\nAssembly"}}')
            self.style_classes.append(f'class {safe_id} branch')
            all_known.add(safe_id)
            _clickable.append(safe_id)

            # Draw edges from each ingredient to the assembly
            ingredients = details.get(
                "ingredients", []) if isinstance(details, dict) else []
            for ing in ingredients:
                if isinstance(ing, dict):
                    parent_raw = ing.get("dataset_id", "")
                elif isinstance(ing, str):
                    parent_raw = ing
                else:
                    continue
                parent = self._safe_node_id(parent_raw)
                if parent in all_known:
                    self.edges.append(f'{parent} --> {safe_id}')
                # If parent not yet mapped (e.g., forward reference), still draw edge
                elif parent_raw:
                    self.edges.append(f'{parent} --> {safe_id}')

        # ── 5. Plots grouped by analysis_groups (green terminals) ─────────────
        # Use analysis_groups for group membership, flattened 'plots' for target_dataset
        analysis_groups = self.cfg.get("analysis_groups", {})
        # Flattened by ConfigManager with target_dataset
        plots_flat = self.cfg.get("plots", {})

        # Build group membership map: plot_id → group_name
        plot_to_group: dict = {}
        for group_name, group_spec in analysis_groups.items():
            if isinstance(group_spec, dict):
                for pid in group_spec.get("plots", {}).keys():
                    plot_to_group[pid] = group_name

        # Collect subgraph blocks (group_name → list of node defs)
        subgraphs: dict = {}

        for pid, pspec in plots_flat.items():
            safe_pid = self._safe_node_id(pid)
            label = pid.replace("_", " ").title()
            node_def = f'{safe_pid}[["{label}\\nPlot"]]'
            self.style_classes.append(f'class {safe_pid} plot')
            all_known.add(safe_pid)
            _clickable.append(safe_pid)

            # Assign to subgraph
            group_name = plot_to_group.get(pid, "Ungrouped")
            if group_name not in subgraphs:
                subgraphs[group_name] = []
            subgraphs[group_name].append(node_def)

            # Resolve parent via target_dataset
            target_raw = None
            if isinstance(pspec, dict):
                target_raw = pspec.get(
                    "target_dataset") or pspec.get("assembly_id")

            if target_raw:
                target = self._safe_node_id(target_raw)
                self.edges.append(f'{target} --> {safe_pid}')
            else:
                info_id = f"INFO_{safe_pid}"
                self.nodes.append(
                    f'{info_id}["ℹ️ {pid}\\nSet target_dataset\\nin plot spec"]'
                )
                self.style_classes.append(f"class {info_id} info")
                self.edges.append(f"{info_id} -.-> {safe_pid}")

        # ── Build final Mermaid string ─────────────────────────────────────────
        lines = [
            "graph LR",
            "%% Styling",
            "classDef trunk fill:#0d6efd,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef ref fill:#6c757d,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef meta fill:#fd7e14,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef branch fill:#9c27b0,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef plot fill:#198754,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef info fill:#e3f2fd,stroke:#1976d2,stroke-width:1px,color:#1a1a1a",
            "classDef activeNode stroke:#212529,stroke-width:4px,stroke-dasharray: 5 5",
            "%% Nodes"
        ]
        lines.extend(self.nodes)

        # Add subgraph sections for each analysis group
        for group_name, group_nodes in subgraphs.items():
            safe_group = self._safe_node_id(group_name)
            lines.append(f'subgraph {safe_group}["{group_name}"]')
            lines.extend(f'  {n}' for n in group_nodes)
            lines.append("end")

        lines.append("%% Edges")
        lines.extend(self.edges)
        lines.append("%% Classes")
        lines.extend(self.style_classes)

        # Highlight active node if set
        if self.active_node:
            safe_active = self._safe_node_id(self.active_node)
            lines.append(f'class {safe_active} activeNode')

        # [ADR-039] Interactivity — click any node to trigger mermaidClick bridge
        # _clickable includes all node types: trunk, ref, meta, branch, AND plot nodes
        # (plot nodes live in subgraphs and were excluded from self.nodes previously)
        lines.append("%% Interactions")
        for node_id in _clickable:
            lines.append(f'click {node_id} call mermaidClick("{node_id}")')

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

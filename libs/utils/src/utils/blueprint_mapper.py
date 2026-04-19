# libs/utils/src/utils/blueprint_mapper.py
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class BlueprintMapper:
    """
    [ADR-039] Generates a DAG-based 'TubeMap' visualization for SPARMVET manifests.
    Parses manifest lineage and outputs Mermaid.js code with high-density styling.
    """

    def __init__(self, raw_config: Dict):
        self.cfg = raw_config
        self.nodes = []
        self.edges = []
        self.style_classes = []

    def _get_label(self, node_id, details):
        """Safely extracts a display label from node details."""
        if not isinstance(details, dict):
            return node_id

        info = details.get("info", {})
        if isinstance(info, str):
            return info
        elif isinstance(info, dict):
            return info.get("display_name", info.get("title", node_id))

        # Fallback to description (Phase 18 convention)
        return details.get("description", node_id)

    def generate_mermaid(self) -> str:
        """Constructs a stylised Mermaid diagram of the project lineage."""
        self.nodes = []
        self.edges = []

        # 1. Map Data Schemas (The Sources / Tier 1)
        schemas = self.cfg.get("data_schemas", {})
        for sid, details in schemas.items():
            label = self._get_label(sid, details)
            self.nodes.append(f'{sid}(["<b>{label}</b><br/>Source"])')
            self.style_classes.append(f'class {sid} trunk')

        # 2. Map Additional Datasets
        add_schemas = self.cfg.get("additional_datasets_schemas", {})
        for aid, details in add_schemas.items():
            label = self._get_label(aid, details)
            self.nodes.append(f'{aid}(["<b>{label}</b><br/>Ref Data"])')
            self.style_classes.append(f'class {aid} trunk')

        # 3. Map Assemblies (The Junctions / Tier 2)
        assemblies = self.cfg.get("assembly_manifests", {})
        for asid, details in assemblies.items():
            label = self._get_label(asid, details)
            self.nodes.append(f'{asid}{{"<b>{asid}</b><br/>Assembly"}}')
            self.style_classes.append(f'class {asid} branch')

            # Map Incoming Ingredients
            ingredients = details.get("ingredients", [])
            for ing in ingredients:
                parent = ing.get("dataset_id")
                if parent:
                    self.edges.append(f'{parent} --> {asid}')

        # 4. Map Plots (The Terminals)
        plots = self.cfg.get("plots", {})
        for pid, details in plots.items():
            label = self._get_label(pid, details)
            self.nodes.append(f'{pid}[["{label}<br/>Plot"]]')
            self.style_classes.append(f'class {pid} plot')

            # Resolve parent: read target_dataset / assembly_id explicitly (Bug #3 fix)
            target = None
            if isinstance(details, dict):
                target = details.get(
                    "target_dataset") or details.get("assembly_id")

            if target and target in assemblies:
                self.edges.append(f'{target} --> {pid}')
            elif target and target in schemas:
                self.edges.append(f'{target} --> {pid}')
            else:
                # No structural link found — show informational node (not scary)
                info_id = f"INFO_{pid}"
                self.nodes.append(
                    f'{info_id}["ℹ️ {pid}<br/><small>Set target_dataset in plot spec<br/>to show lineage</small>"]'
                )
                self.style_classes.append(f"class {info_id} info")
                self.edges.append(f"{info_id} -.-> {pid}")

        # Build the final string
        lines = [
            "graph LR",
            "%% Styling",
            "classDef trunk fill:#0d6efd,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef branch fill:#9c27b0,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef plot fill:#198754,stroke:#fff,stroke-width:2px,color:#fff",
            "classDef info fill:#e3f2fd,stroke:#1976d2,stroke-width:1px,color:#1a1a1a,font-size:12px",
            "%% Nodes"
        ]
        lines.extend(self.nodes)
        lines.append("%% Edges")
        lines.extend(self.edges)
        lines.append("%% Classes")
        lines.extend(self.style_classes)

        # [ADR-039] Interactivity clicks
        lines.append("%% Interactions")
        for node_def in self.nodes:
            # Extract node_id from definitions like 'node_id(["label"])' or 'node_id{"label"}'
            node_id = node_def.split("(")[0].split("{")[0].split("[")[0]
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

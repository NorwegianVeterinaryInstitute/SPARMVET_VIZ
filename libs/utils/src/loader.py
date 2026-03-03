import yaml
from pathlib import Path

class DirectoryConfigLoader:
    def __init__(self, root_config_path: str):
        self.root = Path(root_config_path)

    def get_available_analyses(self):
        """
        Walks through the subdirectories. 
        Folder Name = Category. 
        YAML Name = Specific Analysis.
        """
        registry = {}

        # Look at every folder inside our root config path
        for category_dir in self.root.iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name.capitalize()
                registry[category_name] = []

                # Find all YAMLs in this specific category folder
                for yaml_file in category_dir.glob("*.yaml"):
                    # Ignore 'copy' files like saureus (2).yaml
                    if "(" in yaml_file.name: continue
                    
                    with open(yaml_file, "r") as f:
                        data = yaml.safe_load(f)
                        registry[category_name].append({
                            "id": yaml_file.stem,
                            "display_name": data.get("metadata", {}).get("display_name", yaml_file.stem),
                            "full_path": str(yaml_file)
                        })
        
        return registry
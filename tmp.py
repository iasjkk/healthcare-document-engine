from pathlib import Path

# Base directory
base_dir = Path("framework/core")

# Files to create
files = [
    "__init__.py",
    "base_component.py",
    "base_agent.py",
    "base_model.py",
    "base_node.py",
    "base_parser.py",
    "base_validator.py",
    "base_orchestrator.py",
    "base_storage.py",
    "types.py",
    "constants.py",
    "exceptions.py",
]

# Create directory
base_dir.mkdir(parents=True, exist_ok=True)

# Create files if they don't exist
for file_name in files:
    file_path = base_dir / file_name
    if not file_path.exists():
        file_path.touch()
        print(f"Created: {file_path}")
    else:
        print(f"Already exists: {file_path}")

print("\nFramework core structure is ready.")
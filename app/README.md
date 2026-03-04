## App structure 
.
├── app.py                 <-- THE BOOTSTRAP (Entry Point)
├── app/                   <-- THE PRESENTATION LAYER (UI & Orchestrator)
│   ├── __init__.py        # Makes the folder a package
│   ├── ui.py              # The Display & Interaction Layer
│   └── server.py          # The Orchestrator (Logic Layer)
├── libs/                  <-- THE ENGINE (Ingestion, Transformer, Viz)
│   ├── ingestion/
│   ├── transformer/
│   ├── utils/
│   └── viz_factory/
|
└── config/                <-- THE BRAIN (YAMLs)


## The "Import" Trap
The Risk: Since app.py is in the root and your logic is in app/, you need to be careful with how the scripts in app/ find your libs/.

The Strategy: Always use **Absolute Imports or ensure your PYTHONPATH includes the root directory**.

Example in server.py: from libs.transformer.src.clean_logicA import ...

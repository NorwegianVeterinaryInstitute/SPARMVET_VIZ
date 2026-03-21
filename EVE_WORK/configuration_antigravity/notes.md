Workspace Structure Definition:

.agents/: The "Instruction Layer" containing your persona (rules), custom tool definitions (skills), and multi-step automation logic (workflows).

.antigravity/: The "Execution & Memory Layer" where the IDE stores its operational data, including the local embeddings generated via your Ollama MCP and the active brain (context window cache).


# Restarting work from clean state 
## Initiation repository 
@Agent: Initialize workspace sync. 
1. Map conversation history to ./.antigravity/conversations/.
2. Confirm Cloud Embedding status (Default) is active for the Memory Bank.
3. Validate that .aiignore is preventing indexing of .venv and other noise.

close and start a new conversation - history was lost
@Agent: History Restoration Protocol.
1. Scan the directory ./.antigravity/conversations/ for all existing JSON/Markdown chat logs.
2. Re-index these files into the current session's "Past Conversations" sidebar.
3. Confirm that the 'Memory Bank' is pulling context from ./.antigravity/knowledge/ artifacts.

ask the agent to verify the paths it uses 
@Agent: Generate a 'Workspace Infrastructure Map' for my records. 
Please list every directory and file path you are currently using for data persistence, specifically identifying:

1. Storage Root: Confirm the absolute path for the workspace root.
2. Conversation History: Where are chat logs and summaries being written?
3. Memory Bank: Where are the vector embeddings and project knowledge (blockers/milestones) stored?
4. Logic & Rules: Where are you reading custom agent personas and workflows from?
5. Configuration: Which settings.json or .aiignore files are currently governing your behavior?

For each path, briefly explain its purpose so I can replicate this setup in other repositories.

## Plan, task and knowledge managenemt restoration. 

# Preparation of galaxy integration

## Tools to help dev and testing of the app and integration to galaxy

### Tools summary

| Component | Tool / Library | Purpose |
| --- | --- | --- |
| Tool Authoring | Planemo | The CLI tool for Galaxy developers. Use it to lint, test, and serve your tool locally without a full Galaxy install. |
| API Connector | BioBlend | The official Python library to talk to the Galaxy API. Perfect for your dashboard's "connector" logic. |
| Testing Server | Galaxy Docker | For a full test environment, the bgruening/galaxy-stable Docker image is the industry standard. |
| Test-Driven Dev | Pytest | Since you mentioned a TDD style, Planemo integrates with Pytest to run your tool's <tests> section automatically. |

### Tools Detail description

1. Planemo:

- Having Planemo on your workstation, you get several advantages for your TDD workflow:
- IDE Integration: The VS Code "Galaxy Tools" extension uses the Planemo executable on your host to provide real-time linting.
- Ephemeral Testing: You can run planemo serve to spin up a tiny, temporary Galaxy instance just for a 5-minute test without touching your "real" home server on the thinkpad.
- SDK Capabilities: Planemo can initialize new tool projects (planemo project_init) and auto-generate test files for your dashboard.

1. BioBlend (API communication with Galaxy  )

Tools wrappers

- Static wrapper (batch persona) - for pipeline visualisation
- Interactive persona -> Galaxy interactive tools (GxIT) - allows the dashboard to run as live container (Docker) Inside galaxy - Where user can interact with a persistent URL

Insteractive Tools (GxIT) - for real-time dashboard experience

### Setup / Installation

1. Install on velocifero

> Planemo

```bash
# 1. Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install Planemo as a global tool
uv tool install planemo

# 3. Verify the installation
planemo --version

# OR Install Planemo
pip install planemo

# Run your tool in a temporary Galaxy instance
planemo serve my_dashboard_wrapper.xml
```

## Galaxy server  

bgruening/galaxy-stable Docker image (or Planemo) allows you to simulate the exact environment of a production server.

To test history access and pipeline integration, you should focus on these three mechanisms:

1. Environment Variables:
Galaxy passes history information to the container via environment variables (like $GALAXY_URL and $API_KEY).
You can test if your "connector" properly picks these up to talk back to the API.

2. Data Mapping:
For Interactive Tools (GxIT), Galaxy maps history datasets into the container's file system (typically in ~/galaxy_inputs/). You can test your dashboard's ability to "see" and "read" these files without manual uploads.

3. BioBlend Integration:
Since you are writing a connector, you can use BioBlend within your dashboard to programmatically query the history, list datasets, and even trigger other tools in a pipeline.

### Testing against Existing Pipelines

- No need to run the whole pipeline every time.

- Mock Histories: Use Planemo or a Python script to pre-populate your Docker Galaxy history with "dummy" results that look like they came from a real pipeline.
The "Mock History" strategy:

1. Pre-seed the Test Data: Manually upload a small sample of the files your pipeline would produce (e.g., a .bam file, a .vcf, or a .tsv table) into your test Galaxy Docker instance.
2. Planemo Test Cases: In your tool wrapper's XML, you can write a test section that feeds these specific files into your app. This proves your app can "read" the history data without the pipeline actually existing.
3. API Simulation: If your connector is using BioBlend, you can point it at your local Docker Galaxy instance and use the API to "create" a history that looks exactly like a real one from UseGalaxy.eu.

Testing the "History Access" logic:
Since the dashboard needs to be a "connector" to the Galaxy API, you need to test if it can find the right files.
You can simulate the "Persona" scenarios like this:

| Persona | Simulation Strategy |
| --- | --- |
| Batch/Visualizer | Run the tool with a fixed dataset input. Verify the dashboard displays the static results correctly. |
| Interactive/Explorer | Use the Docker Galaxy to launch the app. Manually use the app's UI to ""browse"" the current history via the API. |

- Dataset Collections:
If your pipeline outputs a collection of files, ensure your wrapper handles the <collection> tag.
You can test this by creating a mock collection in your local Galaxy instance before launching the dashboard tool.

### Path to UseGalaxy.eu

- UseGalaxy.eu has a specific process for onboarding new Interactive Tools (GxIT) because they require specialized infrastructure (ingress, subdomains, and resource allocation).

| Step | Requirement |
| ---- | ----------- |
| Container | Must be published to a public registry like Quay.io or DockerHub.|
| Wrapper | Must be linted with planemo lint and include valid <tests>.|
| Submission | Open a Pull Request (PR) to the usegalaxy-eu/operations repository.|
| Persona Setup | You can define different entry points or environment variables in your PR to handle the "Visualization" vs. "Interactive" personas.|

### Comparison of Test Environments

| Feature | Planemo (planemo serve) | Full Docker Galaxy |
| --- | --- | --- |
| Setup Speed | Instant (ephemeral) | Slower (persistent) |
| API Testing | Basic | Complete (Full API support) |
| GxIT Support | Yes (recent versions) | Yes (Best for Interactive Tools) |
| Persona Testing | Harder to swap configs | Easier via multiple wrappers |

[The best way to run integration tests in your CI/CD pipeline](https://www.youtube.com/watch?v=YtF0rzIYgEk)

Summary Table: Planemo vs. Galaxy Docker

| Feature | Planemo (on Velocifero) | Galaxy Docker (on Thinkpad) |
| --- | --- | --- |
| Role | Developer SDK / CLI | Production-like Test Environment |
| Primary Use | "Linting, testing, & scaffolding" | Running the full API and pipelines |
| Persistence | None (ephemeral) | Full database & history |
| AI Integration | Works with VS Code agents | Target for API connectors |

### Recommended Test Architecture

To maintain your test-driven development (TDD) style on your Fedora machine, follow this hierarchy:

Level 1: Local Unit Tests: Test your dashboard logic (Antigravity) without any Galaxy involvement.

Level 2: Planemo Lint/Serve: Use planemo serve to check if your XML wrapper is valid and if the UI displays the app correctly.

Level 3: Docker Integration: Use the bgruening/galaxy-stable image to test the "Connector" logic (BioBlend) against a live API that contains your pre-uploaded test data.

### Direct Support for UseGalaxy.eu

The UseGalaxy.eu team provides a repository specifically for testing tools before they go live. You can even use their "staging" environment or a local minigalaxy setup to ensure compatibility.

## Setup test server

### alternative 1

1. The Network Logic
By using an SSH tunnel with port forwarding, you are effectively tricking the browser and your app's "connector" on your workstation into thinking the Galaxy server is running locally.

2. The Command:
From your velocifero PC:
ssh -L 8080:localhost:8080 user@thinkpad

Now, any request to <http://localhost:8080> on your workstation is forwarded to the Galaxy instance on your home server.

Why this works for Galaxy Testing?
API Consistency: Since your app's connector will be configured to talk to a Galaxy URL, using localhost:8080 via the tunnel means you don't have to change the configuration when you switch from a local Planemo test to your home server.

Interactive Tool Redirects: Galaxy Interactive Tools (GxIT) often use a proxy (like Nginx or Traefik).
If you are testing GxIT, you might need to forward multiple ports or use a "Wildcard" tunnel if your dashboard relies on Galaxy's dynamic subdomains.

Security: You don't need to open the thinkpad firewall to the whole network; the traffic stays encrypted within the SSH tunnel.

| Step | Action | Command/Detail |
| --- | --- | --- |
| 1. Server Setup | Run Galaxy on thinkpad | docker run -d -p 8080:80 bgruening/galaxy-stable |
| 2. Establish Tunnel | From velocifero | ssh -L 8080:localhost:8080 <user>@<thinkpad-ip> |
| 3. Verify | Open browser on velocifero | Navigate to <http://localhost:8080> |
| 4. TDD Workflow | Run tests/connector | Point your API base URL to <http://localhost:8080> |

Potential Gotcha: GxIT Proxying
If your "antigravity" dashboard runs as a Galaxy Interactive Tool, Galaxy usually generates a unique URL like https://<session-id>.interactivetool.galaxy.org.

The Problem: An SSH tunnel on a single port (8080) won't naturally handle these dynamic subdomains.

The Fix: For initial testing, you can configure Galaxy to use "Path-based" routing instead of "Subdomain-based" routing so that the dashboard lives at <http://localhost:8080/interactivetool/entry/path>.

### Alternative 2

 should we give all acess and work on the remote server then via IDE ?(antigravity/vs

## Addons for development (vscode / antigravity)

### Summary table

| Category | Extension Name | Description / Key Features |
| --- | --- | --- |
| **Galaxy Dev** | Galaxy Tools | XML validation against XSD, auto-completion of tags, documentation on hover, and IUC best-practice linting. |
| **Galaxy Dev** | Galaxy Workflows | Support for .ga and .gxwf.yml formats, syntax highlighting, workflow cleanup, and structural validation. |
| **Containers** | Dev Containers | Allows you to open your project inside the Docker container where your dashboard runs. Essential for debugging. |
| **Containers** | Docker | Manage your Galaxy Docker images and local containers (start/stop/logs) directly from the VS Code sidebar. |
| **Remote Access** | Remote - SSH | Connect to your thinkpad server and edit files on the server as if they were local. |
| **AI (Claude)** | Claude Dev / Cline | Agentic extension that can use your Claude API key to write code, run terminal commands, and create new test files autonomously. |
| **AI (Gemini)** | Gemini Code Assist | Google's official extension for deep Gemini integration. Excels at explaining complex tech and large-scale refactoring. |
| **Bioinformatics** | bioSyntax | Provides syntax highlighting for biological file formats (VCF, SAM, FASTA) that your dashboard will be processing. |

Top Tools for Docker Scaffolding & Orchestration

| Tool / App | Role in your Workflow | Why for you? |
| --- | --- | --- |
| Docker (Official Extension) | Scaffolding & Management | Use the command Docker: Add Docker Files to Workspace. It detects your app type and generates the Dockerfile and Compose files automatically. |
| Cline (Agentic Claude) | Recipe Generator | "You can prompt it: ""Based on my Fedora environment and this dashboard code, write a multi-stage Dockerfile."" It will write and save the files for you." |
| Docker DX | Best Practices | A newer extension that provides real-time linting for Dockerfiles, suggesting security fixes and build optimizations (BuildKit/Buildx). |
| Portainer | Visual Management | A web-based UI (installable via Docker) that lets you manage your ""thinkpad"" containers visually if you prefer not to use the CLI. |

### Details

1. Galaxy Tools Extension:

- Helps developers write the XML files that describe how a specific software (like BLAST or BWA) should interface with the Galaxy web UI.
- Validation: It checks your XML against the official Galaxy schema ($xsd$) in real-time, highlighting errors before you even try to upload the tool to a server.
- IntelliSense: It suggests the correct tags (e.g., <inputs>, <outputs>, <command>) and attributes based on the Galaxy IUC (Intergalactic Utilities Commission) standards.
- Documentation: Hovering over a tag shows the official documentation for that specific Galaxy XML element.

1. Galaxy Workflows Extension
This extension is geared toward "Workflow-as-Code." While many users build workflows using Galaxy’s web-based drag-and-drop canvas, power users often edit the underlying files directly.

Format Support: It handles both the legacy JSON-based .ga files and the newer YAML-based Format 2 workflows (.gxwf.yml).

Best Practices: It enforces standards to ensure workflows remain portable across different Galaxy instances.

## Deep integration strategy for AI agents

1. Claude (via "Cline" or "Claude Dev" Extension)
The Workflow: You can ask Claude: "Analyze this Galaxy tool XML and write a Python test file in tests/ that mocks a history dataset." * The Edge: Claude is currently superior at "Agentic" tasks—it can actually execute the planemo lint command in your terminal and fix the errors it finds without you typing a word.

2. Gemini (via "Gemini Code Assist")
The Workflow: Use Gemini to navigate the BioBlend documentation.

The Edge: Gemini has a massive context window. You can feed it your entire dashboard's codebase and ask, "Where should I implement the Galaxy API connector logic to stay consistent with the existing Antigravity architecture?"

**TDD Support: Since you use an incremental TDD style, ensure you also have the Python extension installed, which will automatically detect your tests/ directory**

1. "Agentic" Scaffolding with Claude (via Cline/Claude Dev)
Since you are using a TDD approach, you can give Claude an "agentic" instruction:

"Read my requirements.txt and package.json. Create a docker-compose.yml that mounts my local code for hot-reloading on port 8080 and links to a local Galaxy API container."
Result: It creates the files and even tests the docker-compose up command in your terminal.

1. Architecture Review with Gemini
Gemini is excellent at checking for "environment drift." You can share your docker-compose.yml and your Fedora 43 system specs:

"Review this Docker recipe for Fedora 43. Ensure the file permissions and X11 forwarding for the dashboard will work on my KDE desktop."
Result: It will catch common Linux-specific issues like GID/UID mismatches between the host and container.

Helpful Tip: Docker Compose "Models"
A new standard in 2026 allows you to define AI models directly inside your docker-compose.yml using the models top-level element. This is useful if your "antigravity" dashboard uses local LLMs for data analysis.


# Getting offline documentation

## Tool offline doc

- ZEAL: sudo dnf install zeal
- **Plotnine Context**: Zeal often uses the **Dash** docset repositories.
 
 - While Plotnine might not have a "Mainstream" docset, you can generate one from the HTML documentation using `doc2dash`. 
- **Usage for AI**: You can use **Repomix** on the _source code_ of Plotnine if you clone the repo, or use a scraper to turn their website into a single Markdown file for your context uploads.

```bash
sudo dnf install zeal

cd ~/Downloads
# Create a fresh venv named 'plotnine_build'
python3.14 -m venv plotnine_build
# Activate it
source plotnine_build/bin/activate
# Ensure pip is current
pip install --upgrade pip

# Install the core build and conversion tools
pip install sphinx quartodoc doc2dash qrenderer
# Install common Sphinx extensions that Plotnine often requires
pip install sphinx-copybutton numpydoc sphinx-design


pip install -r requirements/docs.txt
pip install -e .
# Go to where you cloned the plotnine repo (adjust path if needed)
cd ~/Downloads/plotnine
# Install in editable mode to ensure the doc builder sees the internal logic
pip install -e .
# Navigate to the doc folder and build
cd doc
# Try the legacy bypass first for highest success rate
export PLOTNINE_DOC_LEGACY=1
make clean
make html

## 

pip install doc2dash
pip install 'plotnine[doc]'
pip install qrenderer

git clone https://github.com/has2k1/plotnine.git
cd plotnine/requirements
pip install -r doc.txt
cd ../plotnine/doc
pip install quartodoc
pip install "griffe>=1.7.3"



export PLOTNINE_DOC_LEGACY=1
make clean
make html

```

Stoped ! 

 
```bash 



```


### 2. Strategy for Uploading Plotnine Context

To provide the Agent with the "Artist" logic without wasting quota on repetitive web searches, you should create a **Technical Reference Log** in `./.antigravity/knowledge/`.

1. **Scrape to Markdown**: Use a tool like `r-lib/downlit` or a simple python crawler to convert the [Plotnine Reference Page](https://plotnine.org/reference/) into a single `.md` file.
    
2. **Repomix the Docs**: If you have the Plotnine HTML docs offline, run **Repomix** on the documentation folder to create a compressed context file.
    
3. **The "Artist" KI**: Save this as `./.antigravity/knowledge/ki_plotnine_api.md`.
4. 
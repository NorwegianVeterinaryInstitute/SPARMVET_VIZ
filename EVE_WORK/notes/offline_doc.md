
# Getting offline documentation

## Tool offline doc

- ZEAL: sudo dnf install zeal
- **Plotnine Context**: Zeal often uses the **Dash** docset repositories. While Plotnine might not have a "Mainstream" docset, you can generate one from the HTML documentation using `doc2dash`. pip install doc2dash
- **Usage for AI**: You can use **Repomix** on the _source code_ of Plotnine if you clone the repo, or use a scraper to turn their website into a single Markdown file for your context uploads.

```bash
pip install doc2dash
pip install 'plotnine[doc]'

cd Download
git clone https://github.com/has2k1/plotnine.git
cd plotnine/doc

```

### 2. Strategy for Uploading Plotnine Context

To provide the Agent with the "Artist" logic without wasting quota on repetitive web searches, you should create a **Technical Reference Log** in `./.antigravity/knowledge/`.

1. **Scrape to Markdown**: Use a tool like `r-lib/downlit` or a simple python crawler to convert the [Plotnine Reference Page](https://plotnine.org/reference/) into a single `.md` file.
    
2. **Repomix the Docs**: If you have the Plotnine HTML docs offline, run **Repomix** on the documentation folder to create a compressed context file.
    
3. **The "Artist" KI**: Save this as `./.antigravity/knowledge/ki_plotnine_api.md`.
4. 
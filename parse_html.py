import re

html_path = r"C:\Users\User\.gemini\antigravity\brain\76def6fb-2d43-4a22-b74c-245e7385debf\.system_generated\steps\6\content.md"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's find links to files in the repository.
# On GitHub, file links are typically of the form:
# /mathruffian-dot/clasp-netlify-mcp-guide/blob/main/FILENAME or similar
# Or in HTML structure: href="/mathruffian-dot/clasp-netlify-mcp-guide/blob/main/..."
matches = re.findall(r'href="/mathruffian-dot/clasp-netlify-mcp-guide/blob/main/([^"]+)"', content)
print("File links found in main branch:")
for m in sorted(list(set(matches))):
    print(m)

# Also let's search for "tree" links to see if there are folders:
tree_matches = re.findall(r'href="/mathruffian-dot/clasp-netlify-mcp-guide/tree/main/([^"]+)"', content)
print("\nFolder links found in main branch:")
for m in sorted(list(set(tree_matches))):
    print(m)

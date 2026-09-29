import re

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "r", encoding="utf-8") as f:
    html = f.read()

bg_html = """<div class="bg-layer bg-grid"></div>
<div class="bg-layer bg-glow"></div>
"""

css_html = """
/* Background Animation Layers */
.bg-layer { position: fixed; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: -1; }
.bg-grid {
  background-image: linear-gradient(to right, rgba(45,217,232,0.03) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(45,217,232,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: bgScroll 40s linear infinite;
}
.bg-glow {
  background: radial-gradient(circle at 50% 50%, rgba(139,107,240,0.02) 0%, transparent 60%);
  animation: pulseGlow 10s ease-in-out infinite alternate;
}
@keyframes bgScroll { from { background-position: 0 0; } to { background-position: -400px -400px; } }
@keyframes pulseGlow { from { transform: scale(1); opacity: 0.5; } to { transform: scale(1.5); opacity: 1; } }
"""

# Insert HTML right after <body data-theme="dark">
html = html.replace('<body data-theme="dark">', '<body data-theme="dark">\n' + bg_html)

# Insert CSS right after <style>
html = html.replace('<style>', '<style>\n' + css_html)

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "w", encoding="utf-8") as f:
    f.write(html)

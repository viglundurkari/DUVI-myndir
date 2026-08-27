from pathlib import Path

root = Path(__file__).resolve().parent
folders = [
    ("myndir-dua", "Myndir Dúa"),
    ("myndir-villi", "Myndir Villi"),
]

allowed = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"}

def escape_js_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

images = []
for folder_name, label in folders:
    folder = root / folder_name
    if not folder.exists():
        continue
    for file in sorted(folder.iterdir()):
        if file.is_file() and file.suffix.lower() in allowed:
            images.append(
                {
                    "folder": folder_name,
                    "label": label,
                    "src": f"{folder_name}/{file.name}",
                    "name": file.name,
                }
            )

js_lines = ["const gallery = ["]
for item in images:
    js_lines.append(
        "  {"
        f" folder: \"{escape_js_string(item['folder'])}\","
        f" label: \"{escape_js_string(item['label'])}\","
        f" src: \"{escape_js_string(item['src'])}\"," 
        f" name: \"{escape_js_string(item['name'])}\""
        " },"
    )
js_lines.append("];")

js_block = "\n".join(js_lines)

html = f"""<!DOCTYPE html>
<html lang="is">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Myndir Gallery</title>
    <style>
      :root {{
        --bg: #0b1020;
        --bg-2: #111827;
        --panel: rgba(17, 24, 39, 0.7);
        --panel-strong: rgba(15, 23, 42, 0.9);
        --text: #e5eefb;
        --muted: #a4b3cc;
        --accent: #7dd3fc;
        --accent-2: #c084fc;
        --shadow: rgba(15, 23, 42, 0.7);
      }}

      * {{ box-sizing: border-box; }}

      html {{ scroll-behavior: smooth; }}

      body {{
        margin: 0;
        font-family: Inter, "Segoe UI", sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top, rgba(124, 58, 237, 0.28), transparent 28%),
          radial-gradient(circle at bottom right, rgba(34, 211, 238, 0.18), transparent 22%),
          linear-gradient(160deg, var(--bg) 0%, var(--bg-2) 100%);
        min-height: 100vh;
      }}

      .page {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 48px 20px 80px;
      }}

      .topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-bottom: 28px;
        flex-wrap: wrap;
      }}

      .brand {{
        font-size: clamp(1.8rem, 4vw, 3rem);
        font-weight: 800;
        letter-spacing: -0.06em;
        margin: 0;
      }}

      .brand span {{
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
      }}

      .filter-bar {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
      }}

      button.filter-btn {{
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(148, 163, 184, 0.08);
        color: var(--text);
        padding: 10px 16px;
        border-radius: 999px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.2s ease;
      }}

      button.filter-btn:hover, button.filter-btn.active {{
        background: linear-gradient(135deg, rgba(125, 211, 252, 0.2), rgba(192, 132, 252, 0.25));
        border-color: rgba(125, 211, 252, 0.5);
        transform: translateY(-1px);
      }}

      .gallery-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
      }}

      .card {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 45px var(--shadow);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
      }}

      .card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 28px 60px rgba(15, 23, 42, 0.9);
        border-color: rgba(125, 211, 252, 0.3);
      }}

      .card img {{
        display: block;
        width: 100%;
        height: 280px;
        object-fit: cover;
        background: #0f172a;
      }}

      .card-meta {{
        padding: 14px 16px 18px;
      }}

      .card-meta .folder {{
        display: inline-block;
        font-size: 0.71rem;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 8px;
        font-weight: 700;
      }}

      .card-meta .name {{
        margin: 0;
        font-size: 0.96rem;
        line-height: 1.4;
        color: var(--text);
        word-break: break-word;
      }}

      .empty {{
        padding: 36px 18px;
        text-align: center;
        color: var(--muted);
        border: 1px dashed rgba(255,255,255,0.14);
        border-radius: 18px;
        background: rgba(15, 23, 42, 0.4);
      }}

      @media (max-width: 620px) {{
        .page {{
          padding-top: 28px;
        }}

        .card img {{
          height: 240px;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="page">
      <header class="topbar">
        <h1 class="brand"><span>Myndir</span> gallery</h1>
        <div class="filter-bar" id="filters"></div>
      </header>

      <main class="gallery-grid" id="gallery"></main>
    </div>

    <script>
      {js_block}

      const galleryEl = document.getElementById('gallery');
      const filtersEl = document.getElementById('filters');
      const filterOptions = [
        {{ value: 'all', label: 'Allar myndir' }},
        {{ value: 'myndir-dua', label: 'Myndir Dúa' }},
        {{ value: 'myndir-villi', label: 'Myndir Villi' }}
      ];

      const createButtons = () => {{
        filterOptions.forEach((option) => {{
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'filter-btn active';
          if (option.value !== 'all') {{
            btn.classList.remove('active');
          }}
          btn.textContent = option.label;
          btn.dataset.filter = option.value;
          btn.addEventListener('click', () => {{
            document.querySelectorAll('.filter-btn').forEach((b) => b.classList.toggle('active', b === btn));
            renderGallery(option.value);
          }});
          filtersEl.appendChild(btn);
        }});
      }};

      const renderGallery = (filter = 'all') => {{
        const filtered = filter === 'all'
          ? gallery
          : gallery.filter((item) => item.folder === filter);

        galleryEl.innerHTML = '';

        if (!filtered.length) {{
          galleryEl.innerHTML = '<div class="empty">Engar myndir fundust í þessari möppu.</div>';
          return;
        }}

        filtered.forEach((item) => {{
          const card = document.createElement('article');
          card.className = 'card';
          card.innerHTML = `
            <img src="${{item.src}}" alt="${{item.name}}" loading="lazy" />
            <div class="card-meta">
              <span class="folder">${{item.label}}</span>
              <p class="name">${{item.name}}</p>
            </div>
          `;
          galleryEl.appendChild(card);
        }});
      }};

      createButtons();
      renderGallery();
    </script>
  </body>
</html>
"""

index_path = root / "index.html"
index_path.write_text(html, encoding="utf-8")
print(f"Generated {len(images)} images into {index_path}")

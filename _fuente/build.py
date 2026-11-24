#!/usr/bin/env python3
"""Genera el sitio estático del blog a partir de posts.json.
Uso desde la raíz del repo: python3 _fuente/build.py https://juanangelrivadeneira.github.io .
"""
import json, sys, re, os, shutil, html
from datetime import date

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://USUARIO.github.io").rstrip("/")
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SRC, "out")
AUTOR = "Juan Angel Riva de Neira"
SITIO = "Juan Angel Riva de Neira | HSSE en Oil & Gas y Minería"
LINKEDIN = "https://www.linkedin.com/in/juan-angel-riva-de-neira-060b7a46"
DESC = "Notas de campo sobre seguridad, salud y ambiente en Oil & Gas y Minería, por Juan Angel Riva de Neira."
MES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

posts = sorted(json.load(open(os.path.join(SRC, "posts.json"))), key=lambda p: p["fecha"], reverse=True)
scene = open(os.path.join(SRC, "scene.svg.html")).read()
e = html.escape

def fmt(d):
    y, m, dd = map(int, d.split("-"))
    return f"{dd} de {MES[m-1]} de {y}"

def mins(p):
    return max(2, round(len(re.sub(r"<[^>]+>", " ", p["cuerpo"]).split()) / 200))

def head(title, desc, url, extra=""):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{AUTOR}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="es_AR">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="{e(SITIO)}" href="{BASE}/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{extra}
</head>
<body>
<header class="band top">
  <div class="bar">
    <a class="mark" href="/">{AUTOR}</a>
    <nav aria-label="Principal"><a href="/#articulos">Artículos</a><a href="/#sobre-mi">Sobre mí</a></nav>
  </div>"""

FOOT = f"""<footer class="band">
  <div class="wrap">
    <p>© 2026 Juan Angel Riva de Neira. Las opiniones de este blog son personales y no representan a ninguna empresa.</p>
    <p>Nuevos artículos martes y viernes. <a href="{LINKEDIN}" rel="me">LinkedIn</a> · <a href="/feed.xml">RSS</a></p>
  </div>
</footer>
"""

def meta(p):
    return f'<span class="tag">{e(p["tema"])}</span><span>{fmt(p["fecha"])}</span><span>{mins(p)} min de lectura</span>'

def home():
    f = posts[0]
    temas = ["Todos"] + list(dict.fromkeys(p["tema"] for p in posts))
    chips = "".join(f'<button class="chip" type="button" aria-pressed="{str(t=="Todos").lower()}" data-t="{e(t)}">{e(t)}</button>' for t in temas)
    rows = "".join(f'<li data-t="{e(p["tema"])}"><a class="row" href="/articulos/{p["slug"]}/"><span class="when">{fmt(p["fecha"])}</span><span><span class="tag">{e(p["tema"])}</span><h2 style="margin:8px 0 0;font-size:22px;line-height:1.2;font-weight:700;letter-spacing:-.01em">{e(p["titulo"])}</h2><p>{e(p["resumen"])}</p></span><span class="mins">{mins(p)} min</span></a></li>' for p in posts)
    ld = json.dumps({"@context":"https://schema.org","@type":"Blog","name":SITIO,"url":BASE+"/","author":{"@type":"Person","name":AUTOR,"sameAs":[LINKEDIN],"jobTitle":"Gerente HSSE","knowsAbout":["Seguridad e Higiene","Oil & Gas","Minería","Ambiente"]}}, ensure_ascii=False)
    return head(SITIO, DESC, BASE + "/", f'<script type="application/ld+json">{ld}</script>') + f"""
  <div class="hero">
    <h1>Seguridad, salud y ambiente en Oil&nbsp;&amp;&nbsp;Gas y Minería</h1>
    <p class="lede">Notas de campo de un profesional HSSE con más de 15 años en yacimientos y minería de altura. Artículos nuevos cada martes y viernes.</p>
  </div>
  {scene}
</header>
<main>
  <section class="band" id="articulos" aria-label="Artículos">
    <div class="wrap">
      <a class="feat" href="/articulos/{f["slug"]}/"><div><div class="meta"><span>Último artículo</span>{meta(f)}</div><h3>{e(f["titulo"])}</h3></div><p>{e(f["resumen"])}</p></a>
      <div class="tools">
        <div id="chips" style="display:flex;flex-wrap:wrap;gap:8px" role="group" aria-label="Filtrar por tema">{chips}</div>
        <label class="search"><span hidden>Buscar</span><input id="q" type="search" placeholder="Buscar en el blog" autocomplete="off"></label>
      </div>
      <ul class="list" id="list">{rows}</ul>
      <p class="empty" id="empty" hidden>No hay artículos que coincidan con la búsqueda.</p>
    </div>
  </section>
  <section class="band about" id="sobre-mi">
    <div class="wrap agrid">
      <div>
        <h2>Sobre mí</h2>
        <p>Soy Juan Angel Riva de Neira, Licenciado en Seguridad e Higiene, con más de 15 años de trabajo en operaciones upstream de petróleo y gas y en minería. Hoy lidero la gestión de seguridad, salud, ambiente y seguridad patrimonial de una operadora de hidrocarburos con activos en varias provincias argentinas, con reporte directo a la dirección.</p>
        <p>Pasé por perforación, workover, producción y por un proyecto de litio a gran altura en la Puna. De esos años me quedó una convicción: la seguridad que funciona es la que se entiende en campo, no la que luce en una auditoría.</p>
        <p>En este blog comparto lo que aprendí, lo que todavía me cuestiono y lo que creo que la industria tiene que cambiar.</p>
        <p><a class="btn" style="display:inline-flex;align-items:center;text-decoration:none" href="{LINKEDIN}" rel="me">Conectá conmigo en LinkedIn</a></p>
      </div>
      <ul class="facts">
        <li><b>+15</b><span>años en upstream de oil &amp; gas y minería</span></li>
        <li><b>5</b><span>unidades de negocio bajo gestión, en distintas provincias</span></li>
        <li><b>HSSE</b><span>Seguridad, salud, ambiente y seguridad patrimonial</span></li>
        <li><b>Lic.</b><span>en Seguridad e Higiene, con título habilitante</span></li>
      </ul>
    </div>
  </section>
</main>
{FOOT}<script>
{{
let t="Todos";
const q=document.getElementById("q"),items=[...document.querySelectorAll("#list li")];
function f(){{const s=q.value.trim().toLowerCase();let n=0;for(const li of items){{const ok=(t==="Todos"||li.dataset.t===t)&&(!s||li.textContent.toLowerCase().includes(s));li.hidden=!ok;if(ok)n++}}document.getElementById("empty").hidden=n>0}}
document.getElementById("chips").addEventListener("click",ev=>{{const b=ev.target.closest(".chip");if(!b)return;t=b.dataset.t;for(const c of document.querySelectorAll(".chip"))c.setAttribute("aria-pressed",c===b);f()}});
q.addEventListener("input",f);
}}
</script>
</body>
</html>"""

def article(i, p):
    url = f"{BASE}/articulos/{p['slug']}/"
    prev = posts[i+1] if i + 1 < len(posts) else None
    nxt = posts[i-1] if i > 0 else None
    ld = json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":p["titulo"],"description":p["resumen"],"datePublished":p["fecha"],"dateModified":p["fecha"],"inLanguage":"es-AR","author":{"@type":"Person","name":AUTOR,"url":BASE+"/#sobre-mi","sameAs":[LINKEDIN]},"mainEntityOfPage":url,"articleSection":p["tema"]}, ensure_ascii=False)
    pn = (f'<a href="/articulos/{prev["slug"]}/"><span>Anterior</span>{e(prev["titulo"])}</a>' if prev else "<span></span>") + \
         (f'<a href="/articulos/{nxt["slug"]}/"><span>Siguiente</span>{e(nxt["titulo"])}</a>' if nxt else "<span></span>")
    return head(f'{p["titulo"]} | {AUTOR}', p["resumen"], url,
                f'<meta property="og:type" content="article"><meta property="article:published_time" content="{p["fecha"]}"><script type="application/ld+json">{ld}</script>') + f"""
</header>
<main class="band">
  <article class="post">
    <a class="back" href="/#articulos">← Todos los artículos</a>
    <div class="meta" style="border:0;margin:0;padding:0">{meta(p)}</div>
    <h1>{e(p["titulo"])}</h1>
    <div class="meta"><span>Por {AUTOR}</span></div>
    <div class="body">{p["cuerpo"]}</div>
    <p class="share"><a class="btn" style="display:inline-flex;align-items:center;text-decoration:none" href="{LINKEDIN}" rel="me">Seguime en LinkedIn</a></p>
    <nav class="pn" aria-label="Más artículos">{pn}</nav>
  </article>
</main>
{FOOT}</body>
</html>"""

def build():
    os.makedirs(OUT, exist_ok=True)
    shutil.rmtree(os.path.join(OUT, "articulos"), ignore_errors=True)
    shutil.copy(os.path.join(SRC, "styles.css"), OUT)
    if os.path.abspath(OUT) != os.path.abspath(os.path.dirname(SRC)) or not os.path.exists(os.path.join(OUT, "og.png")):
        shutil.copy(os.path.join(SRC, "og.png"), OUT)
    open(os.path.join(OUT, "index.html"), "w").write(home())
    for i, p in enumerate(posts):
        d = os.path.join(OUT, "articulos", p["slug"])
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(article(i, p))
    urls = [(BASE + "/", posts[0]["fecha"])] + [(f"{BASE}/articulos/{p['slug']}/", p["fecha"]) for p in posts]
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    items = "".join(f"<item><title>{e(p['titulo'])}</title><link>{BASE}/articulos/{p['slug']}/</link><guid>{BASE}/articulos/{p['slug']}/</guid><pubDate>{date.fromisoformat(p['fecha']).strftime('%a, %d %b %Y')} 09:00:00 -0300</pubDate><description>{e(p['resumen'])}</description></item>" for p in posts)
    open(os.path.join(OUT, "feed.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{e(SITIO)}</title><link>{BASE}/</link><description>{e(DESC)}</description><language>es-ar</language>{items}</channel></rss>')
    open(os.path.join(OUT, "404.html"), "w").write(head("Página no encontrada", DESC, BASE + "/") + '\n</header><main class="band"><div class="post"><h1>Esta página no existe</h1><p><a href="/">Volver al inicio</a></p></div></main>' + FOOT + "</body></html>")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print("OK:", len(posts), "artículos ->", OUT)

build()

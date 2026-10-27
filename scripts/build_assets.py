import os, sys, json, glob, random, math
ROOT = sys.argv[1]
out = os.path.join(ROOT, "assets")
os.makedirs(out, exist_ok=True)
for f in glob.glob(f"{out}/*.svg"): os.remove(f)
ICONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json")))

# Emerald on obsidian: one accent hue and its tints (names kept from the earlier neon pass)
BG, PANEL, PANEL2 = "#040706", "#09100d", "#122019"
TEXT, MUTED, FAINT = "#ecf6f1", "#8aa69a", "#48605a"
LIME, PINK, CYAN, VIOLET = "#e6fff4", "#00e59b", "#7dffcf", "#0a8f63"
HEAVY = "'Geist','Helvetica Neue',Helvetica,Arial,sans-serif"
SANS = "'Geist','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'Geist Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# SVGs shown through <img> can't fetch web fonts, so Geist is embedded as a data URI.
import base64
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def _face(family, file):
  b64 = base64.b64encode(open(os.path.join(FONT_DIR, file), "rb").read()).decode()
  return f"@font-face{{font-family:'{family}';font-weight:100 900;src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
FONTS = _face("Geist", "Geist-latin.woff2") + _face("Geist Mono", "GeistMono-latin.woff2")

BASE = f"""
.heavy{{font-family:{HEAVY};font-weight:700;letter-spacing:-.045em}}
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.pulse{{animation:pulse 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.45;transform:scale(1.35)}}}}
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.pop{{animation:pop 1s cubic-bezier(.22,1,.36,1) backwards}}
@keyframes pop{{from{{opacity:0;transform:translateY(14px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""
def svg(w, h, label, body, css=""):
  return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
          f'<style>{FONTS}{BASE}{css}</style>{body}</svg>')

def grad_defs(gid, spin=False, dur=6):
  """Hairline border gradient: accent fading into a faint edge; optionally rotating (SMIL)."""
  anim = (f'<animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="{dur}s" repeatCount="indefinite"/>' if spin else "")
  return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
          f'<stop offset="0" stop-color="{PINK}"/><stop offset=".3" stop-color="{TEXT}" stop-opacity=".08"/><stop offset=".7" stop-color="{TEXT}" stop-opacity=".08"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".6"/>{anim}</linearGradient>')

GLOW = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
SCAN = f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity="0"/></pattern>'

def frame(W, H, gid="bd", r=22):
  return (f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{r}" fill="{PANEL}"/>'
          f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{r}" fill="url(#scan)"/>'
          f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{r}" fill="none" stroke="url(#{gid})" stroke-width="1.5"/>')

# ---------------- HERO ----------------
def hero():
  W, H = 1200, 600
  random.seed(11)
  # neural net on the right
  layers = [4, 6, 6, 3]
  xs = [850, 940, 1030, 1120]
  nodes = []
  for li, n in enumerate(layers):
    top = 300 - (n - 1) * 35
    nodes.append([(xs[li], top + k * 70) for k in range(n)])
  edges, sig = "", ""
  cols = [CYAN, PINK, PINK, CYAN]
  for li in range(len(layers) - 1):
    for a in nodes[li]:
      for b in nodes[li + 1]:
        edges += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{TEXT}" stroke-opacity=".07"/>'
        if random.random() < .45:
          L = math.dist(a, b); c = random.choice(cols); d = round(random.uniform(1.2, 2.6), 2); dl = round(random.uniform(0, 3), 2)
          sig += (f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="2" stroke-linecap="round" '
                  f'stroke-dasharray="14 {int(L)+40}" filter="url(#glow)" class="sig" style="--L:{int(L)+54}px;animation-duration:{d}s;animation-delay:-{dl}s"/>')
  nd = ""
  for li, layer in enumerate(nodes):
    for (x, y) in layer:
      c = cols[li]
      nd += (f'<circle cx="{x}" cy="{y}" r="11" fill="{PANEL}" stroke="{c}" stroke-width="2"/>'
             f'<circle cx="{x}" cy="{y}" r="4" fill="{c}" class="pulse" style="animation-delay:-{round(random.uniform(0,2),2)}s" filter="url(#glow)"/>')
  # drifting colour blobs
  blobs = "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".35" class="blob" style="animation-duration:{d}s;animation-delay:-{dl}s"/>'
    for x, y, r, c, d, dl in [(960, 200, 200, VIOLET, 18, 0), (1060, 470, 150, PINK, 22, 6)])
  name = "ESSA SHAH"
  nx, ny, fs = 58, 300, 112
  def chips(items, x0, y, delay0):
    out, x = "", x0
    for k, (label, hot) in enumerate(items):
      w = round(len(label.replace("&amp;", "&")) * 9.4 + 34)
      out += (f'<g class="pop" style="animation-delay:{delay0 + k*.08:.2f}s">'
              f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="19" fill="{PINK if hot else PANEL2}" fill-opacity="{.14 if hot else .7}" stroke="{PINK if hot else TEXT}" stroke-opacity="{.7 if hot else .14}"/>'
              f'<text x="{x + w/2}" y="{y+24}" text-anchor="middle" class="mono" font-size="14" letter-spacing="1" fill="{PINK if hot else TEXT}">{label}</text></g>')
      x += w + 12
    return out
  skills = (chips([("DEEP LEARNING", True), ("COMPUTER VISION", True), ("NLP &amp; LLMs", True), ("RAG · AWS BEDROCK", False)], 62, 384, .2)
            + chips([("CLASSICAL ML", False), ("MODEL DEPLOYMENT", False), ("FULL-STACK", False)], 62, 432, .5))
  hud = (f'<g stroke="{TEXT}" stroke-opacity=".25" stroke-width="1.5" fill="none">'
         f'<path d="M30 60 V30 H60"/><path d="M{W-60} 30 H{W-30} V60"/><path d="M30 {H-60} V{H-30} H60"/><path d="M{W-60} {H-30} H{W-30} V{H-60}"/></g>')
  css = f"""
.sig{{animation:flow 2s linear infinite}}
@keyframes flow{{from{{stroke-dashoffset:var(--L)}}to{{stroke-dashoffset:0}}}}
.blob{{animation:drift 16s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}}
@keyframes drift{{0%{{transform:translate(0,0) scale(1)}}50%{{transform:translate(-60px,40px) scale(1.2)}}100%{{transform:translate(40px,-30px) scale(.9)}}}}
.sweep{{animation:sweep 5s linear infinite}}
@keyframes sweep{{from{{transform:translateY(-80px)}}to{{transform:translateY({H}px)}}}}
"""
  body = f"""<defs>{grad_defs("bd", dur=8)}{GLOW}{SCAN}
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<filter id="noise"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .06 0"/></filter>
<clipPath id="c"><rect x="3" y="3" width="{W-6}" height="{H-6}" rx="20"/></clipPath>
<linearGradient id="sw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".12"/></linearGradient>
</defs>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="{BG}"/>
<g clip-path="url(#c)">
  <g filter="url(#blur)">{blobs}</g>
  <rect width="{W}" height="{H}" filter="url(#noise)"/>
  <rect width="{W}" height="{H}" fill="url(#scan)"/>
  {edges}{sig}{nd}
  <rect class="sweep" x="0" y="0" width="{W}" height="80" fill="url(#sw)"/>
</g>
{hud}
<text x="70" y="88" class="mono" font-size="14" fill="{PINK}" letter-spacing="3">● ONLINE</text>
<text x="200" y="88" class="mono" font-size="14" fill="{FAINT}" letter-spacing="3">// ML · CV · NLP · GENAI · FULL-STACK</text>
<text x="{W-70}" y="88" text-anchor="end" class="mono" font-size="14" fill="{FAINT}" letter-spacing="3">51.7°N 0.5°E — ESSEX, UK</text>
<text x="62" y="186" class="mono" font-size="22" fill="{MUTED}">$ ./essa --profile</text>
<text x="{nx}" y="{ny}" class="heavy" font-size="{fs}" fill="{TEXT}">{name}</text>
<text x="62" y="350" class="mono" font-size="19" fill="{MUTED}" letter-spacing="3">FULL-STACK SOFTWARE ENGINEER <tspan fill="{FAINT}">·</tspan> <tspan fill="{PINK}">AI/ML DEVELOPER</tspan></text>
{skills}
<g class="pop" style="animation-delay:.8s">
  <rect x="62" y="500" width="262" height="40" rx="20" fill="none" stroke="{FAINT}" stroke-width="1.5"/>
  <circle class="pulse" cx="86" cy="520" r="5" fill="{PINK}" filter="url(#glow)"/>
  <text x="102" y="525" class="mono" font-size="14" fill="{TEXT}">open to opportunities</text>
  <rect x="336" y="500" width="420" height="40" rx="20" fill="{PINK}" fill-opacity=".1" stroke="{PINK}" stroke-opacity=".45" stroke-width="1.5"/>
  <text x="546" y="525" text-anchor="middle" class="mono" font-size="14" fill="{TEXT}">BSc COMPUTING · <tspan fill="{PINK}">FIRST CLASS</tspan> · BIRKBECK</text>
</g>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="none" stroke="url(#bd)" stroke-width="1.5"/>
"""
  return svg(W, H, "ESSA SHAH — Full-stack software engineer and AI/ML developer. Deep learning, computer vision, NLP and LLMs, RAG on AWS Bedrock, classical ML, model deployment. BSc Computing, First Class, Birkbeck.", body, css)

# ---------------- SECTION HEADER ----------------
def section(idx, label, aside):
  W, H = 1200, 90
  css = f""".bar{{animation:bar 2.6s ease-in-out infinite}}
@keyframes bar{{0%{{transform:translateX(-300px)}}100%{{transform:translateX({W}px)}}}}
.gl{{opacity:0;animation:g 4s steps(1) infinite}}
@keyframes g{{0%,80%,100%{{opacity:0;transform:none}}82%{{opacity:1;transform:translate(-4px,0)}}85%{{opacity:1;transform:translate(4px,0)}}88%{{opacity:0}}}}"""
  L = label.upper()
  body = (f'<defs>{grad_defs("bd", spin=False)}{GLOW}{SCAN}<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
          f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{PINK}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></linearGradient></defs>'
          f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{PANEL}"/><rect width="{W}" height="{H}" fill="url(#scan)"/>'
          f'<rect x="0" y="{H-3}" width="{W}" height="3" fill="{PANEL2}"/>'
          f'<rect class="bar" x="0" y="{H-4}" width="300" height="4" fill="url(#bar)" filter="url(#glow)"/></g>'
          f'<text x="28" y="56" class="mono" font-size="20" fill="{PINK}">{idx}</text>'
          f'<text x="72" y="58" class="heavy" font-size="34" fill="{TEXT}">{L}<tspan dx="8" fill="{PINK}" class="blink">_</tspan></text>'
          f'<text x="{W-28}" y="56" text-anchor="end" class="mono" font-size="15" fill="{FAINT}" letter-spacing="2">// {aside}</text>')
  return svg(W, H, f"{idx} {label}", body, css)

# ---------------- MARQUEE ----------------
TOOLS = [("Python","Python","#4B8BBE"),("PyTorch","Pytorch","#EE4C2C"),("TensorFlow","Tensorflow","#FF6F00"),("Keras","Keras","#D00000"),
         ("scikit-learn","Scikitlearn","#F7931E"),("OpenCV","Opencv","#6E5BFF"),("Pandas","Pandas",TEXT),("NumPy","Numpy","#4DABCF"),
         ("Streamlit","Streamlit","#FF4B4B"),("AWS","Amazonaws","#FF9900"),("Google Cloud","Googlecloud","#4285F4"),("Docker","Docker","#2496ED"),
         ("Java","Openjdk",TEXT),("Node.js","Nodedotjs","#5FA04E"),("NestJS","Nestjs","#E0234E"),
         ("Express","Express",TEXT),("FastAPI","Fastapi","#05998B"),("Django","Django","#44B78B"),("Flask","Flask",TEXT),
         ("PostgreSQL","Postgresql","#4169E1"),("Redis","Redis","#FF4438"),("MongoDB","Mongodb","#47A248"),("TypeScript","Typescript","#3178C6"),
         ("JavaScript","Javascript","#F7DF1E"),("React","React","#61DAFB"),("Next.js","Nextdotjs",TEXT),("Three.js","Threedotjs",TEXT),("GSAP","Greensock","#88CE02"),("Tailwind","Tailwindcss","#06B6D4")]
def marquee():
  W, H = 1200, 210
  body, css = "", ""
  for r, tools in enumerate([TOOLS[:14], TOOLS[14:]]):
    x, g = 0, ""
    for name, key, col in tools:
      w = 70 + len(name) * 11
      paths = "".join(f'<path d="{d}"/>' for d in ICONS[key])
      g += (f'<g transform="translate({x},0)"><rect width="{w}" height="64" rx="32" fill="{PANEL}" stroke="{TEXT}" stroke-opacity=".1"/>'
            f'<g transform="translate(20,19) scale(1.1)" fill="{CYAN}" fill-opacity=".9">{paths}</g>'
            f'<text x="60" y="39" class="sans" font-size="18" font-weight="600" fill="{TEXT}">{name}</text></g>')
      x += w + 16
    frm, to = (0, -x) if r == 0 else (-x, 0)
    css += f".r{r}{{animation:m{r} {30+r*6}s linear infinite}}@keyframes m{r}{{from{{transform:translateX({frm}px)}}to{{transform:translateX({to}px)}}}}"
    body += f'<g transform="translate(0,{24 + r*92})"><g class="r{r}">{g}<g transform="translate({x},0)">{g}</g></g></g>'
  defs = (f'<linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
          f'<mask id="mk"><rect width="{W}" height="{H}" fill="url(#f)"/></mask>')
  return svg(W, H, "Toolkit: " + ", ".join(n for n, _, _ in TOOLS), f"<defs>{defs}</defs><g mask=\"url(#mk)\">{body}</g>", css)

# ---------------- PATH (timeline with travelling spark) ----------------
PATH = [("NOW", "AWS GenAI Developer", "Appbank", "compliant GenAI for regulated banking", PINK),
        ("2026", "BSc Computing, First Class", "Birkbeck", "graduated with first class honours", CYAN),
        ("2025", "AI Backend Engineer", "Oont", "one backend for AI-first products", CYAN),
        ("2025", "Computer Vision Engineer", "Scout-Me Online", "live tracking for sports analytics", LIME),
        ("2023", "AI Systems Engineer", "ICAN Peacebuilding", "auditable data across regions", VIOLET),
        ("2021", "Programming Instructor", "TOLANA · PAIMAN", "teaching code on low-resource kit", CYAN),
        ("2020", "Web Dev Instructor", "Qadims Lumiere", "where it all started", LIME)]
def path():
  W, row = 1200, 84
  H = 60 + row * len(PATH)
  X = 150
  y0, y1 = 44, 44 + row * (len(PATH) - 1)
  body = (f'<line x1="{X}" y1="{y0}" x2="{X}" y2="{y1}" stroke="url(#vl)" stroke-width="3"/>'
          f'<circle r="5" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="3.5s" repeatCount="indefinite" path="M{X} {y1} V{y0}"/></circle>')
  for i, (yr, role, co, note, c) in enumerate(PATH):
    y = y0 + i * row
    body += (f'<g class="pop" style="animation-delay:{(len(PATH)-i)*.12}s">'
             f'<text x="{X-34}" y="{y+6}" text-anchor="end" class="mono" font-size="15" fill="{PINK if i==0 else FAINT}">{yr}</text>'
             f'<circle cx="{X}" cy="{y}" r="8" fill="{PINK if i==0 else PANEL}" stroke="{PINK if i==0 else FAINT}" stroke-width="2"/>'
             + (f'<circle cx="{X}" cy="{y}" r="10" fill="none" stroke="{PINK}" stroke-width="2" class="pulse"/>' if i == 0 else "") +
             f'<rect x="{X+36}" y="{y-30}" width="{W-X-38}" height="60" rx="14" fill="{PANEL}" stroke="{PINK if i==0 else TEXT}" stroke-opacity="{.6 if i==0 else .08}"/>'
             f'<text x="{X+60}" y="{y+7}" class="sans" font-size="20" font-weight="700" fill="{TEXT}">{role}<tspan dx="14" class="mono" font-size="17" font-weight="400" fill="{PINK if i==0 else MUTED}">@{co}</tspan></text>'
             f'<text x="{W-24}" y="{y+6}" text-anchor="end" class="mono" font-size="14" fill="{MUTED}">{note}</text></g>')
  defs = (f'{GLOW}<linearGradient id="vl" x1="0" y1="{y0}" x2="0" y2="{y1}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{PINK}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{LIME}"/></linearGradient>')
  return svg(W, H, "Career path: " + "; ".join(f"{r} at {c}" for _, r, c, _, _ in PATH), f"<defs>{defs}</defs>{body}")

# ---------------- FOOTER ----------------
def footer():
  W, H = 1200, 300
  body = f"""<defs>{GLOW}{SCAN}
<linearGradient id="tx" x1="0" x2="1" gradientUnits="objectBoundingBox">
  <stop offset="0" stop-color="{PINK}"/><stop offset=".33" stop-color="{VIOLET}"/><stop offset=".66" stop-color="{CYAN}"/><stop offset="1" stop-color="{LIME}"/>
  <animate attributeName="x1" values="0;-1;0" dur="6s" repeatCount="indefinite"/><animate attributeName="x2" values="1;2;1" dur="6s" repeatCount="indefinite"/>
</linearGradient>{grad_defs("bd", dur=6)}</defs>
{frame(W, H)}
<text x="60" y="80" class="mono" font-size="16" fill="{FAINT}" letter-spacing="3">// AVAILABLE FOR NEW WORK</text>
<text x="56" y="178" class="heavy" font-size="84" fill="{TEXT}">Let’s build something <tspan fill="{PINK}">real.</tspan></text>
<circle class="pulse" cx="68" cy="238" r="5" fill="{PINK}" filter="url(#glow)"/>
<text x="88" y="244" class="mono" font-size="18" fill="{TEXT}">essashah10@gmail.com</text>
<text x="{W-60}" y="244" text-anchor="end" class="mono" font-size="16" fill="{MUTED}">get in touch ↗</text>"""
  return svg(W, H, "Let's build it — essashah10@gmail.com", body)

# ---------------- ABOUT ----------------
def about():
  W, H = 1200, 430
  stats = [("5+", "years in engineering"), ("1st", "First Class Honours · BSc Computing"), ("06", "roles across ML, backend, teaching")]
  tiles = ""
  for i, (v, l) in enumerate(stats):
    x = 48 + i * 376
    tiles += (f'<g class="pop" style="animation-delay:{.3 + i*.12}s"><rect x="{x}" y="296" width="352" height="96" rx="16" fill="{PANEL2}" fill-opacity=".55" stroke="{TEXT}" stroke-opacity=".07"/>'
              f'<text x="{x+24}" y="352" class="heavy" font-size="40" fill="{PINK}">{v}</text>'
              f'<text x="{x+24}" y="376" class="mono" font-size="12" fill="{MUTED}" letter-spacing="1">{l.upper()}</text></g>')
  body = (f'<defs>{grad_defs("bd")}<radialGradient id="gl" cx="100%" cy="0%" r="70%"><stop offset="0" stop-color="{PINK}" stop-opacity=".16"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient></defs>'
          f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="{PANEL}"/><rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="url(#gl)"/>'
          f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="none" stroke="url(#bd)" stroke-width="1.5"/>'
          f'<g class="pop"><text x="48" y="98" class="heavy" font-size="46" fill="{TEXT}">I build machine learning that holds up</text>'
          f'<text x="48" y="152" class="heavy" font-size="46" fill="{PINK}">outside the notebook.</text></g>'
          f'<g class="pop" style="animation-delay:.15s" font-size="18" fill="{MUTED}">'
          f'<text x="48" y="204" class="sans">Deep learning in PyTorch, TensorFlow &amp; Keras, classical models in scikit-learn, real-time computer vision</text>'
          f'<text x="48" y="232" class="sans">with OpenCV, NLP &amp; LLM systems on AWS Bedrock — and the full-stack product around them.</text>'
          f'<text x="48" y="260" class="sans">Banking, AI startups and live sport, after years teaching programming in Pakistan.</text></g>'
          + tiles)
  return svg(W, H, "I build machine learning that holds up outside the notebook. Deep learning in PyTorch and TensorFlow, classical models in scikit-learn, real-time computer vision with OpenCV, and NLP and LLM systems on AWS Bedrock, shipped behind reliable, observable APIs. 5+ years in engineering; BSc Computing, First Class Honours, Birkbeck, University of London; 6 roles across ML, backend and teaching.", body)

# ---------------- NEOFETCH (whoami) ----------------
# 5x7 dot-matrix glyphs for the monogram
GLYPHS = {"E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
          "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"]}
NEOFETCH = [
  ("Role", "Full-Stack Software Engineer · AI/ML Developer"),
  ("Now", "AWS GenAI Developer @ Appbank"),
  ("Degree", "BSc Computing, First Class Honours — Birkbeck"),
  ("Uptime", "6 years in tech (2020 → 2026)"),
  ("Host", "Essex, United Kingdom"),
  None,
  ("ML", "PyTorch · TensorFlow · Keras · scikit-learn"),
  ("Vision", "OpenCV · real-time detection &amp; tracking"),
  ("NLP/GenAI", "LLMs · RAG · AWS Bedrock · Guardrails"),
  ("Data", "Pandas · NumPy · Matplotlib · feature engineering"),
  ("Backend", "FastAPI · Django · Flask · Node.js · NestJS · Express"),
  ("Frontend", "React · Next.js · Three.js · GSAP · Tailwind"),
  ("Databases", "PostgreSQL · MongoDB · Redis"),
  ("Cloud/Ops", "AWS · GCP · Docker · CI/CD · microservices"),
  ("Languages", "Python · TypeScript · JavaScript · Java"),
  None,
  ("Email", "essashah10@gmail.com"),
  ("LinkedIn", "in/essa-shah-7a0a5a294"),
  ("Portfolio", "my-portfolio-theta-ten-12.vercel.app"),
]
def neofetch():
  W = 1200
  random.seed(5)
  # monogram
  dots, step, mx, my = "", 26, 70, 150
  for gi, ch in enumerate("ES"):
    for r, row in enumerate(GLYPHS[ch]):
      for c, bit in enumerate(row):
        x, y = mx + (gi * 6 + c) * step, my + r * step
        if bit == "1":
          cls = f' class="pulse" style="animation-delay:-{random.uniform(0, 3):.2f}s;animation-duration:{random.uniform(2.4, 4):.2f}s"' if random.random() < .3 else ""
          dots += f'<circle cx="{x}" cy="{y}" r="9" fill="{PINK}"{cls} filter="url(#glow)"/>'
        else:
          dots += f'<circle cx="{x}" cy="{y}" r="9" fill="{TEXT}" fill-opacity=".05"/>'
  swatch = "".join(f'<rect x="{mx - 9 + i*36}" y="{my + 7*step + 16}" width="28" height="18" rx="4" fill="{c}"/>'
                   for i, c in enumerate([BG, PANEL2, FAINT, VIOLET, PINK, CYAN, MUTED, TEXT]))
  # info column
  X, KX, VX, y, lh = 420, 420, 420 + 13 * 9.6, 118, 27
  rows = (f'<text x="{X}" y="{y}" class="mono" font-size="20" fill="{PINK}">essa<tspan fill="{TEXT}">@</tspan>shah</text>'
          f'<rect x="{X}" y="{y+14}" width="520" height="1.5" fill="{FAINT}"/>')
  y += 50
  heads = iter(["stack", "contact"])
  for k, item in enumerate(NEOFETCH):
    d = f"{.15 + k*.05:.2f}"
    if item is None:
      rows += f'<text x="{KX}" y="{y+6}" class="mono pop" font-size="13" letter-spacing="2" fill="{FAINT}" style="animation-delay:{d}s">— {next(heads).upper()} —</text>'
      y += lh + 4
      continue
    key, val = item
    lead = "." * max(2, 11 - len(key))
    rows += (f'<text x="{KX}" y="{y}" class="mono pop" font-size="16" style="animation-delay:{d}s">'
             f'<tspan fill="{PINK}">{key}</tspan><tspan fill="{FAINT}"> {lead}</tspan><tspan x="{VX}" fill="{TEXT}">{val}</tspan></text>')
    y += lh
  H = y + 30
  head = (f'<circle cx="34" cy="32" r="6" fill="{PANEL2}"/><circle cx="56" cy="32" r="6" fill="{PANEL2}"/><circle cx="78" cy="32" r="6" fill="{PANEL2}"/>'
          f'<text x="{W/2}" y="38" text-anchor="middle" class="mono" font-size="13" fill="{FAINT}">essa@shah: ~ — neofetch</text>'
          f'<line x1="0" y1="62" x2="{W}" y2="62" stroke="{PANEL2}" stroke-width="2"/>')
  label = "whoami — " + "; ".join(f"{k}: {v}" for k, v in (i for i in NEOFETCH if i)).replace("&amp;", "and")
  return svg(W, H, label, f'<defs>{grad_defs("bd")}{GLOW}{SCAN}</defs>' + frame(W, H) + head + dots + swatch + rows)

SECTIONS = [("01", "whoami", "neofetch"), ("02", "stack", "daily drivers"), ("03", "path", "2020 → now"), ("04", "activity", "live from github")]
files = {"hero": hero(), "about": about(), "neofetch": neofetch(), "marquee": marquee(), "path": path(), "footer": footer()}
for idx, label, aside in SECTIONS: files[f"s{idx}"] = section(idx, label, aside)
for k, v in files.items(): open(f"{out}/{k}.svg", "w").write(v)
print(len(files), "files")

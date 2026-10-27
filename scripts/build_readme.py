import sys
from urllib.parse import quote
U = "Essashah"
A = "https://raw.githubusercontent.com/Essashah/Essashah/main/assets"
SITE = "https://my-portfolio-theta-ten-12.vercel.app/"
LI = "https://www.linkedin.com/in/essa-shah-7a0a5a294"
P = dict(bg="09100d", fg="ecf6f1", muted="8aa69a", faint="48605a", pink="00e59b", lime="e6fff4", cyan="7dffcf", line="122019")

def img(name, alt, width="100%"): return f'<img src="{A}/{name}.svg" alt="{alt}" width="{width}" />'
def sec(i, label): return img(f"s{i}", f"{i} {label}")
streak = f"https://streak-stats.demolab.com/?user={U}&hide_border=true&border_radius=20&background={P['bg']}&ring={P['pink']}&fire={P['pink']}&currStreakNum={P['fg']}&sideNums={P['fg']}&currStreakLabel={P['pink']}&sideLabels={P['muted']}&dates={P['faint']}&stroke={P['line']}"
def badge(label, logo, href, color):
  return f'<a href="{href}"><img alt="{label}" src="https://img.shields.io/badge/{quote(label)}-{P["bg"]}?style=for-the-badge&logo={logo}&logoColor={color}&labelColor={P["bg"]}&color={P["bg"]}" /></a>'

R = []
R.append('<div align="center">\n\n' + img("hero", "ESSA SHAH — Full-Stack Software Engineer · AI/ML Developer") + "\n\n"
  + " ".join([badge("Portfolio", "vercel", SITE, P["fg"]), badge("LinkedIn", "linkedin", LI, P["fg"]), badge("Email", "gmail", "mailto:essashah10@gmail.com", P["fg"])])
  + '\n\n</div>')
R.append(img("about", "I build machine learning that holds up outside the notebook: deep learning in PyTorch, TensorFlow and Keras, classical ML in scikit-learn, real-time computer vision with OpenCV, NLP and LLM systems on AWS Bedrock, and the full-stack product around them. BSc Computing, First Class Honours, Birkbeck, University of London."))
R.append(sec("01", "whoami") + "\n\n" + img("neofetch", "whoami — Essa Shah: full-stack software engineer and AI/ML developer. Now AWS GenAI Developer at Appbank. BSc Computing, First Class Honours, Birkbeck. Stack: PyTorch, TensorFlow, Keras, scikit-learn, OpenCV, Pandas, NumPy, LLMs, RAG, AWS Bedrock, FastAPI, Django, Flask, Node.js, NestJS, React, Next.js, PostgreSQL, MongoDB, Redis, AWS, GCP, Docker."))
R.append(sec("02", "stack") + "\n\n" + img("marquee", "Toolkit: Python, PyTorch, TensorFlow, Keras, scikit-learn, OpenCV, Pandas, NumPy, Streamlit, AWS, Google Cloud, Docker, Java, Node.js, NestJS, Express, FastAPI, Django, Flask, PostgreSQL, Redis, MongoDB, TypeScript, JavaScript, React, Next.js, Three.js, GSAP, Tailwind"))
R.append(sec("03", "path") + "\n\n" + img("path", "Path: AWS GenAI Developer at Appbank (now); BSc Computing, First Class, Birkbeck (2026); AI Backend Engineer at Oont; Computer Vision Engineer at Scout-Me Online; AI Systems Engineer at ICAN Peacebuilding; Programming Instructor at TOLANA; Web Dev Instructor at Qadims Lumiere."))
R.append(sec("04", "activity") + f"""

<div align="center">

<img src="{streak}" alt="Contribution streak" width="70%" />

</div>""")
R.append('<a href="mailto:essashah10@gmail.com">' + img("footer", "Let's build something real — essashah10@gmail.com") + "</a>")
open(sys.argv[1], "w").write("\n\n<br/>\n\n".join(R) + "\n")

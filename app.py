import streamlit as st
import markdown
import re

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Présentations MD",
    page_icon="📊"
)

# CSS pour le style
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stTextArea textarea {
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Titre de l'application
st.title("📊 Générateur de Présentations Markdown")
st.markdown("Transformez votre contenu Markdown en présentation HTML interactive")

# Zone de texte pour le contenu Markdown
st.subheader("1. Collez votre contenu Markdown")
st.info("💡 Séparez vos slides avec `===` sur une ligne seule")

markdown_content = st.text_area(
    "Contenu Markdown",
    height=300,
    placeholder="""# Titre de ma présentation
Contenu de la première slide

===

## Deuxième slide
- Point 1
- Point 2

===

## Code exemple
```python
def hello():
    print("Hello World!")
```

===

## Formule mathématique
$$E = mc^2$$
""",
    label_visibility="collapsed"
)

# Options de configuration
st.subheader("2. Options de présentation")
col1, col2 = st.columns(2)

with col1:
    theme = st.selectbox(
        "Thème",
        ["Moderne Sombre", "Classique Clair", "Minimaliste", "Professionnel"]
    )
    
with col2:
    transition = st.selectbox(
        "Transition",
        ["Slide", "Fade", "None"]
    )

# Fonction pour générer le HTML
def generate_html(content, theme_name, transition_type):
    # Séparer les slides
    slides = content.split("===")
    slides = [slide.strip() for slide in slides if slide.strip()]
    
    # Thèmes CSS
    themes = {
        "Moderne Sombre": {
            "bg": "#1a1a2e",
            "text": "#eee",
            "accent": "#0f3460",
            "highlight": "#16213e"
        },
        "Classique Clair": {
            "bg": "#ffffff",
            "text": "#333",
            "accent": "#f0f0f0",
            "highlight": "#e8e8e8"
        },
        "Minimaliste": {
            "bg": "#fafafa",
            "text": "#2c3e50",
            "accent": "#ecf0f1",
            "highlight": "#bdc3c7"
        },
        "Professionnel": {
            "bg": "#2c3e50",
            "text": "#ecf0f1",
            "accent": "#34495e",
            "highlight": "#3498db"
        }
    }
    
    theme_colors = themes[theme_name]
    
    # Transitions CSS
    transitions = {
        "Slide": "transform 0.5s ease-in-out",
        "Fade": "opacity 0.5s ease-in-out",
        "None": "none"
    }
    
    # Convertir le Markdown en HTML pour chaque slide
    slides_html = []
    
    for i, slide in enumerate(slides):
        # Protéger les formules mathématiques avant le traitement Markdown
        math_inline = []
        math_block = []
        
        # Sauvegarder les blocs $$...$$ d'abord
        def save_block_math(match):
            math_block.append(match.group(0))
            return f"MATHBLOCK{len(math_block)-1}MATHBLOCK"
        
        # Pattern pour les blocs math (double dollar)
        double_dollar_pattern = r'\$\$(.+?)\$\$'
        slide = re.sub(double_dollar_pattern, save_block_math, slide, flags=re.DOTALL)
        
        # Sauvegarder les formules inline $...$
        def save_inline_math(match):
            math_inline.append(match.group(0))
            return f"MATHINLINE{len(math_inline)-1}MATHINLINE"
        
        # Pattern pour les formules inline (simple dollar)
        single_dollar_pattern = r'\$([^\$]+?)\$'
        slide = re.sub(single_dollar_pattern, save_inline_math, slide)
        
        # Utiliser markdown avec extensions pour le code
        html_content = markdown.markdown(
            slide,
            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']
        )
        
        # Restaurer les formules mathématiques
        for idx, math in enumerate(math_inline):
            html_content = html_content.replace(f"MATHINLINE{idx}MATHINLINE", math)
        
        for idx, math in enumerate(math_block):
            html_content = html_content.replace(f"MATHBLOCK{idx}MATHBLOCK", math)
        
        slides_html.append(html_content)
    
    # Template HTML complet
    html_template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Présentation</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                processEscapes: true,
                processEnvironments: true
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: {theme_colors['bg']};
            color: {theme_colors['text']};
            overflow: hidden;
        }}
        
        .presentation-container {{
            width: 100vw;
            height: 100vh;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide {{
            width: 90%;
            max-width: 1200px;
            height: 80vh;
            padding: 3rem;
            background: {theme_colors['accent']};
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            display: none;
            overflow-y: auto;
            transition: {transitions[transition_type]};
        }}
        
        .slide.active {{
            display: block;
        }}
        
        .slide h1 {{
            font-size: 3rem;
            margin-bottom: 1.5rem;
            color: {theme_colors['text']};
        }}
        
        .slide h2 {{
            font-size: 2.2rem;
            margin-bottom: 1.2rem;
            margin-top: 1.5rem;
            color: {theme_colors['text']};
        }}
        
        .slide h3 {{
            font-size: 1.8rem;
            margin-bottom: 1rem;
            margin-top: 1.2rem;
        }}
        
        .slide p {{
            font-size: 1.3rem;
            line-height: 1.8;
            margin-bottom: 1rem;
        }}
        
        .slide ul, .slide ol {{
            font-size: 1.3rem;
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}
        
        .slide li {{
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }}
        
        .slide code {{
            background: {theme_colors['highlight']};
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        .slide pre {{
            background: #282c34;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        
        .slide pre code {{
            background: none;
            padding: 0;
            color: #abb2bf;
        }}
        
        .slide img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .slide table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        .slide th, .slide td {{
            border: 1px solid {theme_colors['highlight']};
            padding: 0.8rem;
            text-align: left;
        }}
        
        .slide th {{
            background: {theme_colors['highlight']};
            font-weight: bold;
        }}
        
        .navigation {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 1rem;
            align-items: center;
            background: rgba(0,0,0,0.5);
            padding: 1rem 2rem;
            border-radius: 50px;
            backdrop-filter: blur(10px);
        }}
        
        .nav-btn {{
            background: {theme_colors['highlight']};
            color: {theme_colors['text']};
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .nav-btn:hover {{
            transform: scale(1.05);
            opacity: 0.9;
        }}
        
        .nav-btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
        }}
        
        .slide-counter {{
            color: white;
            font-size: 1rem;
            font-weight: bold;
            min-width: 80px;
            text-align: center;
        }}
        
        .fullscreen-btn {{
            position: fixed;
            top: 2rem;
            right: 2rem;
            background: rgba(0,0,0,0.5);
            color: white;
            border: none;
            padding: 0.8rem 1.2rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }}
        
        .fullscreen-btn:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        {''.join([f'<div class="slide {("active" if i == 0 else "")}" id="slide-{i}">{slide}</div>' for i, slide in enumerate(slides_html)])}
    </div>
    
    <button class="fullscreen-btn" onclick="toggleFullscreen()">Plein écran</button>
    
    <div class="navigation">
        <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)">← Précédent</button>
        <span class="slide-counter" id="slideCounter">1 / {len(slides)}</span>
        <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">Suivant →</button>
    </div>
    
    <script>
        let currentSlide = 0;
        const totalSlides = {len(slides)};
        
        function showSlide(n) {{
            const slides = document.querySelectorAll('.slide');
            
            if (n >= totalSlides) {{
                currentSlide = totalSlides - 1;
            }} else if (n < 0) {{
                currentSlide = 0;
            }} else {{
                currentSlide = n;
            }}
            
            slides.forEach((slide, index) => {{
                slide.classList.remove('active');
                if (index === currentSlide) {{
                    slide.classList.add('active');
                }}
            }});
            
            document.getElementById('slideCounter').textContent = `${{currentSlide + 1}} / ${{totalSlides}}`;
            document.getElementById('prevBtn').disabled = currentSlide === 0;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
            
            // Re-render MathJax pour la nouvelle slide
            if (typeof MathJax !== 'undefined') {{
                MathJax.typesetPromise();
            }}
            
            // Highlight code blocks
            document.querySelectorAll('.slide.active pre code').forEach((block) => {{
                hljs.highlightElement(block);
            }});
        }}
        
        function changeSlide(direction) {{
            showSlide(currentSlide + direction);
        }}
        
        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else {{
                document.exitFullscreen();
            }}
        }}
        
        // Navigation au clavier
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowLeft') {{
                changeSlide(-1);
            }} else if (e.key === 'ArrowRight' || e.key === ' ') {{
                changeSlide(1);
            }} else if (e.key === 'f' || e.key === 'F') {{
                toggleFullscreen();
            }}
        }});
        
        // Initialiser
        showSlide(0);
        hljs.highlightAll();
    </script>
</body>
</html>"""
    
    return html_template

# Bouton pour générer la présentation
if st.button("🎨 Générer la Présentation", type="primary", use_container_width=True):
    if markdown_content:
        with st.spinner("Génération de la présentation..."):
            html_output = generate_html(markdown_content, theme, transition)
            
            st.success("✅ Présentation générée avec succès !")
            
            # Aperçu
            st.subheader("3. Aperçu et Téléchargement")
            
            # Bouton de téléchargement
            st.download_button(
                label="📥 Télécharger la présentation HTML",
                data=html_output,
                file_name="presentation.html",
                mime="text/html",
                use_container_width=True
            )
            
            # Afficher un aperçu
            with st.expander("👁️ Voir le code HTML généré"):
                st.code(html_output, language="html")
            
            st.info("""
            **Instructions d'utilisation :**
            - Téléchargez le fichier HTML
            - Ouvrez-le dans votre navigateur
            - Utilisez les flèches ← → ou les boutons pour naviguer
            - Appuyez sur F pour le mode plein écran
            - La barre d'espace permet aussi d'avancer
            """)
    else:
        st.error("⚠️ Veuillez entrer du contenu Markdown")

# Section d'aide
with st.expander("📚 Guide d'utilisation"):
    st.markdown("""
    ### Format Markdown supporté
    
    **Séparation des slides :** Utilisez `===` sur une ligne seule
    
    **Texte formaté :**
    ```markdown
    # Titre principal
    ## Sous-titre
    **Gras** et *italique*
    ```
    
    **Code :**
    ```markdown
    \`\`\`python
    def exemple():
        return "Hello"
    \`\`\`
    ```
    
    **Mathématiques :**
    ```markdown
    Inline: $x^2 + y^2 = z^2$
    Bloc: $$\\int_0^\\infty e^{-x^2} dx$$
    ```
    
    **Images :**
    ```markdown
    ![Description](url_de_image.jpg)
    ```
    
    **Listes :**
    ```markdown
    - Point 1
    - Point 2
    
    1. Premier
    2. Deuxième
    ```
    
    **Tableaux :**
    ```markdown
    | Colonne 1 | Colonne 2 |
    |-----------|-----------|
    | Valeur 1  | Valeur 2  |
    ```
    """)

# Footer
st.markdown("---")
st.markdown("💡 **Astuce :** Utilisez les raccourcis clavier dans la présentation pour une navigation rapide !")

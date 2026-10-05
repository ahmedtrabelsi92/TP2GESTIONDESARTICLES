import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Configuration du document PDF
pdf_filename = "COMPTE-RENDU-TP2GESTIONDESARTICLES.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    rightMargin=30,
    leftMargin=30,
    topMargin=30,
    bottomMargin=30
)

# 2. Définition des styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=18,
    alignment=1,  # Centré
    spaceAfter=20,
    textColor=colors.HexColor('#1A365D')
)

heading_style = ParagraphStyle(
    'HeadingStyle',
    parent=styles['Heading2'],
    fontSize=14,
    spaceBefore=12,
    spaceAfter=6,
    textColor=colors.HexColor('#2B6CB0')
)

body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=8,
    leading=14
)

story = []

# 3. En-tête et Titre du TP
story.append(Paragraph("<b>COMPTE RENDU : TP2 GESTION DES ARTICLES (ASP.NET Core MVC & Entity Framework Core)</b>", title_style))
story.append(Spacer(1, 10))

# Informatios générales
info_text = """
<b>Auteur :</b> Ahmed TRABELSI<br/>
<b>Projet :</b> TP2GESTIONDESARTICLES<br/>
<b>Framework :</b> ASP.NET Core MVC / Entity Framework Core (Code First)<br/>
<b>Sujet :</b> Gestion des Catégories et des Produits avec téléversement d'images
"""
story.append(Paragraph(info_text, body_style))
story.append(Spacer(1, 15))

# 4. Section 1 : Structure du Projet & Migrations EF Core
story.append(Paragraph("1. Structure du Projet et Migrations EF Core", heading_style))
p1_text = """
Le projet repose sur l'architecture ASP.NET Core MVC avec Entity Framework Core. 
Les migrations suivantes ont été appliquées avec succès dans la base de données :
<ul>
    <li><b>InitialCreate :</b> Création initiale du contexte de base de données.</li>
    <li><b>AddImagePathToProduct :</b> Ajout du champ d'image pour stocker le chemin des visuels des produits.</li>
    <li><b>AddCategoryAndProduct :</b> Modélisation de la relation entre la catégorie et le produit.</li>
</ul>
"""
story.append(Paragraph(p1_text, body_style))

# Inclusion de la capture de l'Explorateur de solutions
if os.path.exists('input_file_5.png'):
    story.append(Image('input_file_5.png', width=500, height=350))
    story.append(Spacer(1, 15))

# 5. Section 2 : Validation des Fonctionnalités & Captures
story.append(Paragraph("2. Captures d'Écran et Validation des Fonctionnalités", heading_style))
story.append(Paragraph("Les captures ci-dessous illustrent l'arborescence du projet ainsi que la gestion des catégories et des produits dans l'application.", body_style))

# Liste des captures d'écran des formulaires et vues
images_list = ['input_file_0.png', 'input_file_1.png', 'input_file_2.png', 'input_file_3.png', 'input_file_4.png']
for img_name in images_list:
    if os.path.exists(img_name):
        story.append(Image(img_name, width=450, height=250))
        story.append(Spacer(1, 10))

# 6. Génération du PDF
doc.build(story)
print(f"Rapport généré avec succès : {pdf_filename}")
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

# --- Gestionnaire de pied de page dynamique (ex: Page X / 4) ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        footer_text = "TP2GESTIONDESARTICLES - ASP.NET Core MVC"
        page_str = f"Page {self._pageNumber} / {page_count}"
        
        self.drawString(54, 30, footer_text)
        self.drawRightString(612 - 54, 30, page_str)
        self.restoreState()

def generate_exact_tp2_pdf(filename="Rapport_TP2_Gestion_Articles.pdf"):
    # Marges du document (0.75 in = 54 pt)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # --- Styles typographiques ---
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1B4D89'),
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2B6CB0'),
        alignment=1,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'MetaBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1A202C'),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1B4D89'),
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1A202C'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceBefore=6,
        spaceAfter=10
    )

    story = []

    # ==================== PAGE 1 ====================
    story.append(Paragraph("RAPPORT DE TRAVAUX PRATIQUES N°2", title_style))
    story.append(Paragraph("Développement d'une application de gestion d'articles avec ASP.NET Core MVC", subtitle_style))

    # Encadré des métadonnées du projet
    meta_text = "<b>Projet :</b> TP2GESTIONDESARTICLES &nbsp;&nbsp;|&nbsp;&nbsp; <b>Framework :</b> .NET Core MVC &nbsp;&nbsp;|&nbsp;&nbsp; <b>Sujet :</b> CRUD Catégories et Produits avec Upload d'Images"
    meta_table = Table([[Paragraph(meta_text, meta_style)]], colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Section 1
    story.append(Paragraph("1. Présentation Générale", h1_style))
    story.append(Paragraph(
        "Ce document présente la réalisation pratique du TP2 portant sur la création d'une application web de gestion d'articles sous <b>ASP.NET Core MVC</b>. L'application permet la gestion complète du catalogue de produits et de leurs catégories respectives.",
        body_style
    ))
    story.append(Paragraph("Les fonctionnalités clés développées incluent :", body_style))

    bullets_p1 = [
        "• La gestion des catégories (Affichage, Création, Modification, Suppression).",
        "• La gestion du catalogue de produits avec affichage dynamique sous forme de cartes d'articles.",
        "• La recherche multi-critères (par nom de produit ou par catégorie).",
        "• L'association dynamique des catégories aux produits via une liste déroulante.",
        "• La prise en charge du téléversement et de l'affichage des images de produits."
    ]
    for b in bullets_p1:
        story.append(Paragraph(b, bullet_style))

    story.append(Spacer(1, 10))

    # Section 2
    story.append(Paragraph("2. Module de Gestion des Catégories", h1_style))
    story.append(Paragraph(
        "Le module de gestion des catégories permet d'organiser les articles par familles (ex: <i>Electroménager, Informatique, Téléphonie</i>).",
        body_style
    ))

    # Section 2.1
    story.append(Paragraph("2.1. Affichage de la Liste des Catégories", h2_style))
    story.append(Paragraph(
        "La vue principale des catégories affiche un tableau récapitulatif contenant les identifiants, les libellés ainsi que les actions disponibles pour chaque enregistrement.",
        body_style
    ))

    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    img1_path = "Categorys.png"
    if os.path.exists(img1_path):
        story.append(RLImage(img1_path, width=440, height=210))
    story.append(Paragraph("<i>Figure 1 : Interface de consultation de la liste des catégories (/Category)</i>", caption_style))
    story.append(Spacer(1, 15))

    # Section 2.2
    story.append(Paragraph("2.2. Formulaire de Création d'une Catégorie", h2_style))
    story.append(Paragraph(
        "L'interface de création permet d'ajouter rapidement une nouvelle catégorie au système.",
        body_style
    ))

    img2_path = "CategoryCreate.png"
    if os.path.exists(img2_path):
        story.append(RLImage(img2_path, width=440, height=210))
    story.append(Paragraph("<i>Figure 2 : Formulaire de création d'une nouvelle catégorie (/Category/Create)</i>", caption_style))

    story.append(PageBreak())

    # ==================== PAGE 3 ====================
    # Section 3
    story.append(Paragraph("3. Module de Gestion des Produits", h1_style))
    story.append(Paragraph(
        "Le module des produits constitue le cœur du système d'information. Il permet la présentation visuelle des articles en stock et la saisie de leurs caractéristiques détaillées.",
        body_style
    ))

    # Section 3.1
    story.append(Paragraph("3.1. Catalogue des Produits", h2_style))
    story.append(Paragraph(
        "Le catalogue est conçu sous forme de grille interactive. Chaque carte produit expose le nom, le prix exprimé en TND, la quantité disponible en stock, la catégorie rattachée, une illustration visuelle ainsi que des raccourcis d'action (<i>View, Edit, Delete</i>). Un champ de recherche permet de filtrer en temps réel le catalogue.",
        body_style
    ))

    img3_path = "Products.png"
    if os.path.exists(img3_path):
        story.append(RLImage(img3_path, width=440, height=280))
    story.append(Paragraph("<i>Figure 3 : Catalogue interactif des produits avec module de recherche (/Product)</i>", caption_style))

    story.append(PageBreak())

    # ==================== PAGE 4 ====================
    # Section 3.2
    story.append(Paragraph("3.2. Formulaire d'Ajout d'un Produit", h2_style))
    story.append(Paragraph(
        "Le formulaire de création d'un produit prend en charge la saisie structurée des données nécessaires (Nom, Prix, Quantité, Sélection de la catégorie via une liste déroulante et choix du fichier d'image).",
        body_style
    ))

    img4_path = "ProductCreate.png"
    if os.path.exists(img4_path):
        story.append(RLImage(img4_path, width=440, height=280))
    story.append(Paragraph("<i>Figure 4 : Formulaire complet d'ajout d'un nouveau produit (/Product/Create)</i>", caption_style))
    story.append(Spacer(1, 15))

    # Section 4
    story.append(Paragraph("4. Conclusion", h1_style))
    story.append(Paragraph(
        "L'ensemble des exigences du TP2 a été mis en œuvre avec succès. L'application offre une interface claire, réactive et totalement fonctionnelle pour la gestion centralisée des articles et de leurs catégories.",
        body_style
    ))

    # Génération du fichier PDF
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    generate_exact_tp2_pdf()
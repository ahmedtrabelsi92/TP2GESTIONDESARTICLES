from PIL import Image

# 1. Liste de vos 4 images dans l'ordre souhaité
image_files = [
    "Categorys.png", 
    "CategoryCreate.png", 
    "Products.png", 
    "ProductCreate.png"
]

# 2. Ouvrir toutes les images
images = [Image.open(img) for img in image_files]

# 3. Sauvegarder sous forme de GIF animé
images[0].save(
    "Diaporama_TP2.gif",
    save_all=True,
    append_images=images[1:],
    duration=2000,  # Durée d'affichage de chaque image en millisecondes (2 secondes)
    loop=0          # 0 = boucle infinie
)

print("GIF animé généré avec succès sous le nom de 'Diaporama_TP2.gif' !")
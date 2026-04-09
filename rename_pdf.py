import os
from pdf2image import convert_from_path
import pytesseract
import re

# 👉 IMPORTANT : chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r""C:\Users\ajallaguier.OCRE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe""

folder = "pdfs"  # dossier où tu mets tes fichiers

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)

        try:
            images = convert_from_path(path, poppler_path=r"C:\poppler\Library\bin")
            full_text = ""

            for img in images:
                full_text += pytesseract.image_to_string(img, lang='fra')

            # 🔍 zone élève uniquement
            bloc = full_text.split("Identité de l'élève")[1].split("REPRÉSENTANTS LÉGAUX")[0]

            nom = re.search(r"Nom de famille\s*:\s*(\w+)", bloc).group(1)
            prenom = re.search(r"Prénom 1\s*:\s*(\w+)", bloc).group(1)

            new_name = f"{nom}_{prenom}_RENS_BENEF.pdf"

            os.rename(path, os.path.join(folder, new_name))

            print(f"OK : {file} → {new_name}")

        except Exception as e:
            print(f"ERREUR : {file} → {e}")

input("Terminé ! Appuie sur Entrée pour fermer...")

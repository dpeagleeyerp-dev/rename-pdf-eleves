import os
from pdf2image import convert_from_path
import pytesseract
import re

# 👉 Chemins (adaptés à ton PC)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ajallaguier.OCRE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Users\ajallaguier.OCRE\AppData\Local\Programs\Tesseract-OCR\tessdata"

folder = "pdfs"

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)

        try:
            # 📄 Convertir PDF en images
            images = convert_from_path(path, poppler_path=r"C:\poppler\Library\bin")

            full_text = ""
            for img in images:
                text = pytesseract.image_to_string(img, lang='fra')
                full_text += text + "\n"

            # 🔧 Nettoyage OCR (important)
            full_text = full_text.replace("\n", " ")
            full_text = re.sub(r"\s+", " ", full_text)

            # 🔍 Trouver bloc "Identité de l’élève"
            match_bloc = re.search(
                r"Identit[eé]\s+de\s+l[’']?él[eè]ve(.*?)REPRÉSENTANTS L[ÉE]GAUX",
                full_text,
                re.IGNORECASE
            )

            if not match_bloc:
                raise Exception("Bloc élève introuvable")

            bloc = match_bloc.group(1)

            # 🔍 Extraction NOM
            nom_match = re.search(r"Nom\s+de\s+famille\s*:\s*([A-Z\-]+)", bloc, re.IGNORECASE)

            # 🔍 Extraction PRENOM
            prenom_match = re.search(r"Pr[ée]nom\s*1\s*:\s*([A-Za-z\-]+)", bloc, re.IGNORECASE)

            if not nom_match or not prenom_match:
                raise Exception("Nom ou prénom introuvable")

            nom = nom_match.group(1).upper()
            prenom = prenom_match.group(1).capitalize()

            new_name = f"{nom}_{prenom}_RENS_BENEF.pdf"

            os.rename(path, os.path.join(folder, new_name))

            print(f"OK : {file} → {new_name}")

        except Exception as e:
            print(f"ERREUR : {file} → {e}")

input("Terminé ! Appuie sur Entrée pour fermer...")

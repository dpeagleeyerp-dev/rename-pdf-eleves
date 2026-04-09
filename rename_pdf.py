import os
from pdf2image import convert_from_path
import pytesseract
import re

# 🔧 CONFIGURATION (tes chemins)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ajallaguier.OCRE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Users\ajallaguier.OCRE\AppData\Local\Programs\Tesseract-OCR\tessdata"

POPPLER_PATH = r"C:\poppler\Library\bin"
FOLDER = "pdfs"

print("🚀 Démarrage du traitement...\n")

for file in os.listdir(FOLDER):
    if file.lower().endswith(".pdf"):
        path = os.path.join(FOLDER, file)

        try:
            print(f"📄 Traitement : {file}")

            # 📄 Convertir PDF → images
            images = convert_from_path(path, poppler_path=POPPLER_PATH)

            full_text = ""
            for img in images:
                text = pytesseract.image_to_string(img, lang='fra')
                full_text += text + "\n"

            # 🧹 Nettoyage OCR
            full_text = full_text.replace("\n", " ")
            full_text = re.sub(r"\s+", " ", full_text)

            # 🔍 Bloc IDENTITE UNIQUEMENT
            match_bloc = re.search(
                r"IDENTIT[EÉ]\s+DE\s+L['’]ELEVE(.*?)REPRÉSENTANTS L[ÉE]GAUX",
                full_text,
                re.IGNORECASE
            )

            if not match_bloc:
                print(f"⚠️ IGNORÉ : bloc élève introuvable\n")
                continue

            bloc = match_bloc.group(1)

            # 🔍 NOM
            nom_match = re.search(
                r"Nom\s+de\s+famille\s*:\s*([A-Z\-]+)",
                bloc,
                re.IGNORECASE
            )

            # 🔍 PRENOM
            prenom_match = re.search(
                r"Pr[ée]nom(\s*1)?\s*:\s*([A-Za-z\-]+)",
                bloc,
                re.IGNORECASE
            )

            if not nom_match or not prenom_match:
                print(f"⚠️ IGNORÉ : nom/prénom introuvable\n")
                continue

            nom = nom_match.group(1).upper()
            prenom = prenom_match.group(2).capitalize()

            new_name = f"{nom}_{prenom}_RENS_BENEF.pdf"
            new_path = os.path.join(FOLDER, new_name)

            # ⚠️ éviter écrasement
            if os.path.exists(new_path):
                print(f"⚠️ EXISTE DÉJÀ : {new_name}\n")
                continue

            os.rename(path, new_path)

            print(f"✅ RENOMMÉ : {new_name}\n")

        except Exception as e:
            print(f"❌ ERREUR : {file} → {e}\n")

print("🎉 Terminé !")
input("Appuie sur Entrée pour fermer...")

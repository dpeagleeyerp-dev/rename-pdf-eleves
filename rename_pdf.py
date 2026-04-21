import os
from pdf2image import convert_from_path
import pytesseract
import re

# 🔧 CONFIGURATION
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

            # 📄 OCR
            images = convert_from_path(path, poppler_path=POPPLER_PATH)

            full_text = ""
            for img in images:
                text = pytesseract.image_to_string(img, lang='fra')
                full_text += text + "\n"

            # 🧹 Nettoyage
            full_text = full_text.replace("\n", " ")
            full_text = re.sub(r"\s+", " ", full_text)

            # 🔍 Recherche NOM dans phrase officielle
            match = re.search(
                r"soussign[ée]\(e\)\s*(madame|monsieur)\s*,\s*([A-Z\-]+)",
                full_text,
                re.IGNORECASE
            )

            if not match:
                print("⚠️ IGNORÉ : phrase 'Je soussigné...' introuvable\n")
                continue

            nom = match.group(2).upper()

            new_name = f"{nom}_AUTOR_PARE.pdf"
            new_path = os.path.join(FOLDER, new_name)

            # 🔁 Gestion doublons
            counter = 1
            base_name = f"{nom}_AUTOR_PARE"

            while os.path.exists(new_path):
                new_name = f"{base_name}_{counter}.pdf"
                new_path = os.path.join(FOLDER, new_name)
                counter += 1

            os.rename(path, new_path)

            print(f"✅ RENOMMÉ : {new_name}\n")

        except Exception as e:
            print(f"❌ ERREUR : {file} → {e}\n")

print("🎉 Terminé !")
input("Appuie sur Entrée pour fermer...")

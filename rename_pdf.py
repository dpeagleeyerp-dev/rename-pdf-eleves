import os
import shutil
import re
import fitz  # PyMuPDF
import pytesseract

# --- CONFIGURATION TESSERACT ---
# Indique ici le chemin exact vers l'exécutable tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'"C:\Users\ajallaguier.OCRE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"'

SOURCE_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\Monprojet3"
DEST_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\SORTIE_FINAL"

os.makedirs(DEST_ROOT, exist_ok=True)

def extraire_nom_ocr_direct(chemin_pdf):
    try:
        # 1. Ouvrir le PDF et transformer la page 1 en image (pixmap)
        doc = fitz.open(chemin_pdf)
        page = doc[0]
        # On augmente la résolution (zoom=2) pour que Tesseract lise mieux
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        # 2. Transformer l'image en texte via Tesseract
        # On convertit les données brutes de l'image en texte
        img_data = pix.tobytes("png")
        texte = pytesseract.image_to_string(img_data, lang='fra')
        doc.close()

        # 3. Nettoyer et chercher le nom
        texte_ligne = " ".join(texte.split())
        
        # Regex : Cherche Madame/Monsieur puis le premier mot en MAJUSCULES (3+ lettres)
        match = re.search(r"(?:madame|monsieur)[^\w]+([A-ZÀ-ÿ\-]{3,})", texte_ligne, re.IGNORECASE)
        
        if match:
            return match.group(1).strip().upper()
            
    except Exception as e:
        print(f"❌ Erreur sur {os.path.basename(chemin_pdf)} : {e}")
    return None

print("🚀 Analyse OCR en cours (méthode directe)...")
print("Cela peut prendre quelques secondes par fichier.\n")

stats_ok = 0
stats_fail = 0

for file in os.listdir(SOURCE_ROOT):
    if file.lower().endswith(".pdf"):
        chemin_abs = os.path.join(SOURCE_ROOT, file)
        
        nom = extraire_nom_ocr_direct(chemin_abs)
        
        if nom:
            dossier_final = os.path.join(DEST_ROOT, nom)
            os.makedirs(dossier_final, exist_ok=True)
            
            dest_path = os.path.join(dossier_final, f"{nom}_AUTOR_PAR.pdf")
            
            # Gestion doublons
            c = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dossier_final, f"{nom}_AUTOR_PAR_{c}.pdf")
                c += 1
            
            shutil.copy2(chemin_abs, dest_path)
            print(f"✅ Trouvé : {nom} (Fichier: {file})")
            stats_ok += 1
        else:
            print(f"⚠️ Échec : {file}")
            stats_fail += 1

print(f"\n--- BILAN ---")
print(f"✅ Réussis : {stats_ok}")
print(f"⚠️ Échecs  : {stats_fail}")
input("\nAppuie sur Entrée pour quitter...")

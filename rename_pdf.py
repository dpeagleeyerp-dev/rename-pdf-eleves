import os
import shutil
import re
import fitz  # PyMuPDF

SOURCE_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\Monprojet3"
DEST_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\SORTIE2"

os.makedirs(DEST_ROOT, exist_ok=True)

def extraire_nom_du_pdf(chemin_pdf):
    try:
        doc = fitz.open(chemin_pdf)
        # Extraction de la première page avec nettoyage des blancs
        texte = ""
        for page in doc[:1]:
            texte += page.get_text("text")
        doc.close()

        # On transforme tout en une seule ligne propre sans sauts de ligne
        texte_ligne = " ".join(texte.split())

        # REGEX OPTIMISÉE pour : "madame/monsieur, NOM" ou "madame/monsieur NOM"
        # On cherche le mot clé, puis on accepte n'importe quel caractère non-alphabétique 
        # (virgule, espace, slash) avant de capturer le NOM en majuscules.
        match = re.search(r"(?:madame|monsieur)[^a-zA-Z]+([A-ZÀ-ÿ\-]{3,})", texte_ligne, re.IGNORECASE)
        
        if match:
            return match.group(1).strip().upper()
            
    except Exception as e:
        print(f"❌ Erreur lecture : {e}")
    return None

print("🚀 Lancement du scan des 253 fichiers...\n")

stats_ok = 0
stats_fail = 0

for root, dirs, files in os.walk(SOURCE_ROOT):
    for file in files:
        if file.lower().endswith(".pdf"):
            chemin_abs = os.path.join(root, file)
            
            nom = extraire_nom_du_pdf(chemin_abs)
            
            if nom:
                dossier_final = os.path.join(DEST_ROOT, nom)
                os.makedirs(dossier_final, exist_ok=True)
                
                # Format: NOM_AUTOR_PAR.pdf
                nouveau_nom = f"{nom}_AUTOR_PAR.pdf"
                dest_path = os.path.join(dossier_final, nouveau_nom)
                
                # Gestion doublons
                c = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dossier_final, f"{nom}_AUTOR_PAR_{c}.pdf")
                    c += 1
                
                shutil.copy2(chemin_abs, dest_path)
                print(f"✅ {nom} trouvé dans {file}")
                stats_ok += 1
            else:
                print(f"⚠️ NOM NON TROUVÉ : {file}")
                stats_fail += 1

print(f"\n--- BILAN ---")
print(f"✅ Succès : {stats_ok}")
print(f"⚠️ Échecs : {stats_fail}")

input("\nAppuie sur Entrée pour quitter...")

import os
import shutil
import re
import fitz  # PyMuPDF

# 📂 CONFIGURATION DES DOSSIERS
# (Modifie ces chemins si nécessaire)
SOURCE_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\Monprojet3"
DEST_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\SORTIE2"

# Création du dossier de sortie s'il n'existe pas
os.makedirs(DEST_ROOT, exist_ok=True)

def extraire_nom_du_pdf(chemin_pdf):
    """
    Ouvre le PDF, lit la première page et cherche le NOM après madame/monsieur.
    """
    try:
        doc = fitz.open(chemin_pdf)
        if len(doc) == 0:
            return None
            
        # On extrait le texte de la première page uniquement
        texte = doc[0].get_text()
        doc.close()

        # REGEX AFFINÉE :
        # 1. (?:madame|monsieur) -> Cherche l'un ou l'autre sans le capturer
        # 2. [\s,]+ -> Saute les espaces et les virgules qui suivent
        # 3. ([A-ZÀ-ÿ\-]+) -> Capture le NOM (majuscules, accents et tirets)
        match = re.search(r"(?:madame|monsieur)[\s,]+([A-ZÀ-ÿ\-]{2,})", texte, re.IGNORECASE)
        
        if match:
            # On nettoie et on met en majuscules (ex: ABDELLAOUI)
            return match.group(1).strip().upper()
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {os.path.basename(chemin_pdf)} : {e}")
    return None

print("🚀 Démarrage de l'automatisation...")
print(f"📁 Source : {SOURCE_ROOT}")
print(f"📁 Destination : {DEST_ROOT}\n")

stats_ok = 0
stats_ignore = 0

# Parcourir l'arborescence
for root, dirs, files in os.walk(SOURCE_ROOT):
    for file in files:
        if file.lower().endswith(".pdf"):
            path_origine = os.path.join(root, file)
            
            # 1. Extraction du nom
            nom_extrait = extraire_nom_du_pdf(path_origine)

            if not nom_extrait:
                print(f"⚠️ NOM NON TROUVÉ : {file}")
                stats_ignore += 1
                continue

            # 2. Préparer le renommage
            # Format cible : NOM_AUTOR_PAR.pdf
            dossier_destination = os.path.join(DEST_ROOT, nom_extrait)
            os.makedirs(dossier_destination, exist_ok=True)

            nouveau_nom_base = f"{nom_extrait}_AUTOR_PAR"
            dest_path = os.path.join(dossier_destination, f"{nouveau_nom_base}.pdf")

            # 3. Gestion des doublons (évite d'écraser)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dossier_destination, f"{nouveau_nom_base}_{counter}.pdf")
                counter += 1

            # 4. Copie et renommage
            try:
                shutil.copy2(path_origine, dest_path)
                print(f"✅ Classé : {file}  ==>  {os.path.basename(dest_path)}")
                stats_ok += 1
            except Exception as e:
                print(f"❌ Erreur copie : {file} -> {e}")

print(f"\n--- TERMINE ---")
print(f"✨ Fichiers traités avec succès : {stats_ok}")
print(f"⚠️ Fichiers ignorés (nom non trouvé) : {stats_ignore}")
print(f"📂 Les fichiers sont dans : {DEST_ROOT}")

input("\nAppuie sur Entrée pour fermer...")

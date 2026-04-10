import os
import shutil
import re

# 📂 Dossier racine
SOURCE_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\Monprojet2"

# 📁 Dossier de sortie
DEST_ROOT = r"C:\Users\ajallaguier.OCRE\Documents\SORTIE"

os.makedirs(DEST_ROOT, exist_ok=True)

print("🚀 Regroupement par NOM en cours...\n")

for root, dirs, files in os.walk(SOURCE_ROOT):
    for file in files:
        if file.lower().endswith(".pdf"):

            path = os.path.join(root, file)

            try:
                print(f"📄 Analyse : {file}")

                filename = file.upper()

                # 🔍 Extraction NOM (avant _ OU espace OU fin)
                match = re.match(r"([A-Z\-]+)", filename)

                if not match:
                    print("⚠️ IGNORÉ : nom non reconnu\n")
                    continue

                nom = match.group(1)

                # 📁 Créer dossier NOM
                dossier_nom = os.path.join(DEST_ROOT, nom)
                os.makedirs(dossier_nom, exist_ok=True)

                # 📂 Copier fichier
                new_path = os.path.join(dossier_nom, file)

                # 🔁 éviter écrasement
                counter = 1
                base_name = file.replace(".pdf", "")

                while os.path.exists(new_path):
                    new_path = os.path.join(
                        dossier_nom,
                        f"{base_name}_{counter}.pdf"
                    )
                    counter += 1

                shutil.copy2(path, new_path)

                print(f"✅ Copié vers : {nom}\n")

            except Exception as e:
                print(f"❌ ERREUR : {file} → {e}\n")

print("🎉 Terminé !")
input("Appuie sur Entrée pour fermer...")

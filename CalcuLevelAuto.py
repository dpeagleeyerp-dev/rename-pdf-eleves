import os

def check_depth(root_path, max_depth=5):
    root_path = os.path.abspath(root_path)
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Calcul du niveau (profondeur)
        depth = dirpath[len(root_path):].count(os.sep)
        
        if depth + 1 > max_depth:  # +1 pour compter le niveau racine comme niveau 1
            print(f"Niveau {depth + 1} : {dirpath}")
with open("resultat.txt", "w") as f:
    ...
    f.write(f"Niveau {depth + 1} : {dirpath}\n")
 

# 👉 Remplace par ton chemin
check_depth("S:\drafpica\FINANCIER")

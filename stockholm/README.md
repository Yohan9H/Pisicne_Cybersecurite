# Stockholm

Ce projet est un simulateur de rançongiciel.

## Utilisation

1.  **Démarrer l'environnement de développement :**
    ```bash
    make up
    ```

2.  **Ouvrir un terminal dans le conteneur Linux :**
    ```bash
    make shell
    ```

3.  **Exécuter le programme (depuis le shell du conteneur) :**

    *   Pour **créer** le programme :
        ```bash
        pyinstaller --onefile stockholm.py
        ```

    *   Pour **chiffrer** les fichiers dans le dossier `~/infection` :
        ```bash
        ./dist/stockholm
        ```
        La clé de chiffrement sera sauvegardée dans `key.txt`.

    *   Pour **déchiffrer** les fichiers :
        ```bash
        ./dist/stockholm -r <key.txt>
        ```

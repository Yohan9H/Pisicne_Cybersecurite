**Attack**

- make shell
- utiliser *ping -c 1 {adresse}* : pour creer un premier contact qui va nous servir a avoir l'addresse MAC
- utiliser *arp -a* : pour voir les adresses MAC
- Lancer l'attaque ARP poisoning avec le programme ou l'exec dist/inquisitor.

  exemple: 
  ```bash
    python inquisitor.py 10.0.0.30 <MAC_DU_SERVEUR_FTP> 10.0.0.20 <MAC_DE_LA_VICTIME>
  ```

**Victime**

- make victim-shell
- se connecter au serveur LFTP : *lftp -u testuser,testpass 10.0.0.30*
- créer un fichier a envoyer au serveur : *!echo "mon super secret" > secret.txt*
- envoi du fichier : *put secret.txt*
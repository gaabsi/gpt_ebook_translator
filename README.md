# gpt_ebook_translator

## Contexte
Ce projet a été inspiré par ma récente découverte d'un webnovel chinois.  
Après avoir regardé les premiers épisodes de l'animé **Lord Of The Mysteries**, j'ai eu envie de commencer à lire le webnovel.  
Cependant j'ai très vite vu que les tranductions fanmade s'arrêtaient tôt dans leurs parutions.  
J'ai donc cherché si le webnovel était disponible sur internet et j'ai trouvé sa version originale (en mandarin) et une seconde en anglais.  
Malheureusement je ne parle pas le mandarin et je ne me sentais pas de lire 1500+ chapitres dans la langue de Shakespear alors j'ai eu l'idée de ce projet. 

## Fonctionnement
J'ai donc développé une solution qui exploite l'API de ChatGPT d'OpenAI pour effectuer la traduction de l'anglais vers le français de manière automatique.  
La solution prend en entrée un ebook au format .epub et ressort un ebook au format .epub également.  
Ceci afin de rendre l'objet fini lisible par l'application "Livres" native sur iPhone.  

La pipeline s'articule ainsi : 
- le livre en .epub est transformé en .md 
- on spécifie lesquels de ces chapitres on veut traduire
- on envoie chaque chapitre non traduit 1 par 1 accompagné d'un prompt au modèle GPT. 
- on récupère la réponse traduite qu'on stocke 
- ... on itère jusqu'a traduire tous les chapitres voulus ...
- on prend tous les chapitres traduis qu'on assemble selon un style en css défini et on retransforme le tout en .epub

## Prérequis
Pour fonctionner il faut obtenir une clé API sans quoi on ne pourra pas requêter le modèle.   
Pour ce faire voici la démarche : 
- créer un compte ou se connecter au [portail API](https://platform.openai.com/account/api-keys)
- cliquer sur **“Create new secret key”** pour générer une nouvelle clé (en haut à droite)
- copier la clé créée (gardez-la au chaud pour la partie suivante où je vous explique comment l'utiliser)
- recharger le compte de quelques dollars pour pouvoir requêter l'API sur ce [portail](https://platform.openai.com/settings/organization/billing/overview)
  >  *À titre indicatif, un volume de* **Lord of the Mysteries** *d’environ 200 chapitres m’a coûté un peu moins de 7 $ à traduire.*


## Réutilisation

Afin de pouvoir traduire aussi **LOTM** ou tout autre ebook au format .epub.  
Sur le terminal de votre machine physique : 

Copiez le projet dans votre machine.  : 
```bash 
cd ~
git clone https://github.com/gaabsi/gpt_ebook_translator.git
```

Ajouter au shell votre clé API et donnez lui les droits d'execution : 
```bash
code translate.sh #Changez la variable OPENAI_API_KEY et remplacez la par votre clé et sauvegardez le fichier
chmod +x translate .sh
```

Pour traduire un ebook pour pourrez ainsi procéder de la manière suivante : 
```bash 
./translate.sh {Chemin du .epub à traduire} {Chemin du .epub traduit} {Chapitre début trad} {Chapitre fin trad}
#Exemple de traduction du tome Undying de LOTM (chap 733 à 946)
./translate.sh LOTM_original.epub Undying.epub 733 946
```

Bonne lecture ! 


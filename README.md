# **Surveillance de la Pression Artérielle avec FHIR, Kafka, Elasticsearch et Kibana**

Bienvenue dans ce repository GitHub qui contient le code source et les fichiers d'un projet universitaire en Big Data.  
Ce projet implémente une solution complète pour surveiller les pressions artérielles des patients en temps réel, en utilisant les technologies modernes comme **Kafka**, **Elasticsearch**, et **Kibana**.  

---

## **Contexte**  

La surveillance des patients grâce à leurs mesures de pression artérielle est essentielle pour détecter les cas nécessitant une prise en charge rapide.  
En s'appuyant sur le standard **FHIR** ([documentation officielle](https://www.hl7.org/fhir/overview.html)), ce projet vise à :  

- Générer et analyser des données médicales standardisées.  
- Détecter les anomalies critiques.  
- Fournir une visualisation claire et efficace pour un suivi renforcé.  

---

## **Fonctionnalités**  

1. **Génération de messages FHIR** :  
   - Création de fichiers JSON contenant des observations de pression artérielle (systolique et diastolique).  

2. **Transmission avec Kafka** :  
   - Publier les données générées sur un topic Kafka.  
   - Récupérer les messages pour analyse avec un consumer Kafka.  

3. **Analyse des données** :  
   - Détecter les anomalies selon les règles suivantes :  
     - **Systolique** : > 140 mmHg ou < 90 mmHg.  
     - **Diastolique** : > 90 mmHg ou < 60 mmHg.  

4. **Traitement des données** :  
   - **Pression artérielle anormale** : Indexation dans Elasticsearch avec métadonnées.  
   - **Pression artérielle normale** : Archivage local dans des fichiers JSON.  

5. **Visualisation avec Kibana** :  
   - Création de dashboards pour observer :  
     - La répartition des anomalies.  
     - Les tendances des pressions artérielles.  
     - Les cas critiques nécessitant une attention immédiate.  

---

## **Objectifs du Projet**  

### **Objectif Général**  

Développer une solution complète pour analyser et traiter les données de pression artérielle afin d’améliorer le suivi médical des patients.  

### **Objectifs Spécifiques**  

1. Générer des messages FHIR au format JSON pour différents patients.  
2. Publier ces messages sur Kafka et les consommer pour analyse.  
3. Détecter les anomalies selon les seuils définis.  
4. Indexer les anomalies dans Elasticsearch et visualiser les données dans Kibana.  
5. Archiver les données normales localement.  

---

## **Structure du Repository**  

Ce repository contient les fichiers suivants :  

1. **[Message_FHIR_Project.py](./Message_FHIR_Project.py)**  
   - Script principal générant des messages FHIR, publiant les données sur Kafka et indexant les anomalies dans Elasticsearch.  

2. **[Message_FHIR_Project_explication.py](./Message_FHIR_Project_explication.py)**  
   - Fichier d'explication détaillant le fonctionnement du script principal.  

3. **[normal_blood_pressure.json](./normal_blood_pressure.json)**  
   - Exemple de fichier JSON crée après l'exécution du script principal et contenant des messages FHIR de patients avec des pressions artérielles normales.

4. **[dernière_date.txt](./dernière_date.txt)**  
   - Exemple de fichier texte créé après l'exécution du script principal et contenant la dernière date de la dernière observation générée par le script. Ce fichier permet de relancer le script principal à partir de cette date à chaque exécution. Cela évite de lancer le script avec 1000 itérations si votre ordinateur est assez lent et est également utile pour travailler avec de nouveaux groupes de patients. En effet, chaque nouveau groupe est généré à chaque exécution sans écraser l'ancien groupe.

5. **[requirements.txt](./requirements.txt)**  
   - Fichier texte contenant les librairies nécessaires à l'exécution du script principal.

---

## **Instructions d’Utilisation**

### **Prérequis**

Assurez-vous d'avoir installé et configuré les éléments suivants (de préférence sur Docker pour Kafka, Elasticsearch et Kibana) :  
- **Python 3.x**  
- **Kafka 6.2.0**
- **Zookeeper 6.2.0**  
- **Elasticsearch 7.9.1**  
- **Kibana 7.9.1**

Le fichier `requirements.txt` permet d'installer toutes les bibliothèques nécessaires au projet.

Pour éviter tout conflit, vous pouvez aussi installer les bibliothèques Python nécessaires pour des versions compatibles avec la commande suivante :

```bash
pip install -r requirements.txt
```

### **instruction d'usage**

# Ajuster la période temporelle et le nombre de patients dans Message_FHIR_Project

Ce projet génère des données de pression artérielle systolique (SYS) et diastolique (DIA) pour un groupe de patients sur une période donnée. Ce fichier `README` explique comment ajuster la période temporelle, le nombre de patients, et travailler avec différents groupes de patients.

## **1. Ajuster la période temporelle**

Vous pouvez augmenter la période temporelle dans le fichier `Message_FHIR_Project.py` en modifiant la valeur de la ligne suivante ```for i in range(500)```. Cela permet de travailler sur une période plus longue avec le même groupe de patients. Par exemple, lancer le script avec 1000 itérations génère des mesures de pression systolique (SYS) et diastolique (DIA) pour un groupe de patients sur une période moyenne de 6 ans (soit environ 2 à 3 mesures par an pour chaque patient).

## **2. Ajuster le nombre de patient**
Vous pouvez également augmenter le nombre de patients dans un groupe en modifiant la valeur dans la première boucle ```for i in range(100)```. Cela vous permet d'adapter le nombre de patients en fonction de la période que vous souhaitez étudier.

Si vous voulez une période plus courte, réduisez le nombre d'itérations dans le code (``for i in range(500)``).
Si vous souhaitez une période plus longue, augmentez la valeur d'itération.

## **3. Travaillez avec plusieurs groupes :**
Vous pouvez travailez avec plusieurs groupes de patients differents sur differentes perdiodes. Par exemple, vous pourrais trvailler sur un groupe de patient sur 2 ans et sur un autre groupe sur les 2 années suivante. pour cela, il faudra executer le script principal 2 fois. Les données generées précedemment ne sont pas ecraser et les nouvelle donnée debute a la date de la derniere observation du précedent groupe.

## **4. erreur courante :**

Parfois le code ne voudra pas ce lancer ou vous donnera des données fause ou mal indéxé. il faudra donc changer les topics kafka.

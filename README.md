# **Surveillance de la Pression Artérielle avec FHIR, Kafka, Elasticsearch et Kibana**

Bienvenue dans ce repository GitHub qui contient le code source et les fichiers d'un projet universitaire en Big Data.  
Ce projet implémente une solution complète pour surveiller les pressions artérielles des patients en temps réel, en utilisant les technologies modernes comme **FHIR**, **Kafka**, **Elasticsearch**, et **Kibana**.  

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
   - Exemple de fichier JSON contenant des messages FHIR de patients avec des pressions artérielles normales.  

---

## **Instructions d’Utilisation**  

### **Prérequis**  

Assurez-vous d'avoir installé et configuré les éléments suivants (de preférence sur Docker pour Kafka, ElasticSearch et Kibana)  :  
- **Python 3.x**  
- **Kafka 6.2.0**
- **Zookeeper 6.2.0**  
- **Elasticsearch 7.9.1**  
- **Kibana 7.9.1**

Le fichier requirement.txt permet d'installer toutes les bibilothèques necessaires à un projet. 

Pour eviter tout conflit, vous pouvez aussi installez les bibliothèques Python nécessaires pour des versions comptabiles avec la commande suivante : 
```bash
pip install -r requirements.txt
```



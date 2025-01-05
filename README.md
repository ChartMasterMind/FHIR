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
   - Exemple de fichier JSON crée après l'execution du script prinicpal et contenant des messages FHIR de patients avec des pressions artérielles normales.

4. **[dernière_date.txt](./dernière_date.txt)**
   - Exemple de Fichier texte qui est crée apres l'éxecution du script principal et contenant la dernière date de la dernière observation générée par le script : Ce fichier permet de relancer le script principal à partir de cette date à chaque exécution. Cela évite de lancer le script avec 1000 itérations si votre ordinateur est assez lent et est également utile pour travailler avec de nouveaux groupes de patients. En effet, chaque nouveau groupe est généré à chaque exécution sans écraser l'ancien groupe.


5. **[requirements.txt](./requirements.txt)**
- fichier txt contenant les librairies nécessaires à l'execution du script principal.

7.  **[DashBoard_Apercu_des_données.png](./DashBoard_Kibana/DashBoard_Apercu_des_données.png)**
- Dashboard kibana contenant les données générées

8. **[DashBoard_Données_filtrées_pour_un_patient.png](./DashBoard_Kibana/DashBoard_Données_filtrées_pour_un_patient.png)**
- Dashboard kibana contenant les données générées pour un seul patient (suivi de la tension artérielle d'un patient dans le temps)
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

# Instructions d'usage

## 1. Ajuster la période temporelle

Vous pouvez augmenter la période temporelle dans le fichier `Message_FHIR_Project.py` en modifiant la valeur dans la ligne `for i in range(500)`. Cela permet de travailler sur une période plus longue avec le même groupe de patients.

- Par exemple, lancer le script avec 1000 itérations génère des mesures de pression SYS et DIA pour un seul groupe de patients sur une période moyenne de **6 ans** (soit environ **2 à 3 mesures par an** pour chaque patient).

## 2. Ajuster le nombre de patients générés

Vous pouvez également augmenter le nombre de patients dans un groupe en modifiant la valeur dans la première boucle `for i in range`. Cela vous permet d'adapter le nombre de patients en fonction de la période que vous souhaitez étudier :

- Si vous voulez une période plus courte, réduisez le nombre d'itérations dans le code (ligne `for i in range(500)`).
- Si vous souhaitez une période plus longue, augmentez la valeur d'itération.

## 3. Travailler avec différents groupes de patients

Si vous préférez travailler avec plusieurs groupes de patients pour maintenir la diversité des données, voici deux options :

- **Travailler avec un grand nombre de patients sur une seule période** :
    - Augmentez le nombre de patients dans la boucle `for i in range(50)` et exécutez le code une seule fois.
    - Vous pourrez ajuster la durée de la période en modifiant le nombre d'itérations dans la deuxième boucle.

- **Travailler avec des groupes de patients distincts pour différentes périodes** :
    - Par exemple, analyser un groupe de patients sur 3 ans, puis un autre groupe pour les 3 années suivantes.
    - Dans ce cas, relancez le code deux fois pour travailler avec des groupes différents à des périodes distinctes.


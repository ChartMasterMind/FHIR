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
   - Script principal générant des messages FHIR

2. **[Message_FHIR_Project_explication.py](./Message_FHIR_Project_explication.py)**  
   - Fichier cide sans grande importance, inutile de l'ouvrir !

3. **[normal_blood_pressure.json](./normal_blood_pressure.json)**  
   - Exemple de fichier JSON crée après l'exécution du script principal et contenant des messages FHIR de patients avec des pressions artérielles normales.

4. **[dernière_date.txt](./dernière_date.txt)**  
   - Exemple de fichier texte créé après l'exécution du script principal et contenant la dernière date de la dernière observation générée par le script. Ce fichier permet de relancer le script principal à partir de cette date à chaque exécution. Cela évite de lancer le script avec 1000 itérations si votre ordinateur est assez lent et est également utile pour travailler avec de nouveaux groupes de patients. En effet, chaque nouveau groupe est généré à chaque exécution sans écraser l'ancien groupe.

5. **[requirements.txt](./requirements.txt)**  
   - Fichier texte contenant les librairies nécessaires à l'exécution du script principal.

6. **[product.py](./product.py)**
   - Fonction qui permet de recupérer les message FHIR et de les conserver dans un topics Kafka
     
7. **[consumer.py](./consumer.py)**
   -  Recupération et traitements des données sur Kafka et indexation des donnée des message FHIR contenant des anomalies dans Elasticsearch. Une autre fonction permet aussi de conserver les données normales dans le fichier **[normal_blood_pressure.json](./normal_blood_pressure.json)**
  
8. **[lancement.py](./lancement.py)**
   - Script qui permet de lancer simultanement les 3 scripts dont :  **[Message_FHIR_Project.py](./Message_FHIR_Project.py)**, **[product.py](./product.py)** et **[consumer.py](./consumer.py)**
  
9. **[docker-compose.yml](./docker-compose.yml)**
    - fichier qui permet d'installer et de conteneuriser les services Kibana, elasticsearch, kafka et zookeeper sur Docker Desktop
      
10.**[DashBoard_Apercu_des_données.png](./DashBoard_Apercu_des_données.png)**
   - Dashboard qui représente les données de pression artérielle normale pour un groupe de patients

11.**[DashBoard_Données_filtrées_pour_un_patient.png](./DashBoard_Données_filtrées_pour_un_patient.png)**
   - Dashboard qui représente les données de pression artérielle normale pour un seul patient pour un suivi medicale par exemple

12. **[project_big_data.pdf](./project_big_data.pdf)**
   - Ce document a pour objectif de détailler la configuration et l’interaction des différents fichiers utilisés dans notre projet, afin de vous offrir une compréhension approfondie de son fonctionnement.                                                                   



## **Instructions d’Utilisation**


Cette partie est consacré aux telechargements et à la configuration des packages essentielles au projet.

### **Prérequis**

Assurez-vous après avoir suivi les étapes d'instalation, d'avoir installé et configuré les éléments suivants et que les versions correspondent à celles mentionnés en dessous :
- **Python 3.x**  
- **Kafka 6.2.0**
- **Zookeeper 6.2.0**  
- **Elasticsearch 7.9.1**  
- **Kibana 7.9.1**

# Comment Lancer les script


## **1. Installer et lancer Docker Desktop**


Vous pouvez trouver le lien de Docker Desktop à cette adresse : https://www.docker.com/products/docker-desktop/


## **2. Crée un répertoire contenant tout les fichiers de ce github**


Vous pouvez par exemple exporter ce repository GitHub sur votre machine local à l'aide de cette commande : 

```bash
git clone https://github.com/ChartMasterMind/FHIR.git
```


## **3. Installer Kibana, elasticsearch, kafka et zookeeper sur Docker**


Cette étape vous permettra d'installer Kibana, Elasticsearch, Kafka et Zookeeper dans des conteneurs, ce qui rend l'installation et la gestion de ces services plus faciles. Le projet contient un fichier docker-compose.yml qui vous aide à configurer et lancer ces services en quelques commandes simples. Il vous suffit de suivre les instructions dans ce fichier pour démarrer rapidement tous les services nécessaires.

Pour cela, il vous faut lancer docker desktop et aller sur leur termnal intégré puis aller jusqu'au répertoire de travail (dossier qui contient le fichier **[docker-compose.yml](./docker-compose.yml)**)  à l'aide la commande et taper la commande :

```bash 
cd FHIR
```

puis suivi de :

```bash 
docker compose -p blood_pressure_project up
```

Puis lancé manuellement les conteneurs (recommandée) ou bien les lancés avec la commande:

```bash
docker compose start
```

## **4. Installer VS Code ou lancer les scripts depuis le terminal**

Pour utiliser ce projet, commencez par cloner ce repository GitHub sur votre machine locale. Une fois cela fait, vous pouvez lancer le script `lancement.py`, soit via le terminal, soit via Visual Studio Code.

### **Étapes à suivre** :

 ## 1. **Cloner le repository** :


   Si ce n'est pas déjà fait, clonez le repository en utilisant la commande suivante dans votre terminal :

   ```bash
   git clone https://github.com/ChartMasterMind/FHIR.git
   ```
   
 ## 2. **Lancer le script depuis le terminal**


   1. Ouvrez votre terminal.

   2. Naviguez jusqu'au dossier du repository cloné à l'aide de la commande ``` cd ```. Si le repository se nomme FHIR, alors taper la commande
      
   ```bash
   cd FHIR
   ```

   3. Exécutez le fichier `lancement.py` en utilisant la commande suivante :

   ```bash
   python lancement.py
   ```

    
 ## 3.** Lancer le script depuis Visual Studio Code (VS Code)**


   1. Ouvrez le dossier du repository dans VS Code.


   2. **Télecharger toutes les biblothèques nécessaire à l'aide du fichier requirement**. Le fichier `requirements.txt` permet d'installer toutes les bibliothèques nécessaires au projet. Donc pour éviter tout conflit, vous devez installer les bibliothèques Python.
    nécessaires pour des versions compatibles.

   Pour cela, ouvrez le terminal intégré de VScode avec le raccourci `CTRL J` et crée un environnment virtuelle à l'aide de la commande ( **IMPORTANT** : vérifier bien que vous vous trouver dans le répértoire de travail sur le terminal où sont stocké tout les fichiers du repositry GitHub )  :
   
   ```bash
   python -m venv nom_de_l_environnement
   ```
   ensuite activer cette evrionnement à l'aide la commande : 

   ```bash
   .\nom_de_l_environnement\Scripts\activate
   ```
   et enfin installer les bibliothèques Python à l'aide du fichier requirements sur cette envrionnement.
   
   ```bash
   pip install -r requirements.txt
   ```


   3. Ouvrez le fichier `lancement.py`.


   4. Cliquez sur l'icône de lecture (ou utilisez le raccourci `F5`) pour exécuter le script.

   Ce fichier `lancement.py` lance simultanément les scripts nécessaires pour générer, produire et consommer des messages en temps réel, intégrant ainsi toute la chaîne de traitement des données dans le cadre de ce projet.






# Ajuster la période temporelle et le nombre de patients dans Message_FHIR_Project

Ce projet génère des données de pression artérielle systolique (SYS) et diastolique (DIA) pour un groupe de patients sur une période donnée. Ce fichier `README` explique comment ajuster la période temporelle, le nombre de patients, et travailler avec différents groupes de patients.

## **1. Ajuster la période temporelle**

Vous pouvez augmenter la période temporelle dans le fichier `Message_FHIR_Project.py` en modifiant la valeur de la ligne suivante ```for i in range(500)```. Cela permet de travailler sur une période plus longue avec le même groupe de patients. Par exemple, lancer le script avec 1000 itérations génère des mesures de pression systolique (SYS) et diastolique (DIA) pour un groupe de patients sur une période moyenne de 6 ans (soit environ 2 à 3 mesures par an pour chaque patient).

## **2. Ajuster le nombre de patient**
Vous pouvez également augmenter le nombre de patients dans un groupe en modifiant la valeur dans la première boucle ```for i in range(100)```. Cela vous permet d'adapter le nombre de patients en fonction de la période que vous souhaitez étudier.

Si vous voulez une période plus courte, réduisez le nombre d'itérations dans le code (``for i in range(500)``).
Si vous souhaitez une période plus longue, augmentez la valeur d'itération.

## **3. Travaillez avec plusieurs groupes :**
Vous pouvez travailez avec plusieurs groupes de patients differents sur differentes perdiodes. Par exemple, vous pourrais travailler sur un groupe de patient sur 2 ans et sur un autre groupe sur les 2 années suivante. Pour cela, il faudra executer le script principal 2 fois. Les données generées précedemment ne sont pas ecraser et les nouvelle donnée debute a la date de la derniere observation du précedent groupe.


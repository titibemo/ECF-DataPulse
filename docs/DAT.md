#### Livrable 1.1 : Dossier d'Architecture Technique (DAT)


**1. Choix d'architecture globale**
- Quelle architecture proposez-vous ? (Data Lake, Data Warehouse, Lakehouse, base NoSQL, autre ?)
        Pour l'utilisation des différents scrapper : mongoDB sera utiliser pour stocker les données de manière persistantes. MinIO sera utilisé pour la sauvegarde des fichiers non traités (CSV, JSON...).
        Pour l'api : Une base de données PostgresSQL sera utilisé pour stocker les données.

- Pourquoi ce choix plutôt qu'une alternative ?
        Concernant le scraping, mongoDB est plus permissif permettra d'y ajouter ou non des données qui potentiellement ne sont pas présentes. MinIO permettra d'y sauvegarder des données complexes (Images), de pouvoir versionner nos documents.
        Concernant l'api: Les données récupérées via l'api permettent facilement de structurer les informations à envoyées (Ou non) à notre base de données. Il sera aussi plus facile de joindre une ou plusieurs table lors de la récupération des données.

- Quels sont les avantages et inconvénients de votre choix ?
    Pour le scraping, mongoDB permettra d'être flexible sur la sauvegarde de données (Au prix de quelques incohérences).
    Pour l'API, les données seront structurées efficacement avec toutes les informations souhaitées. Cependant, cela demandera de faire plus de traitement avant d'envoyer les données afin d'éviter les erreurs d'insertion.

**2. Choix des technologies**
- Quelles technologies utilisez-vous pour le stockage des données brutes ?
    Minio sera utilisé pour le stockage des données brutes, via les backups afin de récupérer les données si celle-ci ont été par exemple effacé ou mal traités.

- Quelles technologies utilisez-vous pour les données transformées ?
    Les données transformées seront stockées dans les bases de données PostgresSQL ou MongoDB, ces données pourront être utilisés pour divers traitements statistiques.


- Quelles technologies utilisez-vous pour l'interrogation SQL ? Justifiez.
    Pour mongoDB nous utiliseront pymongo et pour postgresSQL psycopg, librairies disponible avec Python.

- Comparez avec au moins une alternative pour chaque choix.

**3. Organisation des données**
- Comment organisez-vous les données dans votre architecture ?
    Suivant les options utilisées lors du lancement du script ainsi que les pipelines, les données seront stockées soit seulement dans les bases de données, soit aussi vers minIO.
    par exemple, l'option --export-csv permettra de sauvegader les données dans minIO dans le dossier export dans la pipeline quote.
    Concernant l'api, une backup sera

- Proposez-vous des couches de transformation ? Lesquelles et pourquoi ?
    Non, cependant nous pourrions pousser plus loin en utilisant l'architexture en médaillon via minIO en créant trois bucket spécifiques (Bronze, Silver et Gold) afin d'y ajouter dans l'ordre les données brutes, les données traités et les données prêt à être utilisées pour analyse ou sauvegarde en base de données.
    Actuellement, 3 buckets sont créés : 
    1. le bucket images contenant les images des scraper.
    2. le bucket export contenant les exports fait avec l'option --export-csv lors du lancement de la pipeline.
    3. le bucket backup contenant les backups fait avec l'option --backup lors du lancement de la pipeline ou automatiquement lancé lors de la pipeline excel.

- Quelle convention de nommage adoptez-vous ?
    Les données brutes seront stocké sous cette forme:
    PROVENANCE_DU_FICHIER_export_DATE.EXTENSION : exemple, quotes_export_20260105_102302.csv


**4. Modélisation des données**
- Quel modèle de données proposez-vous pour la couche finale ?
- Fournissez un schéma (diagramme entité-relation ou autre)
- Justifiez vos choix de modélisation

**5. Conformité RGPD**
- Quelles données personnelles identifiez-vous dans les sources ?
    Dans les sources, il y a la présence de données sensibles qui sont : contact_nom, contact_email, contact_telephone.

- Quelles mesures de protection proposez-vous ?
    Le réglement RGPD stipule :
    Le règlement européen interdit de recueillir ou d’utiliser ces données, sauf, notamment, dans les cas suivants :

    si la personne concernée a donné son consentement exprès (démarche active, explicite et de préférence écrite, qui doit être libre, spécifique, et informée) ;
    si les informations sont manifestement rendues publiques par la personne concernée ;
    si elles sont nécessaires à la sauvegarde de la vie humaine ;
    si leur utilisation est justifiée par l'intérêt public et autorisé par la CNIL ;
    si elles concernent les membres ou adhérents d'une association ou d'une organisation politique, religieuse, philosophique, politique ou syndicale. 

    Dans mon cas, je n'utilise pas les données, ces données seront exclus lors du traitement. Cependant, elles peuvent être anonymisées ou cryptés afin de les garder en base de données.

- Comment gérez-vous le droit à l'effacement ?
    Si une demande était amené à être envoyé par un utilisateur alors toutes données voulant être supprimées doivent être supprimées.
    https://www.cnil.fr/fr/comprendre-mes-droits/le-droit-leffacement-supprimer-vos-donnees-en-ligne
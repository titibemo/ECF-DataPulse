/* 1. Une requête d'agrégation simple */
SELECT
    AVG(ca_by_year) AS ca_moyen_annuel
FROM partner_library;

/* 2. Une requête avec jointure */
SELECT
    pl.nom_librairie,
    pl.ville,
    lg.latitude,
    lg.longitude
FROM partner_library pl
JOIN library_geocoding lg
    ON pl.id_partner_library = lg.id_partner_library;

/* 3. Une requête avec fonction de fenêtrage (window function) */


/* 4. Une requête de classement (top N) */
SELECT 
    name_library,
    city, 
    ca_by_year 
FROM partner_library 
ORDER BY ca_by_year DESC 
LIMIT 2;

/* 5. Une requête croisant au moins 2 sources de données */

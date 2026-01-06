/* 1. Une requête d'agrégation simple */
SELECT
    AVG(ca_by_year) AS ca_moyen_annuel
FROM partner_library;

/* 2. Une requête avec jointure */
SELECT
    pl.name_library,
    pl.city,
    geo.postcode,
    geo.citycode
FROM partner_library pl
JOIN geocoding geo
    ON pl.city = geo.city;
    
/* 3. Une requête avec fonction de fenêtrage (window function) */
SELECT
    name_library,
    city,
    ca_by_year,
    RANK() OVER (PARTITION BY city ORDER BY ca_by_year DESC) AS rank_ca_by_year
FROM partner_library;

/* 4. Une requête de classement (top N) */
SELECT 
    name_library,
    city, 
    ca_by_year 
FROM partner_library 
ORDER BY ca_by_year DESC 
LIMIT 2;

/* 5. Une requête croisant au moins 2 sources de données */
SELECT
    pl.name_library,
    pl.city,
    pl.ca_by_year,
    geo.postcode,
    geo.citycode
FROM partner_library pl
JOIN geocoding geo
    ON pl.city = geo.city

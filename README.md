# Data-mining-project (Shufersal)
### By Samuel Lederman & Ofir Shein Lumbroso

>data-mining-project repo contains a package of files that enables the user to scrab the data \
from the online supermarket site of the Shufersal chain: https://www.shufersal.co.il/online/he/S 

The scraped data will be inserted to the "shufersal" database, ERD diagram at *DERD Diagram - milestone 3.png* 



\
To run the scraper, one should run ***main.py***:\
**Usage:** main.py [-h] [-c] [-gl] [-url URL] [-all] [-translate TABLE COLUMN LANGUAGE=ENGLISH]
               

*Optional arguments:*\
  -h,  --help                          **show** this help message and exit \
  -c                                   **create** tables for "shufersal" database\
  -gl                                  **get** subcategories **links** to parse and fill category table \
  -url  URL                            **specific category url** from the "Shufersal" online site to parse and collect to the shufersal database \
  -all                                 get all links from category table, **parse and fill** "shufersal" database \
  -translate TABLE COLUMN LANGUAGE=ENGLISH \
                                       **translate** specific table and column from the "shufersal" database to the desired language (english by default).\


\
**USAGE EXAMPLES AND NOTES:**

\
**-c** :
- -c argument will create the tables for the "shufersal" database.

\
**-gl** :
- "shufersal" tables must exist before using the -gl argument.

\
**-url** :
- The url following the -url argument should be from the second sub category type, for example look at *sub_links.png*
- "shufersal" tables must be created before using the -url argument.
- The products in the url will be parsed and filed to the "shufersal" database.
- The given url will be inserted to the url column in the category table.
- Usage example: -url https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%A4%D7%99%D7%A8%D7%95%D7%AA-%D7%95%D7%99%D7%A8%D7%A7%D7%95%D7%AA/%D7%99%D7%A8%D7%A7%D7%95%D7%AA-%D7%95%D7%A4%D7%99%D7%A8%D7%95%D7%AA-%D7%9E%D7%A6%D7%95%D7%A0%D7%A0%D7%99%D7%9D/c/A0409

\
**-all** :
- "shufersal" tables must exist before using the -all argument.
- -all will parse all the acceptable urls from the category table. To fill the category table with all the acceptable links one should run the -gl command or alternatively use the -url argument.

\
**-translate** :
- The translate argument can be used with other arguments, in which case it will be implemented last, or by itself. 
- The translate argument will create a new column, if it does not exist, next to the translated column with the suffix "_language" 
- To see the available languages insert "languages" as the argument for LANGUAGE
- Usage example: -translate product_details name en 
-> translates table "product_details", column "name" and insert translation to english in column "name_en" 



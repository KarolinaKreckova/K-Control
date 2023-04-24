create database Objednavka;
use objednavka;                
CREATE TABLE IF NOT EXISTS zbozi (
id INT AUTO_INCREMENT PRIMARY KEY, 
pocet INT, 
popis VARCHAR(100), 
cena INT
);

CREATE TABLE IF NOT EXISTS Faktura (
id INT AUTO_INCREMENT PRIMARY KEY, 
jmeno VARCHAR(50), 
prijmeni VARCHAR(50), 
telefon VARCHAR(9), 
zbozi_id INT, 
FOREIGN KEY (zbozi_id) REFERENCES zbozi(id))
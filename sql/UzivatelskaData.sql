create database uzivatelskadata;
use uzivatelskadata


create table zbozi_sklad(
id int auto_increment primary key,
cislo int not null,
nazev varchar(50) not null,
kod varchar(50) not null,
pocet int,
cena int
)
create table email(
id int auto_increment primary key,
odesilatel varchar(50),
komu varchar(50),
predmet varchar(50),
obsah varchar (50),
poznamka varchar(50),
nutnost varchar(10)
);
create table uzivatel(
id int auto_increment primary key not null, 
username varchar (50), 
password varchar(40), 
role varchar(45)
)

insert into 
select*from zbozi

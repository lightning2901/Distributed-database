# Distributed-database
A project to have a database on 2 or plus devices wich can have a communication via network and do querys and inserts between them.

## Members and contact
José Ángel López Gutiérrez -> jalg030119@gmail.com


Carlos Daniel Camilo Aguilar -> mordexcamiloaguilar878689@gmail.com

## Affiliation
This is a project of the Distributed dadabases course of the Universidad Nacional Autónoma de México (UNAM), at the Escuela Nacional de Estudios Superiores Unidad Morela (ENES - Morelia).This project is carried out by students of the Bachelor's Degree in Technologies for Information in Sciences.

### Introduction
The idea of this project is to put it to use the knowledges learned in the course to develop a system of distributed databases, wich has the ability to interact on multiple databases at the same time as long as they are connected (through internet).
Our system is being developed on linux machines, and relays on using python for coding and making some user interaction, Mariadb server to be able to connect different systems and HTML to get a graphical interface of the system. 

### System Architecture and logic

The idea is: Each machine has a local mariadb server running, and in there is also a DB that is the same on structure on every other machine. We most emphasize that having the same database is a Requirement for the system to eork When the system starts, it'll look for more systems connected to the nerwork.

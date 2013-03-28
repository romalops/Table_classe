import sqlite3
from readDoc import *

class Db(object):
     def __init__(self):
          self.conn = sqlite3.connect("db.sqlite")
          self.cur = self.conn.cursor()

          try:
               sqr = "CREATE TABLE prof (id_prof INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT)"
               self.cur.execute(sqr)
               sqr = "CREATE TABLE classe (id_classe INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT)"
               self.cur.execute(sqr)
               sqr = "CREATE TABLE cours (id_cours INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, heure INTEGER, fraction INTEGER, id_classe INTEGER)"
               self.cur.execute(sqr)
          
          except:
               pass
               print("Base de données déjà existante.")

     def enregistrerProf (self, cheminFichier, nom=None, prenom=None,):
          fichier = open(cheminFichier, "r")
          i = 1
          while(1):
               ligne = fichier.readline()
               if ligne=="":
                   break
               prof = ligne[0:len(ligne)-1].split(";")
               sqr = "INSERT INTO prof VALUES(NULL, ?, ?)"
               self.cur.execute(sqr, (prof[0], prof[1]))
               print("Enregistrement {} effectué" .format(i))
               i+=1
               
     def lireProf(self):
          self.cur.execute("SELECT * FROM prof")
          
          for it in self.cur:
               print(it[0], it[1], it[2])
          self.enregistreAll()

     def enregistrerClasse(self, cheminFichier):
          classe = open("nomClasse.txt", "r")
          i = 1
          while(1): 
               ligne = classe.readline()
               if ligne == "" :
                    break
               sqr = "INSERT INTO classe (id_classe, nom) VALUES(NULL, ?)"
               self.cur.execute(sqr, [ligne[0:len(ligne)-1]]) ### [x] POUR -8 caractères
               print("Enregistrement {} effectué" .format(i))
               i+=1

     def lireClasse(self):
          self.cur.execute("SELECT * FROM classe")

          for it in self.cur:
               print(it[0], it[1])
          self.enregistreAll()

     def enregistrerCours(self):
          fichier = open("cours.txt")
          i = 1
          while(1):
               ligne = fichier.readline()
               if ligne == "":
                   break
               lst = ligne.split(";")
               nom = lst[0]
               heure = lst[1]
               fraction = None
               sqr = "SELECT nom, heure FROM cours"
               self.cur.execute(sqr)
               bool = 1
               for it in self.cur:
                    if nom == it[0] and heure == it[1]:
                         print("Données déjà existante dans la table cours")
                         bool = 0
                    else:
                         bool = 1
               if (bool == 1):
                    sqr = "INSERT INTO cours VALUES(NULL, ?, ?, ?, NULL)"
                    self.cur.execute(sqr, (nom, heure, fraction))
                    print("Enregistrement {} effectué" .format(i))
               i+=1   
          
     def afficheCours(self):
          self.cur.execute("SELECT * FROM cours")
          for it in self.cur:
               print(it)
          self.enregistreAll()
          
     def enregistreAll(self):
          choix = input("<Enter> Pour enregistrer ")
          if choix == "":
               self.conn.commit()
               
if __name__ == "__main__":
     db = Db()
     #db.enregistrerProf("profs.txt")
     db.lireProf()
     #db.enregistrerClasse("classe.txt")
     db.lireClasse()
     #db.enregistrerCours()
     db.afficheCours()




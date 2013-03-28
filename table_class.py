from tkinter import *
import tkinter.font
from db import *

LARGEUR_ROOT = 1563
HAUTEUR_ROOT = 800
LARGEUR_CLASSE = 900
HAUTEUR_CLASSE = 100
LARGEUR_COURS = 900
HAUTEUR_COURS = 600

class Classe(Frame):
        def __init__(self, master=None):
                Frame.__init__(self, master)
                self.grid(row=1,column=1,sticky=NSEW)
                self.configure(bg="red", width=LARGEUR_CLASSE, height=HAUTEUR_CLASSE)
                self.grid_propagate(False)
                self.save = Button(self, text="Sauvegarder", command=self.save)
                self.save.grid(row=1, column=3, sticky=W)
                self.quitter = Button(self, text="Quitter", command=master.destroy)
                self.quitter.grid(row=1, column=4, padx=10)
                cadreLB = Frame(self)
                self.bListe = Listbox(cadreLB, height=5, width=20)
                scrol = Scrollbar(cadreLB, command=self.bListe.yview)
                self.bListe.config(yscrollcommand=scrol.set)
                self.bListe.pack(side=LEFT)
                self.bListe.bind("<Double-1>", self.sortieClic)
                self.bListe.bind("<Return>", self.sortieClic)
                scrol.pack(expand=YES, fill=Y)
                cadreLB.grid(row=1, column=2, padx=30, pady=10)
                cadreLB.configure(bg="red")     
                self.bListe.delete(0, END)
                self.nomClasse = []
                db.cur.execute("SELECT * FROM classe")
                for it in db.cur:
                        self.bListe.insert(END, "{}" .format(it[1]))
                        self.nomClasse.append(it[1])
                self.largeur = Entry(self)
                self.largeur.insert(END, self.nomClasse[0])
                self.largeur.bind("<Return>", self.sortieTouche)
                self.largeur.grid(row=1, column=1, padx=10)

        def sortieClic(self, event=None):
                index = self.bListe.curselection()
                ind0 = int(index[0])
                self.item = self.nomClasse[ind0]
                self.largeur.delete(0, END)
                self.largeur.insert(END, self.item)
                FEN_cours.afficheMatiere(self.largeur.get())

        def sortieTouche(self, event=None):
                FEN_cours.afficheMatiere(self.largeur.get())
                
        def save(self):
                fichier = open("classe_save/"+self.largeur.get()+".txt", "a")
                for it in range(20):
                        if str(FEN_cours.nomMatiere[it]) != "":
                                fichier.write(str(FEN_cours.nomMatiere[it])+" --- "+str(FEN_cours.listeprofs[it].get())+"\n")
                fichier.write("\n******** FIN DE SAUVEGARDE ********\n\n")
                fichier.close()
        

class Cours(Frame):
        def __init__(self, master=None):
                Frame.__init__(self, master)
                self.grid(row=2,column=1, rowspan=3)
                self.can=Canvas(self,bg='pink',width=900,height=600,scrollregion=(0,0,900,900)) 
                self.vbar=Scrollbar(self,orient=VERTICAL)
                self.vbar.pack(side=RIGHT,fill=Y)
                self.vbar.config(command=self.can.yview)          
                self.can.config(width=900,height=700)
                self.can.config(yscrollcommand=self.vbar.set)
                self.can.pack(side=LEFT,expand=True,fill=BOTH)   
                self.MATIERE = []
                self.listeprofs=[]
                self.listebouttons1 = []
                self.listebouttons2 = [] 
                self.police = tkinter.font.Font(self, size=11, family='Courier')
                self.y=40
                for it in range(21):
                        self.matiere = Entry(self.can,bg="purple",font=self.police,width=20)
                        self.choisir1=Button(self.can,text="+",fg="black",font=self.police, command = lambda choix=it:self.numCours(choix))
                        self.choisir2=Button(self.can,text="+",fg="black",font=self.police, command = lambda choix=it:self.numProf(choix))
                        self.prof=Entry(self.can,bg="purple",font=self.police,width=20)
                        self.fa = self.can.create_window(220, self.y, window =self.matiere, width=400)
                        self.fb = self.can.create_window(450, self.y, window =self.choisir1)
                        self.fb = self.can.create_window(750, self.y, window =self.choisir2)
                        self.fc = self.can.create_window(600, self.y, window =self.prof)
                        self.MATIERE.append(self.matiere)
                        self.listeprofs.append(self.prof)
                        self.listebouttons1.append(self.choisir1)
                        self.listebouttons2.append(self.choisir2)
                        self.y+=40

        def numCours(self, o):
                self.o = o
                self.listebouttons1[o].configure(fg="red") 
        def numProf(self ,n):
                self.n = n
                self.listebouttons2[n].configure(fg="red")
        
        def afficheMatiere(self, classe="1ASM"):        
                db.cur.execute("SELECT * FROM classe")
                for it in range(len(self.nomMatiere)):
                        self.MATIERE[it].configure(text=self.nomMatiere[it])
                        self.fa = self.can.create_window(220, self.y, window =self.matiere, width=400)             
                        self.y+=40

        def signaleErreur(self):
                FEN_classe.largeur.configure(bg="blue")
                FEN_classe.largeur.delete(0, len(FEN_classe.largeur.get()))
                FEN_classe.largeur.insert(END, "Cette classe n'existe pas")
                root.after(1500, self.videEntree)
                
        def videEntree(self):
                FEN_classe.largeur.configure(bg="white")
                FEN_classe.largeur.delete(0, len(FEN_classe.largeur.get()))

class ListeCours(Frame):
        def __init__(self, master=None):
                Frame.__init__(self, master)
                self.grid(row=1,column=2, rowspan=2,sticky=NSEW)
                self.configure(bg="pink",height=900,width=290)
                self.liste = Listbox(self, height=40, width=30,bg="ivory",font="Courier")
                self.scroll = Scrollbar(self, command=self.liste.yview)
                self.liste.configure(yscrollcommand=self.scroll.set)
                self.liste.grid(row=1,column=1)
                self.liste.bind('<Double-1>', self.clic)
                self.scroll.grid(row=1,column=2,sticky=NSEW)
                self.remplir(self.liste)
                
        def remplir(self, lst):
                lst.delete(0, END)
                db.cur.execute("SELECT * FROM cours")
                for it in db.cur:
                        lst.insert(END, "{} : {}" .format(it[1], it[2]))

        def clic(self, event=None):
                cours = self.liste.get(self.liste.curselection())
                FEN_cours.MATIERE[FEN_cours.o].delete(0, END)
                FEN_cours.MATIERE[FEN_cours.o].insert(END, cours)
                FEN_cours.listebouttons1[FEN_cours.o].configure(fg="black")

class Profs(Frame):
        def __init__(self, master=None):
                Frame.__init__(self, master)
                self.grid(row=1,column=3,rowspan=2,sticky=NSEW)
                self.configure(bg="pink",height=900,width=290)
                self.liste = Listbox(self, height=40, width=30,bg="ivory",font="Courier")
                self.scroll = Scrollbar(self, command=self.liste.yview)
                self.liste.configure(yscrollcommand=self.scroll.set)
                self.liste.grid(row=1,column=1)
                self.liste.bind('<Double-1>', self.clic)
                self.scroll.grid(row=1,column=2,sticky=NSEW)
                self.remplir(self.liste)
                
        def remplir(self, lst):
                lst.delete(0, END)
                db.cur.execute("SELECT * FROM prof")
                for it in db.cur:
                        lst.insert(END, "{} : {} {}" .format(it[0], it[1], it[2]))
        
        def clic(self, event=None):
                profChoisi = FEN_profs.liste.get(FEN_profs.liste.curselection())
                FEN_cours.listeprofs[FEN_cours.n].delete(0, END)
                FEN_cours.listeprofs[FEN_cours.n].insert(END, profChoisi)
                FEN_cours.listebouttons2[FEN_cours.n].configure(fg="black")

class MenuBar(Frame):
        def __init__(self, master=None):
                Frame.__init__(self, borderwidth=3, bg="black")
                self.grid(row=3, column=2, rowspan=3, columnspan=3)
                self.can = Canvas(self, bg="grey", width=315, height=25)
                self.can.grid(row=0, column=0, rowspan=3, columnspan=3)
                fileProf = Menubutton(self, text="Profs", bg="grey")
                fileProf.grid(row=1, column=0)
                me1 = Menu(fileProf)
                me1.add_command(label="Ajouter un prof", underline=0, command=lambda l=300,h=200,c=1:self.para(l,h,c))
                me1.add_command(label="Modifier un prof", underline=0, command=lambda l=300,h=200,c=2:self.para(l,h,c))
                me1.add_command(label="Supprimer un prof", underline=0, command=lambda l=300,h=200,c=3:self.para(l,h,c))
                fileProf.configure(menu = me1)

        def para(self,largeur, hauteur, choix):
                fen2 = Parametre(largeur, hauteur, choix)
class Parametre(Tk):
        def __init__(self, largeur, hauteur, c):
                Tk.__init__(self)
                self.frame = Frame(self, width=largeur, height=hauteur)
                self.frame.grid()
                if c == 1:
                        self.addProf()
                elif c == 2:
                        self.modProf()
                elif c == 3:
                        self.delProf()
                elif c == 4:
                        self.addClasse()
                self.mainloop()

        def addProf(self):
                self.title("Ajouter un prof")
                self.nom = Label(self.frame, text="Nom :")
                self.nom.grid(row=1, column=1, sticky=W, padx=10, pady=10)
                self.prenom = Label(self.frame, text="Prénom :")
                self.prenom.grid(row=2, column=1, sticky=W, padx=10, pady=10)
                self.nom2 = Entry(self.frame)
                self.nom2.grid(row=1, column=2, sticky=W, padx=10, pady=10)
                self.prenom2 = Entry(self.frame)
                self.prenom2.grid(row=2, column=2, sticky=W, padx=10, pady=10)
                self.save = Button(self, text="Enregistrer", command= lambda c=1:self.enregistrer(c))
                self.save.grid(row=3, padx=5, pady=5)
                self.info = Label(self.frame, text="")
                self.info.grid(row=4, column=2)

        def modProf(self):
                self.title("Modifier un prof")
                self.nom = Label(self.frame, text="Nom :")
                self.nom.grid(row=1, column=1, sticky=W, padx=10, pady=10)
                self.prenom = Label(self.frame, text="Prénom :")
                self.prenom.grid(row=2, column=1, sticky=W, padx=10, pady=10)
                self.nom2 = Entry(self.frame)
                self.nom2.grid(row=1, column=2, sticky=W, padx=10, pady=10)
                self.prenom2 = Entry(self.frame)
                self.prenom2.grid(row=2, column=2, sticky=W, padx=10, pady=10)
                self.prof = Label(self.frame, text="Profs à modifier")
                self.prof.grid(row=3, column=1, sticky=W, padx=10, pady=10)
                self.prof2 = Entry(self.frame)
                self.prof2.grid(row=3, column=2, sticky=W, padx=10, pady=10)
                self.liste = Listbox(self.frame, height=10, width=30,bg="ivory")
                self.scroll = Scrollbar(self.frame, command=self.liste.yview)
                self.liste.configure(yscrollcommand=self.scroll.set)
                self.liste.grid(row=1,column=3, rowspan=3, columnspan=3, padx=10, pady=10)
                self.liste.bind('<Double-1>', self.clic)
                self.scroll.grid(row=1,column=4,sticky=NSEW, rowspan=3, columnspan=3, pady=10)
                FEN_profs.remplir(self.liste)
                self.info = Label(self.frame, text="")
                self.info.grid(row=4, column=2)
                self.save = Button(self, text="Modifier", command= lambda c=2:self.enregistrer(c))
                self.save.grid(row=5, padx=5, pady=5)

        def clic(self, event=None):
                profChoisi = self.liste.get(self.liste.curselection()).split(" ")
                self.nom2.delete(0, END)
                self.prenom2.delete(0, END)
                self.prof2.delete(0, END)
                self.nom2.insert(END, "{}" .format(profChoisi[2]))
                self.prenom2.insert(END, "{}" .format(profChoisi[3]))
                self.prof2.insert(END, "{} {}" .format(profChoisi[2], profChoisi[3]))

        def delProf(self):
                self.title("Supprimer un prof")
                self.prof = Label(self.frame, text="Profs à supprimer")
                self.prof.grid(row=3, column=1, sticky=W, padx=10, pady=10)
                self.prof2 = Entry(self.frame)
                self.prof2.grid(row=3, column=2, sticky=W, padx=10, pady=10)
                self.liste = Listbox(self.frame, height=10, width=30,bg="ivory")
                self.scroll = Scrollbar(self.frame, command=self.liste.yview)
                self.liste.configure(yscrollcommand=self.scroll.set)
                self.liste.grid(row=1,column=3, rowspan=3, columnspan=3, padx=10, pady=10)
                self.liste.bind('<Double-1>', self.clic2)
                self.scroll.grid(row=1,column=4,sticky=NSEW, rowspan=3, columnspan=3, pady=10)
                FEN_profs.remplir(self.liste)
                self.info = Label(self.frame, text="")
                self.info.grid(row=4, column=2)
                self.save = Button(self, text="Supprimer", command= lambda c=3:self.enregistrer(c))
                self.save.grid(row=5, padx=5, pady=5)

        def clic2(self, event=None):
                profChoisi = self.liste.get(self.liste.curselection()).split(" ")
                self.prof2.delete(0, END)
                self.prof2.insert(END, "{} {}" .format(profChoisi[2], profChoisi[3]))

        def affClasse(self):
                self.title("Ajouter une classe")
                self.nom = Label(self.frame, text="Nom :")
                self.nom.grid(row=1, column=1, sticky=W, padx=10, pady=10)
                self.nom2 = Entry(self.frame)
                self.nom2.grid(row=1, column=2, sticky=W, padx=10, pady=10)
                self.save = Button(self, text="Enregistrer", command= lambda c=4:self.enregistrer(c))
                self.save.grid(row=3, padx=5, pady=5)
                self.info = Label(self.frame, text="")
                self.info.grid(row=4, column=2)
                
        def enregistrer(self, choix):
                if choix == 1:
                        sqr = "INSERT INTO prof VALUES(NULL, ?, ?)"
                        db.cur.execute(sqr, (self.nom2.get(), self.prenom2.get()))
                        FEN_profs.remplir(FEN_profs.liste)
                        self.destroy()
                if choix == 2:
                        try:
                                profChoisi = self.prof2.get().split(" ")
                                sqr = "UPDATE prof SET nom ='{}' WHERE nom LIKE '{}'" .format(self.nom2.get(), profChoisi[0])
                                db.cur.execute(sqr)
                                sqr = "UPDATE prof SET prenom ='{}' WHERE prenom LIKE '{}'" .format(self.prenom2.get(), profChoisi[1])
                                db.cur.execute(sqr)
                                FEN_profs.remplir(FEN_profs.liste)
                                self.destroy()
                        except:
                                self.prof2.delete(0, END)
                                self.prof2.insert(END, "ERREUR")
                if choix == 3:
                        try:
                                profChoisi = self.prof2.get().split(" ")
                                sqr = "DELETE FROM prof WHERE nom LIKE '{}' AND prenom LIKE '{}'" .format(profChoisi[0], profChoisi[1])
                                db.cur.execute(sqr)
                                FEN_profs.remplir(FEN_profs.liste)
                                self.destroy()
                        except:
                                self.prof2.delete(0, END)
                                self.prof2.insert(END, "ERREUR")

if __name__ == "__main__":   
        root = Tk()
        root.title("Gestion d'attribution des professeurs")
        root.geometry("{}x{}" .format(LARGEUR_ROOT, HAUTEUR_ROOT))
        db = Db()
        FEN_classe = Classe(root)
        FEN_cours = Cours(root)
        FEN_listeCours = ListeCours(root)
        FEN_profs = Profs(root)
        FEN_menu = MenuBar(root)
        root.mainloop()

def readDoc(chemin):
    File = open("{}" .format(chemin), "r")
    liste = []
    tamp = []
    while 1:
        ligne = File.readline()
        if ligne == "":
            break

        if ";" in ligne:
            tamp = ligne[0:len(ligne)-1].split(";")
            liste.append((tamp[0], tamp[1]))
        else:
            if ligne[0] in "0123456789":
                liste.append(ligne[0:len(ligne)-1])

            if ligne == "///\n":
                liste.append("END")
        
        

    return liste

if __name__ == "__main__":
    print(readDoc("classe.txt"))
    

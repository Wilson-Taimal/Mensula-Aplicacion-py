# FUNCIÓN DIÁMETRO BARRAS DE REFUERZO
# Nb: Número de la barra
# db: Diámetro de la barra _ cm

def f_db(Nb):
    Nb = Nb
#    print ('Nb =',Nb)
    match Nb:
        case 2:
            db = 0.64
        case 3:
            db = 0.95
        case 4:
            db = 1.27
        case 5:
            db = 1.59
        case 6:
            db = 1.91
        case 7:
           db = 2.22
        case 8:
            db = 2.54
        case _ :
            print ('Nb no valido')
    return (db)
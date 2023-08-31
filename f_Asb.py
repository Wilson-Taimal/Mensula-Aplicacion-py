# FUNCIÓN AREA BARRAS DE REFUERZO
# Nb: Número de la barra
# Asb: Área de la barra _ cm²

def f_Asb(Nb):
    Nb = Nb
#    print ('Nb =',Nb)
    match Nb:
        case 2:
            Asb = 0.32
        case 3:
            Asb = 0.71
        case 4:
            Asb = 1.29
        case 5:
            Asb = 1.99
        case 6:
            Asb = 2.84
        case 7:
           Asb = 3.87
        case 8:
            Asb = 5.10
        case _ :
            print ('Nb no valido')
    return (Asb)
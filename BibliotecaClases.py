# Biblioteca de clases para el diseño de mensulas

class Materiales():
    def __init__ (self):
        self.fc = 1.0           # Resistencia del concreto a compresión  _ [MPa]
        self.fy = 1.0           # Esfuerzo de fluencia del refuerzo _ [MPa]
        self.u = 1.0            # Coeficiente de fricción
        self.phiv = 1.0         # Factor de reducción a cortante
        self.phif = 1.0         # Factor de reducción a flexión y/o tracción


class Geometria():
    def __init__ (self):
        self.c = 1.0            # Ancho de la ménsula _ [cm]
        self.b = 1.0            # Ancho del soporte (muro) _ [cm]
        self.av = 1.0           # Dist. al punto de aplicación de la carga _ [cm]
        self.h = 1.0            # Altura de la ménsula _ [cm]
        self.r = 1.0            # Recubrimiento del refuerzo _ [cm]
        self.bw = 1.0           # Largo de la mensula _ [cm]
        self.d = 1.0            # Altura efectiva _ [cm]
        self.hmin = 1.0         # Altura mínima = 0.5*d _ [cm]


class Cargas():
    def __init__ (self):
        self.Vu = 1.0          # Fuerza cortante mayorada  _ [kN]
        self.Nuc = 1.0         # Fuerza horizontal a tracción mayorda  _ [kN]
        self.Nuc1 = 1.0        # Fuerza horizontal a tracción dato de entrada  _ [kN]
        self.Nuc2 = 1.0        # Fuerz horizontal a tracción dato calculado  _ [kN]
        self.Mu = 1.0          # Momento flector mayorado _ [kN]

    def Ec_Mu(self, Vu, av, Nuc, h, d):
        Mu = (Vu*av) + Nuc*(h-d)
        return Mu


class Refuerzo():
    def __init__ (self):
        self.Nb = 1.0           # Número de la barra refuerzo principal
        self.Nbs = 1.0          # Número de la barra refuerzo auxiliar
        self.Nbe = 1.0          # Número de la barra para estribos
        self.db = 1.0           # Diámetro de la barra refuerzo principal _ [cm]
        self.dbs = 1.0          # Diámetro de la barra refuerzo auxiliar _ [cm]
        self.dbe = 1.0          # Diámetro de la barra para estribos _ [cm]
        self.Asb = 1.0          # Área sec. tranv. de la barra refuerzo principal _ [cm²]
        self.Asba = 1.0         # Área sec. tranv. de la barra refuerzo auxiliar _ [cm²]
        self.Asbe = 1.0         # Área sec. tranv. de la barra para estribos _ [cm²]
        self.cant = 1.0         # cantida de barras usadas ref principal _ [kN]
        self.s = 1.0            # separación entre barras ref principal _ [kN]
        self.canta = 1.0        # cantida de barras usadas ref auxiliar _ [kN]
        self.sa = 1.0           # separación entre barras ref auxiliar _ [kN]
        self.cante = 1.0        # cantida de barras usadas para estribos _ [kN]
        self.se = 1.0           # separación entre barras para estribos _ [kN]
        self.Refp = 1.0         # Distribución refuerzo principal
        self.Refa = 1.0         # Distribución refuerzo auxiliar
        self.Refe = 1.0         # Distribución de estribos

    def f_db(self, Nb):
        Nb = Nb
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
        return db

    def f_As(self, Nb):
        Nb = Nb
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
        return Asb

class Calculos():
    def __init__ (self):
        self.Vc = 1.0           # Resistencia al corte _ [kN]
        self.Vc1 = 1.0          # Resistencia al corte Ecu1 _ [kN]
        self.Vc2 = 1.0          # Resistencia al corte Ecu2 _[kN]
        self.Vc3 = 1.0          # Resistencia al corte Ecu3 _[kN]
        self.Avf = 1.0          # Refuerzo necesario para resistir Vu [cm²]
        self.An = 1.0           # Refuerzo necesario para resistir Nuc [cm²]
        self.Af = 1.0           # Refuerzo necesario para resistir Mu [cm²]
        self.As = 1.0           # Refuerzo prinsipal que se debe disponer [cm²]
        self.As1 = 1.0          # Refuerzo prinsipal. Ecu1 _[cm²]
        self.As2 = 1.0          # Refuerzo prinsipal. Ecu2 _[cm²]
        self.As3 = 1.0          # Refuerzo prinsipal. Ecu3 _[cm²]
        self.Aa = 1.0           # Refuerzo auxiliar [cm²]
        self.Ah = 1.0           # Refuerzo para estribos [cm²]
        self.Ascol = 1.0        # Area de acero colocado [cm²]
        self.hde = 1.0          # Altura para la distribución de estribos _ [cm]
        self.pcal = 1.0         # Cuantía de refuerzo calculada _ [cm]
        self.pmin = 1.0         # Cuantía de refuerzo mínima _ [cm]
        self.lw = 1.0           # Longitud lateral de la soldadura _ [cm]
        self.tw = 1.0           # Longitud transversal de la soldadura _ [cm]


    def Ec_Vc1(self, phiv, fc, bw, d):
        Vc1 = 0.2 * phiv * (fc/10) * bw * d
        return Vc1

    def Ec_Vc2(self, fc, phiv, bw, d):
        Vc2 = ((3.3 + 0.08 * fc) * phiv * bw * 10 * d * 10) / 1000
        return Vc2

    def Ec_Vc3(self, phiv, bw, d):
        Vc3 = 11 * phiv * bw * d
        return Vc3

    def Ec_Avf(self, Vu, phiv, fy, u):
        Avf = Vu / (phiv * (fy/10) * u)
        return Avf

    def Ec_An(self, Nuc, phif, fy):
        An = Nuc / (phif * (fy/10))
        return An

    def Ec_Af(self, Mu, phif, fy, d, av):
        Af = Mu / (phif * (fy/10) * (d - av / 2))
        return Af

    def Ec_Ah(self, As, An):
        Ah = 0.5 * (As - An)
        return Ah

class Chequeos():
    def __init__(self):
        self.relacion_ad = 1.0
        self.Nuc_menor_Vu = 1.0
        self.Vu_menor_Vc = 1.0
        self.pcal_mayor_pmin = 1.0
from BibliotecaClases import*
import math
import numpy as np
import pandas as pd

material = Materiales()
geom = Geometria()
carga = Cargas()
ref = Refuerzo()
calculo = Calculos()
chequeo = Chequeos()

# Propiedades de los materiales
material.fc = 24.5
material.fy = 420
material.u = 1.4
material.phiv = 0.75
material.phif = 0.75

# Numero de barras a usar
ref.Nb = 6
ref.Nbe = 4

# Geometría
geom.av = 25
geom.b = 30
geom.c = 47.5
geom.h = 60
geom.r = 3
geom.bw = 125

geom.d = geom.h - geom.r
geom.hmin = 0.5*geom.d
if ( (geom.av/geom.d) < 1):
    chequeo.relacion_ad = 'Ok'
else:
    chequeo.relacion_ad = 'No cumple'

# Cargas de diseño
carga.Vu = 475.6
carga.Nuc1 = 16.6

if (carga.Nuc1 <= carga.Vu):
    chequeo.Nuc_menor_Vu = 'Ok'
else:
    chequeo.Nuc_menor_Vu = 'No cumple'

carga.Nuc2 = 0.2*carga.Vu
carga.Nuc = max(carga.Nuc1, carga.Nuc2)
carga.Mu = carga.Ec_Mu(carga.Vu, geom.av, carga.Nuc, geom.h, geom.d)

# Verificación Vu
calculo.Vc1 = calculo.Ec_Vc1(material.phiv, material.fc, geom.bw, geom.d)
calculo.Vc2 = calculo.Ec_Vc2(material.fc, material.phiv, geom.bw, geom.d)
calculo.Vc3 = calculo.Ec_Vc3(material.phiv, geom.bw, geom.d)
calculo.Vc = min(calculo.Vc1, calculo.Vc2, calculo.Vc3)
if (carga.Vu <= calculo.Vc):
    chequeo.Vu_menor_Vc = 'Ok'
else:
    chequeo.Vu_menor_Vc = 'No cumple'

# Refuerzo principal, auxiliar y estribos
calculo.Avf = calculo.Ec_Avf(carga.Vu, material.phiv, material.fy, material.u)
calculo.An = calculo.Ec_An(carga.Nuc, material.phif, material.fy)
calculo.Af = calculo.Ec_Af(carga.Mu, material.phif, material.fy, geom.d, geom.av)
calculo.As1 = calculo.Af + calculo.An
calculo.As2 = 2/3*calculo.Avf + calculo.An
calculo.As3 = 0.04*(material.fc/material.fy)*geom.bw*geom.d
calculo.As = max(calculo.As1, calculo.As2, calculo.As3)
calculo.Aa = 0.002*geom.bw*geom.c
calculo.Ah = calculo.Ec_Ah(calculo.As, calculo.An)

# Distribucion refuerzo principal
ref.Asb = ref.f_As(ref.Nb)
ref.Cant = math.ceil(calculo.As/ref.Asb)
ref.s = round((geom.bw-10)/(ref.Cant-1),0)

# Distribucion refuerzo auxiliar
ref.Asba = ref.f_As(ref.Nb)
ref.Canta = math.ceil(calculo.Aa/ref.Asba)
ref.sa = round((geom.bw-10)/(ref.Canta-1),0)

# Distribucion estribos
ref.Asbe = ref.f_As(ref.Nbe)
ref.Cante = math.ceil(calculo.Ah/ref.Asbe)
ref.se = round((2/3*geom.d)/(ref.Cante),0)

# Verificación refuerzo mínimo
calculo.Ascol = ref.Asb * ref.Cant
calculo.pcal = calculo.Ascol/(geom.bw * geom.d)
calculo.pmin = 0.04 * material.fc/material.fy
if (calculo.pcal >= calculo.pmin):
    chequeo.pcal_mayor_pmin = 'Ok'
else:
    chequeo.pcal_mayor_pmin = 'No cumple'

# Distribución refuerzo
ref.Refp = str(ref.Cant) + ' barras N°' + str(f'{ref.Nb}') + ' C/ ' + str(f'{ref.s}') + ' cm'
ref.Refa = str(ref.Canta) + ' barras N°' + str(f'{ref.Nb}') + ' C/ ' + str(f'{ref.sa}') + ' cm'
ref.Refe = str(ref.Cante) + ' barras N°' + str(f'{ref.Nbe}') + ' C/ ' + str(f'{ref.se}') + ' cm'

# Detalles soldadura
ref.db = ref.f_db(ref.Nb)
calculo.lw = 3/4 * ref.db
calculo.tw = 1/2 * ref.db


# ================================================================================================ #
# REPORTE EN EXCEL #

print ('\nDISEÑO ESTRUCTURAL MÉNSULA')
print ('ACI 318 - 19 _ 16.5 - Ménsulas y cartelas')

P1 = 'Materiales'
P2 = '  fc. Resistencia del concreto.'
P3 = '  fy. Fluencia del acero.'
P4 = '  µ. Coeficiente de fricción.'
P5 = '  øv. Factor de reducción a cortante.'
P6 = '  øf. Factor de reducción a flexión.'
P7 = '  Número de la barra refuerzo principal.'
P8 = '  Número de la barra refuerzo auxiliar.'
P9 = '  Número de la barra estribos cerrados.'
P10 = ''
P11 = 'Geometría'
P12 = '  av. Dist. aplicación de carga.'
P13 = '  b. Ancho del soporte.'
P14 = '  c. Ancho de la ménsula.'
P15 = '  h. Altura de la ménsula.'
P16 = '  r. Recubrimiento del refuerzo.'
P17 = '  bw. Largo de la ménsula.'
P18 = ''
P19 = 'Cargas de diseño'
P20 = '  Vu. Fuerza cortante.'
P21 = '  Nuc. Fuerza horizontal.'
P22 = '  Nuc cal = 0.2 * Vu.'
P23 = '  Nuc = máx(Nuc, Nuc cal).'
P24 = '  Mu. Momento flector.'
P25 = ''
P26 = 'Chequeos'
P27 = '  Relación a/d < 1.0'
P28 = '  hm. hmín = 0.5 * d'
P29 = '  Nuc ≤ Vu'
P30 = ''
P31 = 'Verificación Vu'
P32 = '  Vc1 = 0.2 * ø * fc * bw * d'
P33 = '  Vc2 = (3.3 + 0.08 * fc) * ø * bw * d'
P34 = '  Vc3 = 11 * ø * bw * d'
P35 = '  Vc = mín. (Vc1, Vc2, Vc3)'
P36 = '  Vu ≤ Vc'
P37 = ''
P38 = 'Refuerzo principal'
P39 = '  Avf = Vu / (ø * fy * μ)'
P40 = '  An = Nuc / (ø * fy)'
P41 = '  Af = Mu / (ø * fy * (d - a / 2))'
P42 = '  As1 = Af + An'
P43 = '  As2 = 2/3 * Avf + An'
P44 = '  As3 = 0.04 * (fc / fy ) * bw * d'
P45 = '  As = máx (As1, As2, As3)'
P46 = ''
P47 = 'Refuerzo en estribos'
P48 = '  Ah = 0.5 * (As-An)'
P49 = ''
P50 = 'Refuerzo auxiliar'
P51 = '  Aa : 0.002 * bw * c'
P52 = ''
P53 = 'Verificación refuerzo mínimo'
P54 = '  Asc. Acero colocado'
P55 = '  pcal = Asc / (bw * d)'
P56 = '  pmín = 0.04 * fc / fy'
P57 = '  pcal ≥ pmín'
P58 = ''
P59 = 'Distribución del refuerzo'
P60 = '  Refuerzo principal.'
P61 = '  Refuerzo auxiliar.'
P62 = '  Estribos cerrados.'
P63 = ''
P64 = 'Detalle soldadura'
P65 = '  db. Diámetro refuerzo principal.'
P66 = '  lw. Long de la soldadura.'
P67 = '  tw. Long de la soldadura.'

V1 = ' '
V2 = round(material.fc, 2)
V3 = round(material.fy, 2)
V4 = round(material.u, 2)
V5 = round(material.phiv, 2)
V6 = round(material.phif, 2)
V7 = ref.Nb
V8 = ref.Nb
V9 = ref.Nbe
V10 = ' '
V11 = ' '
V12 = round(geom.av, 2)
V13 = round(geom.b, 2)
V14 = round(geom.c, 2)
V15 = round(geom.h, 2)
V16 = round(geom.r, 2)
V17 = round(geom.bw, 2)
V18 = ' '
V19 = ' '
V20 = round(carga.Vu, 2)
V21 = round(carga.Nuc1, 2)
V22 = round(carga.Nuc2, 2)
V23 = round(carga.Nuc, 2)
V24 = round(carga.Mu, 2)
V25 = ' '
V26 = ' '
V27 = chequeo.relacion_ad
V28 = round(geom.hmin, 2)
V29 = chequeo.Nuc_menor_Vu
V30 = ' '
V31 = ' '
V32 = round(calculo.Vc1, 2)
V33 = round(calculo.Vc2, 2)
V34 = round(calculo.Vc3, 2)
V35 = round(calculo.Vc, 2)
V36 = chequeo.Vu_menor_Vc
V37 = ' '
V38 = ' '
V39 = round(calculo.Avf, 2)
V40 = round(calculo.An, 2)
V41 = round(calculo.Af, 2)
V42 = round(calculo.As1, 2)
V43 = round(calculo.As2, 2)
V44 = round(calculo.As3, 2)
V45 = round(calculo.As, 2)
V46 = ' '
V47 = ' '
V48 = round(calculo.Ah, 2)
V49 = ' '
V50 = ' '
V51 = round(calculo.Aa, 2)
V52 = ' '
V53 = ' '
V54 = round(calculo.Ascol, 2)
V55 = round(calculo.pcal, 4)
V56 = round(calculo.pmin, 4)
V57 = chequeo.pcal_mayor_pmin
V58 = ' '
V59 = ' '
V60 = ref.Refp
V61 = ref.Refa
V62 = ref.Refe
V63 = ' '
V64 = ' '
V65 = ref.db
V66 = round(calculo.lw, 2)
V67 = round(calculo.tw, 2)

U1 = ' '
U2 = '[MPa]'
U3 = '[MPa]'
U4 = '-'
U5 = '-'
U6 = '-'
U7 = '-'
U8 = '-'
U9 = '-'
U10 = ' '
U11 = ' '
U12 = '[cm]'
U13 = '[cm]'
U14 = '[cm]'
U15 = '[cm]'
U16 = '[cm]'
U17 = '[cm]'
U18 = ' '
U19 = ' '
U20 = '[kN]'
U21 = '[kN]'
U22 = '[kN]'
U23 = '[kN]'
U24 = '[kN.cm]'
U25 = ' '
U26 = ' '
U27 = '-'
U28 = '[cm]'
U29 = '-'
U30 = ' '
U31 = ' '
U32 = '[kN]'
U33 = '[kN]'
U34 = '[kN]'
U35 = '[kN]'
U36 = '_'
U37 = ' '
U38 = ' '
U39 = '[cm²]'
U40 = '[cm²]'
U41 = '[cm²]'
U42 = '[cm²]'
U43 = '[cm²]'
U44 = '[cm²]'
U45 = '[cm²]'
U46 = ' '
U47 = ' '
U48 = '[cm²]'
U49 = ' '
U50 = ' '
U51 = '[cm²]'
U52 = ' '
U53 = ' '
U54 = '[cm²]'
U55 = '-'
U56 = '-'
U57 = '-'
U58 = ' '
U59 = ' '
U60 = ' '
U61 = ' '
U62 = ' '
U63 = ' '
U64 = ' '
U65 = '[cm]'
U66 = '[cm]'
U67 = '[cm]'

parametro = np.array([P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24,P25,P26,P27,P28,P29,P30,P31,P32,P33,P34,P35,P36,P37,P38,P39,P40,P41,P42,P43,P44,P45,P46,P47,P48,P49,P50,P51,P52,P53,P54,P55,P56,P57,P58,P59,P60,P61,P62,P63,P64,P65,P66,P67])
valor= np.array([V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,V29,V30,V31,V32,V33,V34,V35,V36,V37,V38,V39,V40,V41,V42,V43,V44,V45,V46,V47,V48,V49,V50,V51,V52,V53,V54,V55,V56,V57,V58,V59,V60,V61,V62,V63,V64,V65,V66,V67])
unidad = np.array([U1,U2,U3,U4,U5,U6,U7,U8,U9,U10,U11,U12,U13,U14,U15,U16,U17,U18,U19,U20,U21,U22,U23,U24,U25,U26,U27,U28,U29,U30,U31,U32,U33,U34,U35,U36,U37,U38,U39,U40,U41,U42,U43,U44,U45,U46,U47,U48,U49,U50,U51,U52,U53,U54,U55,U56,U57,U58,U59,U60,U61,U62,U63,U64,U65,U66,U67])

print('\n----------------------------------------------------------------')
datos = {'Parámetro': parametro, 'Valor': valor, 'Unidad': unidad}
df = pd.DataFrame(datos)
#print(df.head())
print (df.loc[1:])
print('----------------------------------------------------------------')

with pd.ExcelWriter('D:\APP_REPORTES\Reporte_DisMensulaV2.xlsx') as writer:
    df.to_excel(writer, sheet_name='Mensula', index=False, float_format="%.2f")

print ('\n!!! Datos guardados con exitos ¡¡¡')







import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# the universe of variables and membership function
jarak = ctrl.Antecedent(np.arange(0, 5250, 1), 'jarak')
kirim = ctrl.Antecedent(np.arange(0, 8, 1), 'kirim')
durasi = ctrl.Consequent(np.arange(0, 11, 1), 'durasi')

# Fungsi keanggotaan untuk masing-masing variabel
# (jarak, kirim dan durasi)
# Rules
jarak['sangat_dekat'] = fuzz.trimf(jarak.universe, [0, 400, 800.5])
jarak['dekat'] = fuzz.trimf(jarak.universe, [801, 1100, 1500.5])
jarak['sedang'] = fuzz.trimf(jarak.universe, [1501, 2000, 2500.5])
jarak['jauh'] = fuzz.trimf(jarak.universe, [2501, 3000, 3500.5])
jarak['sangat_jauh'] = fuzz.trimf(jarak.universe, [3501, 4375, 5250.5])

kirim['weekday'] = fuzz.trimf(kirim.universe, [0, 2, 5.5])
kirim['weekend'] = fuzz.trimf(kirim.universe, [5.5, 6, 7.5])

durasi['sangat_cepat'] = fuzz.trimf(durasi.universe, [1, 1, 2.5])
durasi['cepat'] = fuzz.trimf(durasi.universe, [2, 3, 4.5])
durasi['sedang'] = fuzz.trimf(durasi.universe, [4, 5, 6.5])
durasi['lambat'] = fuzz.trimf(durasi.universe, [6, 7, 8.5])
durasi['sangat_lambat'] = fuzz.trimf(durasi.universe, [8, 9, 10])

jarak.view()
kirim.view()
durasi.view()

# deklarasi rule
rule1 = ctrl.Rule(jarak['sangat_dekat'] &
                  kirim['weekday'], durasi['sangat_cepat'])
rule2 = ctrl.Rule(jarak['sangat_dekat'] & kirim['weekend'], durasi['cepat'])
rule3 = ctrl.Rule(jarak['dekat'] & kirim['weekday'], durasi['cepat'])
rule4 = ctrl.Rule(jarak['dekat'] & kirim['weekend'], durasi['sedang'])
rule5 = ctrl.Rule(jarak['sedang'] & kirim['weekday'], durasi['sedang'])
rule6 = ctrl.Rule(jarak['sedang'] & kirim['weekend'], durasi['lambat'])
rule7 = ctrl.Rule(jarak['jauh'] & kirim['weekday'], durasi['sedang'])
rule8 = ctrl.Rule(jarak['jauh'] & kirim['weekend'], durasi['lambat'])
rule9 = ctrl.Rule(jarak['sangat_jauh'] & kirim['weekday'], durasi['lambat'])
rule10 = ctrl.Rule(jarak['sangat_jauh'] &
                   kirim['weekend'], durasi['sangat_lambat'])

durasi_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])

braking = ctrl.ControlSystemSimulation(durasi_ctrl)

JarakKirim = int(input("Jauh Jarak : "))
HariKirim = int(input("Input Hari Kirim : "))

braking.input['jarak'] = JarakKirim
braking.input['kirim'] = HariKirim
braking.compute()
DurasiKirim = int(braking.output['durasi'])
print(braking.output['durasi'])


def carihari(mencari):
    if(mencari <= 5):
        harikirim = 'Weekday'
    elif(mencari > 5):
        harikirim = 'Weekend'
    return harikirim


def durasistring(pencari):
    if(pencari <= 2):
        Kirim = 'Sangat Cepat'
    elif(pencari > 2 and pencari <= 4):
        Kirim = 'Cepat'
    elif(pencari > 4 and pencari <= 6):
        Kirim = 'Sedang'
    elif(pencari > 6 and pencari <= 8):
        Kirim = 'Lambat'
    else:
        Kirim = 'Sangat Lambat'
    return Kirim


def output():
    print('Hasil Fuzzy')
    print('Hari Kirim = ', carihari(HariKirim))
    print('Jarak = ', JarakKirim, 'KM')
    print('Durasi Kirim =', DurasiKirim,
          'Hari (', durasistring(DurasiKirim), ')')


output()
durasi.view(sim=braking)
plt.show()

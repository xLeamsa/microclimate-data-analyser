import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import concurrent.futures

# 2. Zmienne i przynależności
temperature = ctrl.Antecedent(np.arange(0, 41, 0.1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 0.1), 'humidity')
co2 = ctrl.Antecedent(np.arange(400, 5001, 1), 'co2')

temperature['Very low'] = fuzz.gaussmf(temperature.universe, 0, 6.0)
temperature['Low'] = fuzz.gaussmf(temperature.universe, 18, 1.6)
temperature['Optimal'] = fuzz.gaussmf(temperature.universe, 22, 2.5)
temperature['High'] = fuzz.gaussmf(temperature.universe, 28, 1.6)
temperature['Very high'] = fuzz.gaussmf(temperature.universe, 40, 4.0)

humidity['Very low'] = fuzz.gaussmf(humidity.universe, 0, 12)
humidity['Low'] = fuzz.gaussmf(humidity.universe, 25, 10)
humidity['Optimal'] = fuzz.gaussmf(humidity.universe, 50, 10)
humidity['High'] = fuzz.gaussmf(humidity.universe, 75, 10)
humidity['Very high'] = fuzz.gaussmf(humidity.universe, 100, 12)

co2['Ideal'] = fuzz.gaussmf(co2.universe, 400, 300)
co2['Optimal'] = fuzz.gaussmf(co2.universe, 1000, 200)
co2['High'] = fuzz.gaussmf(co2.universe, 1800, 250)
co2['Too high'] = fuzz.gaussmf(co2.universe, 5000, 600)

comfort = ctrl.Consequent(np.arange(0, 101, 1), 'comfort', defuzzify_method='centroid')

comfort['Very low'] = fuzz.trapmf(comfort.universe, [-50, -50, 0, 25])
comfort['Low']      = fuzz.gaussmf(comfort.universe, 25, 12)
comfort['Medium']   = fuzz.gaussmf(comfort.universe, 50, 12)
comfort['High']     = fuzz.gaussmf(comfort.universe, 75, 12)
comfort['Very high'] = fuzz.trapmf(comfort.universe, [80, 95, 150, 150])

# 3. Reguły
rule1 = ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['Ideal'], comfort['Very low'])
rule2 = ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['Optimal'], comfort['Very low'])
rule3 = ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['High'], comfort['Very low'])
rule4 = ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['Too high'], comfort['Very low'])
rule5 = ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['Ideal'], comfort['Very low'])
rule6 = ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['Optimal'], comfort['Very low'])
rule7 = ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['High'], comfort['Very low'])
rule8 = ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['Too high'], comfort['Very low'])
rule9 = ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['Ideal'], comfort['Very low'])
rule10 = ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['Optimal'], comfort['Very low'])
rule11 = ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['High'], comfort['Very low'])
rule12 = ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['Too high'], comfort['Very low'])
rule13 = ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['Ideal'], comfort['Very low'])
rule14 = ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['Optimal'], comfort['Very low'])
rule15 = ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['High'], comfort['Very low'])
rule16 = ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['Too high'], comfort['Very low'])
rule17 = ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['Ideal'], comfort['Very low'])
rule18 = ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['Optimal'], comfort['Very low'])
rule19 = ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['High'], comfort['Very low'])
rule20 = ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['Too high'], comfort['Very low'])

rule21 = ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['Ideal'], comfort['Very low'])
rule22 = ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['Optimal'], comfort['Very low'])
rule23 = ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['High'], comfort['Very low'])
rule24 = ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['Too high'], comfort['Very low'])
rule25 = ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['Ideal'], comfort['Medium'])
rule26 = ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['Optimal'], comfort['Low'])
rule27 = ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['High'], comfort['Low'])
rule28 = ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['Too high'], comfort['Very low'])
rule29 = ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['Ideal'], comfort['High'])
rule30 = ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['Optimal'], comfort['High'])
rule31 = ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['High'], comfort['Medium'])
rule32 = ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['Too high'], comfort['Very low'])
rule33 = ctrl.Rule(temperature['Low'] & humidity['High'] & co2['Ideal'], comfort['Medium'])
rule34 = ctrl.Rule(temperature['Low'] & humidity['High'] & co2['Optimal'], comfort['Low'])
rule35 = ctrl.Rule(temperature['Low'] & humidity['High'] & co2['High'], comfort['Low'])
rule36 = ctrl.Rule(temperature['Low'] & humidity['High'] & co2['Too high'], comfort['Very low'])
rule37 = ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['Ideal'], comfort['Very low'])
rule38 = ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['Optimal'], comfort['Very low'])
rule39 = ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['High'], comfort['Very low'])
rule40 = ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['Too high'], comfort['Very low'])

rule41 = ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['Ideal'], comfort['Very low'])
rule42 = ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['Optimal'], comfort['Very low'])
rule43 = ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['High'], comfort['Very low'])
rule44 = ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['Too high'], comfort['Very low'])
rule45 = ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['Ideal'], comfort['High'])
rule46 = ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['Optimal'], comfort['High'])
rule47 = ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['High'], comfort['Medium'])
rule48 = ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['Too high'], comfort['Very low'])
rule49 = ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['Ideal'], comfort['Very high'])
rule50 = ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['Optimal'], comfort['High'])
rule51 = ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['High'], comfort['Medium'])
rule52 = ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['Too high'], comfort['Very low'])
rule53 = ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['Ideal'], comfort['High'])
rule54 = ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['Optimal'], comfort['High'])
rule55 = ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['High'], comfort['Medium'])
rule56 = ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['Too high'], comfort['Very low'])
rule57 = ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['Ideal'], comfort['Very low'])
rule58 = ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['Optimal'], comfort['Very low'])
rule59 = ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['High'], comfort['Very low'])
rule60 = ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['Too high'], comfort['Very low'])

rule61 = ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['Ideal'], comfort['Very low'])
rule62 = ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['Optimal'], comfort['Very low'])
rule63 = ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['High'], comfort['Very low'])
rule64 = ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['Too high'], comfort['Very low'])
rule65 = ctrl.Rule(temperature['High'] & humidity['Low'] & co2['Ideal'], comfort['Medium'])
rule66 = ctrl.Rule(temperature['High'] & humidity['Low'] & co2['Optimal'], comfort['Low']) #takie pozmieniane z medium
rule67 = ctrl.Rule(temperature['High'] & humidity['Low'] & co2['High'], comfort['Low'])
rule68 = ctrl.Rule(temperature['High'] & humidity['Low'] & co2['Too high'], comfort['Very low'])
rule69 = ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['Ideal'], comfort['High'])
rule70 = ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['Optimal'], comfort['High'])
rule71 = ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['High'], comfort['Medium'])
rule72 = ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['Too high'], comfort['Very low'])
rule73 = ctrl.Rule(temperature['High'] & humidity['High'] & co2['Ideal'], comfort['Medium'])
rule74 = ctrl.Rule(temperature['High'] & humidity['High'] & co2['Optimal'], comfort['Low'])
rule75 = ctrl.Rule(temperature['High'] & humidity['High'] & co2['High'], comfort['Low'])
rule76 = ctrl.Rule(temperature['High'] & humidity['High'] & co2['Too high'], comfort['Very low'])
rule77 = ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['Ideal'], comfort['Very low'])
rule78 = ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['Optimal'], comfort['Very low'])
rule79 = ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['High'], comfort['Very low'])
rule80 = ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['Too high'], comfort['Very low'])

rule81 = ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['Ideal'], comfort['Very low'])
rule82 = ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['Optimal'], comfort['Very low'])
rule83 = ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['High'], comfort['Very low'])
rule84 = ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['Too high'], comfort['Very low'])
rule85 = ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['Ideal'], comfort['Very low'])
rule86 = ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['Optimal'], comfort['Very low'])
rule87 = ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['High'], comfort['Very low'])
rule88 = ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['Too high'], comfort['Very low'])
rule89 = ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['Ideal'], comfort['Very low'])
rule90 = ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['Optimal'], comfort['Very low'])
rule91 = ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['High'], comfort['Very low'])
rule92 = ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['Too high'], comfort['Very low'])
rule93 = ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['Ideal'], comfort['Very low'])
rule94 = ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['Optimal'], comfort['Very low'])
rule95 = ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['High'], comfort['Very low'])
rule96 = ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['Too high'], comfort['Very low'])
rule97 = ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['Ideal'], comfort['Very low'])
rule98 = ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['Optimal'], comfort['Very low'])
rule99 = ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['High'], comfort['Very low'])
rule100 = ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['Too high'], comfort['Very low'])

rule_fix_low = ctrl.Rule(humidity['Very low'], comfort['Very low'])
rule_fix_high = ctrl.Rule(humidity['Very high'], comfort['Very low'])

rules = [
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
    rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,
    rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40,
    rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50,
    rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60,
    rule61, rule62, rule63, rule64, rule65, rule66, rule67, rule68, rule69, rule70,
    rule71, rule72, rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80,
    rule81, rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89, rule90,
    rule91, rule92, rule93, rule94, rule95, rule96, rule97, rule98, rule99, rule100,rule_fix_low,rule_fix_high]

comfort_ctrl = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(comfort_ctrl)


def calculate_comfort(temp_val, hum_val, co2_val):
    sim.input['temperature'] = float(temp_val)
    sim.input['humidity'] = float(hum_val)
    sim.input['co2'] = float(co2_val)
    
    try:
        sim.compute()
        return round(sim.output['comfort'], 2)
    except Exception as e:
        print(f"Błąd logiki rozmytej: {e}")
        return 0.0
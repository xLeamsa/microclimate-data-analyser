import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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
comfort['Low'] = fuzz.gaussmf(comfort.universe, 25, 12)
comfort['Medium'] = fuzz.gaussmf(comfort.universe, 50, 12)
comfort['High'] = fuzz.gaussmf(comfort.universe, 75, 12)
comfort['Very high'] = fuzz.trapmf(comfort.universe, [80, 95, 150, 150])

rules = [
    ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Optimal'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['High'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very low'] & humidity['Very high'] & co2['Too high'], comfort['Very low']),

    ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['Ideal'], comfort['Medium']),
    ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['Optimal'], comfort['Low']),
    ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['High'], comfort['Low']),
    ctrl.Rule(temperature['Low'] & humidity['Low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['Ideal'], comfort['High']),
    ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['Optimal'], comfort['High']),
    ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['High'], comfort['Medium']),
    ctrl.Rule(temperature['Low'] & humidity['Optimal'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['High'] & co2['Ideal'], comfort['Medium']),
    ctrl.Rule(temperature['Low'] & humidity['High'] & co2['Optimal'], comfort['Low']),
    ctrl.Rule(temperature['Low'] & humidity['High'] & co2['High'], comfort['Low']),
    ctrl.Rule(temperature['Low'] & humidity['High'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Low'] & humidity['Very high'] & co2['Too high'], comfort['Very low']),

    ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['Ideal'], comfort['High']),
    ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['Optimal'], comfort['High']),
    ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['High'], comfort['Medium']),
    ctrl.Rule(temperature['Optimal'] & humidity['Low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['Ideal'], comfort['Very high']),
    ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['Optimal'], comfort['High']),
    ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['High'], comfort['Medium']),
    ctrl.Rule(temperature['Optimal'] & humidity['Optimal'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['Ideal'], comfort['High']),
    ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['Optimal'], comfort['High']),
    ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['High'], comfort['Medium']),
    ctrl.Rule(temperature['Optimal'] & humidity['High'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Optimal'] & humidity['Very high'] & co2['Too high'], comfort['Very low']),

    ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Low'] & co2['Ideal'], comfort['Medium']),
    ctrl.Rule(temperature['High'] & humidity['Low'] & co2['Optimal'], comfort['Low']),
    ctrl.Rule(temperature['High'] & humidity['Low'] & co2['High'], comfort['Low']),
    ctrl.Rule(temperature['High'] & humidity['Low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['Ideal'], comfort['High']),
    ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['Optimal'], comfort['High']),
    ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['High'], comfort['Medium']),
    ctrl.Rule(temperature['High'] & humidity['Optimal'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['High'] & co2['Ideal'], comfort['Medium']),
    ctrl.Rule(temperature['High'] & humidity['High'] & co2['Optimal'], comfort['Low']),
    ctrl.Rule(temperature['High'] & humidity['High'] & co2['High'], comfort['Low']),
    ctrl.Rule(temperature['High'] & humidity['High'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['High'] & humidity['Very high'] & co2['Too high'], comfort['Very low']),

    ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Low'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Optimal'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['High'] & co2['Too high'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['Ideal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['Optimal'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['High'], comfort['Very low']),
    ctrl.Rule(temperature['Very high'] & humidity['Very high'] & co2['Too high'], comfort['Very low']),

    ctrl.Rule(humidity['Very low'], comfort['Very low']),
    ctrl.Rule(humidity['Very high'], comfort['Very low']),
]

comfort_ctrl = ctrl.ControlSystem(rules)
simulation = ctrl.ControlSystemSimulation(comfort_ctrl)


def calculate_comfort(temp_val, hum_val, co2_val):
    simulation.input['temperature'] = float(temp_val)
    simulation.input['humidity'] = float(hum_val)
    simulation.input['co2'] = float(co2_val)

    try:
        simulation.compute()
        return round(simulation.output['comfort'], 2)
    except Exception as error:
        print(f"Fuzzy logic error: {error}")
        return 0.0

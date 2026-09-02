export function getComfortAdvice(temperature, humidity, co2) {
    const issues = [];

    if (temperature < 18) {
        issues.push('Temperature is low - try increasing heating.');
    } else if (temperature > 28) {
        issues.push('Temperature is high - ventilate the room or use AC.');
    }

    if (humidity < 25) {
        issues.push('Humidity is low - consider using a humidifier.');
    } else if (humidity > 75) {
        issues.push('Humidity is high - ventilate the room or use a dehumidifier.');
    }

    if (co2 > 1500) {
        issues.push('CO2 level is high - open a window to air out the room.');
    } else if (co2 > 1000) {
        issues.push('CO2 level is elevated - airing out soon is a good idea.');
    }

    return issues;
}
import astropy.units as u
import astropy.constants as c


# Constants
G = c.G  # Gravitational constant
K = 8.9875e9 * u.N * u.meter ** 2 / u.C ** 2 # Coulomb's constant

planet_mass = {
    'sun': c.M_sun,
    'mercury': c.M_mercury,
    'venus': c.M_venus,
    'earth': c.M_earth,
    'mars': c.M_mars
}

planet_speeds = {
    'earth': 29722.2222222,
    'mars': 24100
}

planet_distance = {
    'earth': 1.495978707e11,
    'mars': 2.28e11
}
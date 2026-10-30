import bisect
import math



GRAVITY=9.80665

G1 = [
    (0.00, 0.2629), (0.05, 0.2558), (0.10, 0.2487), (0.15, 0.2413), (0.20, 0.2344),
    (0.25, 0.2278), (0.30, 0.2214), (0.35, 0.2155), (0.40, 0.2104), (0.45, 0.2061),
    (0.50, 0.2032), (0.55, 0.2020), (0.60, 0.2034), (0.70, 0.2165), (0.725, 0.2230),
    (0.75, 0.2313), (0.775, 0.2417), (0.80, 0.2546), (0.825, 0.2706), (0.85, 0.2901),
    (0.875, 0.3136), (0.90, 0.3415), (0.925, 0.3734), (0.95, 0.4084), (0.975, 0.4448),
    (1.00, 0.4805), (1.025, 0.5136), (1.05, 0.5427), (1.075, 0.5677), (1.10, 0.5883),
    (1.125, 0.6053), (1.15, 0.6191), (1.20, 0.6393), (1.25, 0.6518), (1.30, 0.6589),
    (1.35, 0.6621), (1.40, 0.6625), (1.45, 0.6607), (1.50, 0.6573), (1.55, 0.6528),
    (1.60, 0.6474), (1.65, 0.6413), (1.70, 0.6347), (1.75, 0.6280), (1.80, 0.6210),
    (1.85, 0.6141), (1.90, 0.6072), (1.95, 0.6003), (2.00, 0.5934), (2.05, 0.5867),
    (2.10, 0.5804), (2.15, 0.5743), (2.20, 0.5685), (2.25, 0.5630), (2.30, 0.5577),
    (2.35, 0.5527), (2.40, 0.5481), (2.45, 0.5438), (2.50, 0.5397), (2.60, 0.5325),
    (2.70, 0.5264), (2.80, 0.5211), (2.90, 0.5168), (3.00, 0.5133), (3.10, 0.5105),
    (3.20, 0.5084), (3.30, 0.5067), (3.40, 0.5054), (3.50, 0.5040), (3.60, 0.5030),
    (3.70, 0.5022), (3.80, 0.5016), (3.90, 0.5010), (4.00, 0.5006), (4.20, 0.4998),
    (4.40, 0.4995), (4.60, 0.4992), (4.80, 0.4990), (5.00, 0.4988),
]
G1_MACH = [m for m, _ in G1]
G1_CD = [c for _, c in G1]


def speed_of_sound(temp_c: float = 15.0) -> float:
    """Speed of sound in dry air, in m/s."""
    gamma = 1.4        # ratio of specific heats for air
    R = 287.05         # specific gas constant for air, J/(kg·K)
    return math.sqrt(gamma * R * (temp_c + 273.15))


def drag_coefficient(speed: float, temp_c: float = 15.0, form_factor: float = 1.0) -> float:
    """
    Drag coefficient Cd for a projectile moving at `speed` (m/s) through air.

    temp_c:      air temperature in °C (sets the speed of sound)
    form_factor: 1.0 uses the G1 reference shape. For a specific bullet, pass its
                 form factor (its Cd divided by the G1 Cd at the same Mach number).
    Cd is linearly interpolated from the G1 table, which covers Mach 0 to 5.
    """
    if speed < 0:
        raise ValueError("speed must be >= 0 m/s")
    mach = speed / speed_of_sound(temp_c)
    if not G1_MACH[0] <= mach <= G1_MACH[-1]:
        raise ValueError(f"Mach {mach:.2f} is outside the table range (0 to 5)")
    i = bisect.bisect_right(G1_MACH, mach)
    if i == len(G1_MACH):                  # exactly Mach 5
        return form_factor * G1_CD[-1]
    m0, m1 = G1_MACH[i - 1], G1_MACH[i]
    c0, c1 = G1_CD[i - 1], G1_CD[i]
    t = (mach - m0) / (m1 - m0)
    return form_factor * (c0 + t * (c1 - c0))



def air_density(pressure_pa: float = 101325.0, temp_c: float = 15.0) -> float:
    """Air density p (p) in kg/m³, from pressure (Pa) and temperature (°C)."""
    R_AIR = 287.05  # specific gas constant for air, J/(kg·K)
    return pressure_pa / (R_AIR * (temp_c + 273.15))



def frontal_area(diameter: float=0.01295 ) -> float:
    """Frontal area a (A) of a round object in m², from its diameter in m."""
    return math.pi * diameter ** 2 / 4


def dragForce(p: float, v: float, cd: float, a: float) -> float:
    """Drag force F = ½ · p · v² · cd · a, in newtons."""
    drag_force= 0.5 * p * v ** 2 * cd * a
    return drag_force


   
def drag_factor(v,p,cd,a,mass: float = (0.0428),time: float= (0.00000001)):
    b=1/2*p*cd*a/mass
    return b


def change_in_speed(time,v,b,a):
    while time!=12

def shot(target_distance)



target_distance=float(input("how far away is the target "))
height=float(input("how much heigher is the target from you"))

if __name__ == "__main__":
    v= 890
    p=air_density()
    a=frontal_area()
    cd=drag_coefficient(v)
    result=dragForce(p,v,cd,a)
    b=drag_factor(v,p,cd)
    print(f"the air resistance is {result}N")
    
    


'''Range, which still has to be measured accurately, because it decides how much the bullet drops.
Gravity, which pulls the bullet down the whole way.
Wind, still the hardest variable, since it can blow differently at different points along the bullet’s path.
Air density (temperature, altitude, pressure, humidity), which changes drag.
Uphill or downhill angle.
Spin drift and the Earth’s rotation on very long shots.'''



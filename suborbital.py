import matplotlib.pyplot as plt
from math import sqrt, pi
from numpy import sign

altitude = 0
velocity = 0
mass = 5000
a = 2 * 2 * pi
timedelta = 0.1


def AtmosDensity():
    a = altitude / 1000
    return 10 ** (
        7.001985e-2 +
        -4.335215e-3 * (a ** 1) +
        -5.009831e-3 * (a ** 2) +
        1.621827e-4 * (a ** 3) +
        -2.471283e-6 * (a ** 4) +
        1.904383e-8 * (a ** 5) +
        -7.189421e-11 * (a ** 6) +
        1.060067e-13 * (a ** 7)
    )


def Drag():
    density = AtmosDensity()
    re = density * abs(velocity) / 1.81e-5

    if re < 0.1:
        cd = 0.4
    else:
        cd = (21.12 / re) + (6.3 / sqrt(re)) + 0.25

    return 0.5 * density * (velocity ** 2) * cd * a * -sign(velocity)


def Gravity():
    return -9.81 * mass


def Simulate(startVelocity):
    global altitude
    global velocity

    altitude = 20000
    velocity = startVelocity
    time = 0
    s001 = 0
    s0001 = 0
    t001 = 0
    t0001 = 0
    started001 = False
    started0001 = False
    apogee = 0

    a = []

    while altitude > 0:
        drag = Drag()
        force = drag + Gravity()

        acceleration = force / mass
        velocity += acceleration * timedelta
        altitude += velocity * timedelta

        if altitude < 0:
            break

        if started001:
            if abs(drag) < 9.81 * mass * 0.01:
                t001 = time
        else:
            if abs(drag) < 9.81 * mass * 0.01:
                s001 = time
                started001 = True
        if started0001:
            if abs(drag) < 9.81 * mass * 0.001:
                t0001 = time
        else:
            if abs(drag) < 9.81 * mass * 0.001:
                s0001 = time
                started0001 = True

        time += timedelta

        if altitude > apogee:
            apogee = altitude

    return t001 - s001, t0001 - s0001, apogee

_alt = []
_t001 = []
_t0001 = []

for i in range(500, 1600, 20):
    _a, _b, _c = Simulate(i)
    _t001.append(_a)
    _t0001.append(_b)
    _alt.append(_c / 1000)

    # print(i, _c / 1000, _a, _b)

f = plt.figure()
f.set_figwidth(12)
f.set_figheight(9)

plt.plot(_alt, _t001, label="Time under 1% g")
plt.plot(_alt, _t0001, label="Time under 0.1% g")
plt.hlines(60, min(*_alt), max(*_alt))
plt.legend()

plt.xlabel("Apogee (km)")
plt.ylabel("Time (s)")

plt.tight_layout()

plt.savefig("suborbital.png")

from numpy import pi

# Start with middle C = C4
# Each note increments by a phase of pi/4
# https://pages.mtu.edu/~suits/notefreqs.html#:~:text=Frequencies%20of%20Musical%20Notes%2C%20A4%20%3D%20440%20Hz
c_scale = {
    round(0, 2): ("C4", 261.63 * 2),
    round(1 * pi / 4, 2): ("D4", 293.66 * 2),
    round(2 * pi / 4, 2): ("E4", 329.63 * 2),
    round(3 * pi / 4, 2): ("F4", 349.23 * 2),
    round(4 * pi / 4, 2): ("G4", 392.00 * 2),
    round(-3 * pi / 4, 2): ("A4", 440.00 * 2),  # after pi, phases are negative
    round(-2 * pi / 4, 2): ("B4", 493.88 * 2),
    round(-1 * pi / 4, 2): ("C5", 523.25 * 2),
}

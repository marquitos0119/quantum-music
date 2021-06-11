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

# How to compute any major scale in terms of half-steps
# All major scales follow: W W H W W W H
major_scale_steps = [2, 2, 1, 2, 2, 2, 1]


def get_scale(start_note, pi_division=4):
    """
    :param start_note: a tuple of form (note_name, frequency)
    :param pi_division: each pitch is a multiple of pi/pi_division
    """
    note, frequency = start_note
    print(f"note: {note}, frequency: {frequency}")

    # Initialize first note
    scale = {0: ("0", frequency)}

    # Index into major_scale_steps
    step_index = 0
    # Number of half-steps from the first note
    steps_from_start = 0

    # A list of numerators, first to pi, then pi to 2pi (phase is negative)
    phase_numerators = list(range(1, pi_division + 1)) + [
        num * -1 for num in list(range(pi_division - 1, 0, -1))
    ]
    for i in phase_numerators:
        steps_from_start += major_scale_steps[step_index]
        phase = round(i * pi / pi_division, 2)

        # Each half-step is 2^(1/12) away
        scale[phase] = (f"{steps_from_start}", frequency * (2 ** (steps_from_start / 12)))
        step_index = (step_index + 1) % len(major_scale_steps)

    return scale

from numpy import pi
import re

notes_by_name = [
    "C",
    "C#/Db",
    "D",
    "D#/Eb",
    "E",
    "F",
    "F#/Gb",
    "G",
    "G#/Ab",
    "A",
    "A#/Bb",
    "B",
]

# Middle C = C4
# Each note increments by a phase of pi/4
# https://pages.mtu.edu/~suits/notefreqs.html#:~:text=Frequencies%20of%20Musical%20Notes%2C%20A4%20%3D%20440%20Hz
c_scale = {
    round(0, 2): ("C5", 261.63 * 2),
    round(1 * pi / 4, 2): ("D5", 293.66 * 2),
    round(2 * pi / 4, 2): ("E5", 329.63 * 2),
    round(3 * pi / 4, 2): ("F5", 349.23 * 2),
    round(4 * pi / 4, 2): ("G5", 392.00 * 2),
    round(-3 * pi / 4, 2): ("A5", 440.00 * 2),  # after pi, phases are negative
    round(-2 * pi / 4, 2): ("B5", 493.88 * 2),
    round(-1 * pi / 4, 2): ("C6", 523.25 * 2),
}

g_scale = {
    round(0, 2): ("G5", 783.99),
    round(1 * pi / 4, 2): ("A5", 880.00),
    round(2 * pi / 4, 2): ("B5", 987.77),
    round(3 * pi / 4, 2): ("C6", 1046.50),
    round(4 * pi / 4, 2): ("D6", 1174.66),
    round(-3 * pi / 4, 2): ("E6", 1318.51),  # after pi, phases are negative
    round(-2 * pi / 4, 2): ("F#6", 1479.98),
    round(-1 * pi / 4, 2): ("G6", 1567.98),
}

# How to compute any major scale in terms of half-steps
# All major scales follow: W W H W W W H
major_scale_steps = [2, 2, 1, 2, 2, 2, 1]


def get_note_index(start_note):
    """Gets the starting index in notes_by_name"""
    note, frequency = start_note
    note_number = int(re.findall(r"\d+", note)[0])
    # print(f"note: {note}, frequency: {frequency}")
    # print(f"note number: {note_number}")

    note_name_index = 0
    note_name = "".join([i for i in note if not i.isdigit()])
    # print(f'Looking to match {note_name}')
    for i, n in enumerate(notes_by_name):
        # print(f'n={n}, note_name={note_name}')
        if note_name == n:
            note_name_index = i
            break
        else:
            if "/" in n:
                possible_notes = n.split("/")
                if note_name in possible_notes:
                    note_name_index = i
                    break

    if note_name != notes_by_name[note_name_index]:
        print(f"start_note {start_note[0]} is in incorrect format")
        return 0, 0

    return note_name_index, note_number


def get_scale(start_note, pi_division=4):
    """
    :param start_note: a tuple of form (note_name, frequency)
    :param pi_division: each pitch is a multiple of pi/pi_division
    """

    note_name_index, note_number = get_note_index(start_note)
    print(
        f"note={notes_by_name[note_name_index]}, "
        f"note_name_index={note_name_index}, "
        f"note_number={note_number}"
    )

    # Initialize first note
    frequency = start_note[1]
    scale = {0: (f"{start_note[0]}", start_note[1])}

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

        # Each half-step is 2^(1/12)
        note_name_index = (note_name_index + major_scale_steps[step_index]) % len(notes_by_name)
        if note_name_index <= 1:
            note_number += 1
        note_name = notes_by_name[note_name_index]
        scale[phase] = (
            f"{note_name}{note_number}",
            round(frequency * (2 ** (steps_from_start / 12)), 2),
        )

        step_index = (step_index + 1) % len(major_scale_steps)

    return scale

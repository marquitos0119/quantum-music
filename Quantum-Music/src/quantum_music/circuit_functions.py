#!/usr/bin/python3

import numpy as np
from numpy import pi

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization.utils import _get_layered_instructions

# Additional imports for audio
from time import sleep
from IPython.display import Audio, display
import matplotlib.pyplot as plt

# Simulators
state_vector_sim = Aer.get_backend("statevector_simulator")
unitary_sim = Aer.get_backend("unitary_simulator")


# Utility functions
def get_state_vector(circuit):
    return state_vector_sim.run(circuit).result().get_statevector()


def get_unitary_matrix(circuit):
    return execute(circuit, unitary_sim).result().get_unitary()


def get_amplitudes(matrix):
    return abs(matrix)


def get_probabilities(matrix):
    return abs(matrix ** 2)


def get_phases(matrix):
    return np.angle(matrix)


def get_example_circuit():
    """Example circuit to use in testing"""
    qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";

    qreg q[3];
    creg c[3];

    h q[0];
    h q[1];
    s q[0];
    s q[1];
    t q[0];
    s q[1];
    tdg q[0];
    cx q[1],q[2];
    t q[0];
    s q[1];
    h q[1];
    cx q[0],q[1];
    t q[0];
    h q[1];
    t q[0];
    """

    return QuantumCircuit.from_qasm_str(qasm)


# Pretty-printing
def print_matrix(matrix):
    print("Matrix shape ", matrix.shape)
    for row in matrix:
        for num in row:
            print(f"{np.around(num, 2)}   ", end="")
        print("")
    print("\n---")


def print_vector(vector, comment=""):
    print(f"Vector {comment} with shape {vector.shape}")
    for num in vector:
        print(np.around(num, 2))
    print("---")


def get_circuits_by_column(circuit):
    """circuit-splitter.ipynb"""
    # Get circuit metadata
    num_qubits = circuit.num_qubits
    num_clbits = circuit.num_clbits
    _, _, ops = _get_layered_instructions(circuit)
    num_columns = len(ops)

    # Initialize column information
    curr_column = [0] * num_qubits
    columns = []
    for i in range(num_columns):
        columns.append([])

    # Organize instructions by column
    for (insn, qargs, cargs) in circuit.data:
        col = -1
        anchor_qubit = -1
        for qubit in qargs:
            index = qubit.index
            if curr_column[index] > col:
                col = curr_column[index]
                anchor_qubit = index
        if col == -1 or anchor_qubit == -1:
            print("Something went wrong...")
            continue

        columns[col].append((insn, qargs, cargs))
        curr_column[anchor_qubit] += 1
        for qubit in qargs:
            index = qubit.index
            curr_column[index] = curr_column[anchor_qubit]

    # Build the subcircuits by column
    sub_circuits = []
    for col in range(0, num_columns):
        sub_circuit = QuantumCircuit(num_qubits, num_clbits)
        for (insn, qargs, cargs) in columns[col]:
            sub_circuit.append(insn, qargs, cargs)
        sub_circuits.append(sub_circuit)

    assert len(sub_circuits) == num_columns
    return sub_circuits


"""Audio variables and functions"""


def plot_sound(x, y, frequency, xlim=None):
    """
    Plot the frequency (sound) as a visual graph.
    Optionally pass in the x-axis limits (xlim) as an array of two numbers
    """
    # Zooms in so we can actually see the waves
    if xlim and len(xlim) == 2:
        plt.xlim(xlim[0], xlim[1])
    plt.title(f"Frequency {frequency} Hz")
    plt.plot(x, y)


class InvisibleAudio(Audio):
    def _repr_html_(self):
        audio = super()._repr_html_()
        audio = audio.replace("<audio", '<audio onended="this.parentNode.removeChild(this)"')
        return f'<div style="display:none">{audio}</div>'


def play_notes(columns, merge=True, plot=False, volume=1.0):
    """
    :param notes: a list of tuples of form (note, frequency)
    :param merge: if True, play notes simultaneously, else sequentially
    :param plot: if True, display a graph of the frequencies
    """
    rate = 16000.0
    duration = 1
    x = np.linspace(0.0, duration, int(rate * duration))
    fullx = np.linspace(0.0, duration * len(columns), int(rate * duration))

    if merge:
        y = None
        for i,column in enumerate(columns):
            offset = float(i) * duration
            for (note, frequency) in column:
                yi = np.sin((frequency * 2.0 * np.pi * x) - offset)
                yi *= volume
                if y is None:
                    y = yi
                else:
                    y += yi

        if plot:
            plot_sound(fullx, y, "chord")

        # Play sound and display widget
        display(InvisibleAudio(y, rate=rate, autoplay=True))

    else:
        for (note, frequency) in notes:
            y = volume * np.sin(frequency * 2.0 * np.pi * x)
            if plot:
                plot_sound(x, y, frequency, xlim=[0.13, 0.15])

            # Play sound and display widget
            display(Audio(y, rate=rate, autoplay=True))
            sleep(0.25)  # Add delay between notes


def play_notes_from_state_vector(state_vector, show_vectors=False, use_volume=True):
    notes = get_notes(state_vector)
    volumes = get_probabilities(state_vector)
    if show_vectors:
        print_vector(state_vector, comment="state vector")
        print_vector(get_phases(state_vector), comment="phases")
        print_vector(volumes, comment="amplitudes")

    if len(notes) != len(volumes):
        print("Number of phases and amplitudes do not match")
        return

    rate = 16000.0
    duration = 1.25
    x = np.linspace(0.0, duration, int(rate * duration))
    y = None

    for i, (note, frequency) in enumerate(notes):
        yi = np.sin(frequency * 2.0 * np.pi * x)
        if use_volume:
            yi *= volumes[i]

        if y is None:
            y = yi
        else:
            y += yi

    display(InvisibleAudio(y, rate=rate, autoplay=True))


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


def get_note(phase):
    """Return music note given a phase"""
    # Round to the nearest multiple of pi/4
    base = pi / 4
    key = round(base * round(phase / base), 2)
    if key not in c_scale:
        print(f"{key} not in scale!")
        return None

    note = c_scale[key]
    return note


def get_notes(state_vector):
    notes = []
    phases = get_phases(state_vector)
    for phase in phases:
        notes.append(get_note(phase))

    return notes


def get_cummulative_state_vectors(sub_circuits):
    """Get the state vectors at each column as if executed in order"""
    if len(sub_circuits) == 0:
        return []

    state_vectors = [get_state_vector(sub_circuits[0])]
    for i in range(1, len(sub_circuits)):
        sub_circuit = sub_circuits[i]
        unitary_matrix = get_unitary_matrix(sub_circuit)

        # Multiply this column's unitary matrix with previous state_vector
        state_vectors.append(np.matmul(unitary_matrix, state_vectors[i - 1]))

    return state_vectors

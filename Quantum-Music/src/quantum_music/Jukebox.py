from time import sleep

from IPython.display import display, clear_output
from ipywidgets import widgets
import numpy as np
from qiskit import QuantumCircuit

from quantum_music.circuit_functions import (
    get_state_vector,
    get_unitary_matrix,
    get_circuits_by_column,
    play_notes,
    get_notes,
)


class Jukebox:
    def __init__(self, circuit: QuantumCircuit):
        self.index = 0
        self.circuit = circuit
        self.sub_circuits = None
        self.state_vectors = None
        self.buttons = self.get_buttons()

        self.load_circuit(circuit)

        # Display UI controls
        self.display()

    def refresh_output(self):
        """Removes previous output and refreshes the button controls"""
        clear_output(wait=True)
        self.display()

    def get_cummulative_state_vectors(self, sub_circuits):
        if len(sub_circuits) == 0:
            return []

        state_vectors = [get_state_vector(sub_circuits[0])]
        for i in range(1, len(sub_circuits)):
            sub_circuit = sub_circuits[i]
            unitary_matrix = get_unitary_matrix(sub_circuit)

            # Multiply this column's unitary matrix with previous state_vector
            state_vectors.append(np.matmul(unitary_matrix, state_vectors[i - 1]))

        return state_vectors

    def load_circuit(self, circuit: QuantumCircuit):
        """Overwrite the current circuit with the new circuit"""
        self.sub_circuits = get_circuits_by_column(circuit)
        self.state_vectors = self.get_cummulative_state_vectors(self.sub_circuits)

    def play(self, button):
        self.refresh_output()
        notes = get_notes(self.state_vectors[self.index])
        play_notes(notes)

    def play_all_from(self, button):
        for i in range(self.index, len(self.state_vectors)):
            self.refresh_output()
            self.index = i
            self.play(button)
            sleep(1)

    def restart(self, button):
        """Moves back to the first column"""
        if self.index == 0:
            return
        self.refresh_output()
        self.index = 0
        print(f"Column={self.index}")

    def back(self, button):
        if self.index == 0:
            return
        self.refresh_output()
        self.index -= 1
        self.play(button)
        print(f"Column={self.index}")

    def forward(self, button):
        if self.index == len(self.sub_circuits) - 1:
            return
        self.refresh_output()
        self.index += 1
        self.play(button)
        print(f"Column={self.index}")

    def get_buttons(self):
        restart_button = widgets.Button(icon="fast-backward", tooltip="Restart to beginning")
        restart_button.on_click(self.restart)

        back_button = widgets.Button(icon="backward")
        back_button.on_click(self.back)

        play_button = widgets.Button(icon="play")
        play_button.on_click(self.play)

        play_all_from_button = widgets.Button(
            icon="play-circle", tooltip="Automatically play to the end"
        )
        play_all_from_button.on_click(self.play_all_from)

        forward_button = widgets.Button(icon="forward")
        forward_button.on_click(self.forward)

        return [restart_button, back_button, play_button, play_all_from_button, forward_button]

    def display(self):
        """Display the audio controls UI"""
        # Display in HBox
        display(self.circuit.draw())
        display(self.sub_circuits[self.index].draw())
        buttons = widgets.HBox(self.buttons)
        display(buttons)

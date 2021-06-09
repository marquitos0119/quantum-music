from time import sleep
from warnings import filterwarnings, resetwarnings

from matplotlib._api.deprecation import MatplotlibDeprecationWarning
from IPython.display import display, clear_output, HTML
from ipywidgets import widgets
from qiskit import QuantumCircuit
from qiskit.visualization import plot_state_qsphere

from quantum_music.circuit_functions import (
    get_cummulative_state_vectors,
    get_circuits_by_column,
    play_notes,
    get_notes,
)
from quantum_music.display import get_output_widget


class Jukebox:
    def __init__(self, circuit: QuantumCircuit):
        self.index = 0
        self.circuit = circuit
        self.sub_circuits = None
        self.state_vectors = None
        self.buttons = self.get_buttons()
        self.notes = []

        self.load_circuit(circuit)

        # Ignore warnings that come from Qiskit visualizations
        filterwarnings("ignore", category=MatplotlibDeprecationWarning)
        # Display UI controls
        self.display()

    def __del__(self):
        # Re-enable warnings from Qiskit visualizations
        resetwarnings()

    def refresh_output(self):
        """Removes previous output and refreshes the button controls"""
        clear_output(wait=True)
        self.display()

    def load_circuit(self, circuit: QuantumCircuit):
        """Overwrite the current circuit with the new circuit"""
        self.sub_circuits = get_circuits_by_column(circuit)
        self.state_vectors = get_cummulative_state_vectors(self.sub_circuits)
        self.notes = get_notes(self.state_vectors[self.index])

    def play(self, button):
        self.notes = get_notes(self.state_vectors[self.index])
        self.refresh_output()
        play_notes(self.notes)

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
        self.index = 0
        self.notes = get_notes(self.state_vectors[self.index])
        self.refresh_output()

    def back(self, button):
        if self.index == 0:
            return
        self.refresh_output()
        self.index -= 1
        self.play(button)

    def forward(self, button):
        if self.index == len(self.sub_circuits) - 1:
            return
        self.refresh_output()
        self.index += 1
        self.play(button)

    def get_buttons(self):
        play_all_from_button = widgets.Button(
            icon="play-circle", tooltip="Automatically play all columns"
        )
        play_all_from_button.on_click(self.play_all_from)
        play_all_from_button.style.button_color = "lightgreen"

        restart_button = widgets.Button(icon="fast-backward", tooltip="Restart to beginning")
        restart_button.on_click(self.restart)

        back_button = widgets.Button(icon="backward", tooltip="Go back a column and play")
        back_button.on_click(self.back)

        play_button = widgets.Button(icon="play", tooltip="Play one column")
        play_button.on_click(self.play)

        forward_button = widgets.Button(icon="forward", tooltip="Go forward a column and play")
        forward_button.on_click(self.forward)

        # Defines the display order from left to right
        return [play_all_from_button, restart_button, back_button, play_button, forward_button]

    def display(self):
        """Display the audio controls UI"""

        # Left HBox
        circuit_output = get_output_widget()
        notes_str = ",".join([note[0] for note in self.notes])
        with circuit_output:
            # Entire circuit
            display(self.circuit.draw())
            # One column
            display(HTML(f"<h3>Column {self.index}</h3>"))
            display(HTML(f"<p><b>Notes played</b>: {notes_str}</p>"))
            display(self.sub_circuits[self.index].draw())

        # Right HBox
        qsphere_output = get_output_widget()
        with qsphere_output:
            display(plot_state_qsphere(self.state_vectors[self.index]))
        display(widgets.HBox([circuit_output, qsphere_output]))

        # Control buttons
        buttons = widgets.HBox(self.buttons)
        display(buttons)

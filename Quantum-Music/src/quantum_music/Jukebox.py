from time import sleep
from warnings import filterwarnings, resetwarnings

from IPython.display import display, HTML
from ipywidgets import widgets, interactive
from qiskit import QuantumCircuit
from qiskit.visualization import plot_state_qsphere

from quantum_music.circuit_functions import (
    get_cummulative_state_vectors,
    get_circuits_by_column,
    play_notes,
    get_notes,
)
from quantum_music.display import get_output_widget
from quantum_music.scales import get_scale


class Jukebox:
    def __init__(
        self,
        circuit: QuantumCircuit,
        start_note=("C5", 523.25),
        pi_division=4,
        by_barrier=False,
    ):
        """
        :param circuit: the Qiskit circuit to play
        :param start_note: the first note in the scale. The Jukebox is configured
            to play the major scale starting from start_note
        :param pi_division: the number of divisions in pi rotation.
            Each division is a different pitch (musical note)
        :param by_barrier: if True, play notes only at barriers.
            Else, play at all columns of the circuit.
        """
        self.index = 0
        self.circuit = circuit
        self.sub_circuits = None
        self.state_vectors = None
        self.buttons = self.get_buttons()
        self.notes = []

        # Length of time for rests (between notes) and note
        self.rest_time = 0.0
        self.note_time = 1.0

        # Adjust scale
        self.scale = get_scale(start_note, pi_division=pi_division)
        self.pi_division = pi_division

        self.by_barrier = by_barrier
        self.load_circuit(circuit)

        # Ignore warnings that come from Qiskit visualizations
        filterwarnings("ignore")

        # Display UI controls
        self.circuit_output = None
        self.qsphere_output = None
        self.init_display()

    def __del__(self):
        # Re-enable warnings from Qiskit visualizations
        resetwarnings()

    def get_current_state_vector(self):
        """Returns the current column's state vector"""
        return self.state_vectors[self.index]

    def get_notes(self):
        """Helper function"""
        return get_notes(
            self.state_vectors[self.index], scale=self.scale, pi_division=self.pi_division
        )

    def load_circuit(self, circuit: QuantumCircuit):
        """Overwrite the current circuit with the new circuit"""
        self.sub_circuits = get_circuits_by_column(circuit, by_barrier=self.by_barrier)
        self.state_vectors = get_cummulative_state_vectors(self.sub_circuits)
        self.notes = self.get_notes()

    # Audio controls
    def set_rest_time(self, rest):
        self.rest_time = rest

    def set_note_time(self, note):
        self.note_time = note

    # Playback buttons
    def play(self, button):
        self.notes = self.get_notes()
        self.update_visual_display()
        play_notes(self.notes, note_time=self.note_time)

    def play_all_from(self, button):
        for i in range(self.index, len(self.state_vectors)):
            self.update_visual_display()
            self.index = i
            self.play(button)
            sleep(self.rest_time)

    def restart(self, button):
        """Moves back to the first column"""
        if self.index == 0:
            return
        self.index = 0
        self.notes = self.get_notes()
        self.update_visual_display()

    def back(self, button):
        if self.index == 0:
            return
        self.update_visual_display()
        self.index -= 1
        self.play(button)

    def forward(self, button):
        if self.index == len(self.sub_circuits) - 1:
            return
        self.update_visual_display()
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

    def update_visual_display(self):
        # Left HBox
        notes_str = ",".join([note[0] for note in self.notes])
        self.circuit_output.clear_output(wait=True)
        with self.circuit_output:
            display(HTML("<h2>Current State</h2>"))
            # One column/barrier section
            if self.by_barrier:
                label = "Barrier"
            else:
                label = "Column"
            display(HTML(f"<h3>{label} {self.index}</h3>"))
            display(HTML(f"<p><b>Notes played</b>: {notes_str}</p>"))
            display(self.sub_circuits[self.index].draw())

        # Right HBox
        self.qsphere_output.clear_output(wait=True)
        with self.qsphere_output:
            display(plot_state_qsphere(self.state_vectors[self.index]))

    def init_display(self):
        """Display the audio controls UI"""
        # Setup visual display
        self.circuit_output = get_output_widget()
        self.qsphere_output = get_output_widget()
        self.update_visual_display()
        entire_circuit_display = get_output_widget()
        with entire_circuit_display:
            display(HTML("<h2>Quantum Circuit</h2>"))
            if len(self.sub_circuits) < 15:
                display(self.circuit.draw())
            else:
                display(
                    HTML('<p style="color:gray">(this circuit is too large to be displayed.)</p>')
                )
        display(
            widgets.HBox(
                [entire_circuit_display, widgets.VBox([self.circuit_output, self.qsphere_output])]
            )
        )

        # Play, forward, back buttons
        buttons = widgets.HBox(self.buttons)
        display(buttons)

        # Audio controls
        audio_controls_label = widgets.HTML("<p><b>Duration</b></p>")
        rest_slider = interactive(self.set_rest_time, rest=(0.0, 1.0))
        note_slider = interactive(self.set_note_time, note=(0.10, 1.0))
        display(
            widgets.HBox(
                [
                    audio_controls_label,
                    rest_slider,
                    note_slider,
                ]
            )
        )

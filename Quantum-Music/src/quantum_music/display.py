"""Helper functions for displaying UI in notebooks"""

from ipywidgets import Output


def get_output_widget():
    """
    Can be used to place all output into one column in an HBox:
        out1 = get_inline_output_widget()
        # Capture stdout using "with" keyword:
        with out1:
            print('Hello!')
            display(circuit.draw())

        out2 = get_inline_output_widget()
        with out2:
            display(plot_state_qsphere(state_vector))

        # Display side-by-side
        HBox([out1, out2])
    """
    return Output(layout={"flex-direction": "row"})

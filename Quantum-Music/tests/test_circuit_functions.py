from quantum_music.circuit_functions import get_phases


class TestGetNotes:
    def test_get_notes_g_scale(self):
        state_vector = [-0.5879378 + 0.0j, 0.39284748 + 0.0j, -0.5879378 + 0.0j, 0.39284748 + 0.0j]
        phases = get_phases(state_vector)
        print("phases", phases)
        assert len(state_vector) == len(phases)

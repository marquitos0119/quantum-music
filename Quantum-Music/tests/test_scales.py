from quantum_music.scales import get_scale, c_scale


class TestScales:
    def test_c_scale(self):
        start_note = ("C4", 261.63 * 2)
        scale = get_scale(start_note, pi_division=4)

        for phase in c_scale:
            freq_diff = scale[phase][1] - c_scale[phase][1]
            assert freq_diff < 0.1

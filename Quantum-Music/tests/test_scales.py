from quantum_music.scales import get_scale, c_scale, g_scale


class TestScales:
    def test_c_scale(self):
        start_note = ("C5", 523.25)
        scale = get_scale(start_note, pi_division=4)

        for phase in c_scale:
            freq_diff = scale[phase][1] - c_scale[phase][1]
            assert freq_diff < 0.1

    def test_g_scale(self):
        start_note = ("G5", 783.99)
        scale = get_scale(start_note, pi_division=4)

        for phase in g_scale:
            print(f"phase: {phase}")
            freq_diff = scale[phase][1] - g_scale[phase][1]
            assert freq_diff < 0.1

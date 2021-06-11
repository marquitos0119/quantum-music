from quantum_music.scales import get_scale, c_scale


class TestScales:
    def test_get_scale(self):
        start_note = ("C4", 261.63 * 2)
        scale = get_scale(start_note)

        for phase in scale.keys():
            print(f"phase: {phase}")
            print("scale", scale[phase])
            print("c_scale", c_scale[phase])

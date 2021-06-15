from quantum_music.scales import get_scale, c_scale, g_scale


class TestScales:
    def test_c_scale(self):
        start_note = ("C5", 523.25)
        scale = get_scale(start_note, pi_division=4)

        for phase in c_scale:
            freq_diff = scale[phase][1] - c_scale[phase][1]
            assert freq_diff <= 1.0

    def test_g_scale(self):
        start_note = ("G5", 783.99)
        scale = get_scale(start_note, pi_division=4)

        for phase in g_scale:
            freq_diff = scale[phase][1] - g_scale[phase][1]
            assert freq_diff <= 1.0

    def test_g_scale_div_8(self):
        start_note = ("G5", 783.99)
        scale = get_scale(start_note, pi_division=8)

        for phase in scale:
            print(f"phase {phase}: freq={scale[phase]}")

    def test_d_scale(self):
        start_note = ("D4", 293.66)
        scale = get_scale(start_note, pi_division=8)

        for phase in scale:
            print(f"phase {phase}: freq={scale[phase]}")


# class TestFromQASM:
#    def test_pallet_town(self):
#        """From James!"""
#        qasm = """
#        OPENQASM 2.0;
#        include "qelib1.inc";
#        qreg q[2];
#        creg c[2];
#        ry(13*pi/8) q[0];
#        h q[1];
#        h q[0];
#        z q[0];
#        barrier q[0],q[1];
#        x q[1];
#        cp(11*pi/8) q[1],q[0];
#        x q[1];
#        cp(2*pi/8) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(15*pi/8) q[1],q[0];
#        x q[1];
#        cp(0) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(15*pi/8) q[1],q[0];
#        x q[1];
#        cp(pi/8) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(15*pi/8) q[1],q[0];
#        x q[1];
#        cp(0) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(6*pi/8) q[1],q[0];
#        x q[1];
#        cp(2*pi/8) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(14*pi/8) q[1],q[0];
#        x q[1];
#        cp(0) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(pi/8) q[1],q[0];
#        x q[1];
#        cp(15*pi/8) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(15*pi/8) q[1],q[0];
#        x q[1];
#        cp(0) q[0],q[1];
#        barrier q[0],q[1];
#        x q[1];
#        cp(15*pi/8) q[1],q[0];
#        x q[1];
#        cp(14*pi/8) q[0],q[1];
#        barrier q[0],q[1];
#        """
#
#        circuit = QuantumCircuit.from_qasm_str(qasm)
#

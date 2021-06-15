OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
ry(13*pi/8) q[0];
h q[1];
h q[2];
x q[0];
h q[0];
barrier q[0],q[1],q[2];
p(7*pi/8) q[0];
p(2*pi/8) q[1];
cp(4*pi/8) q[2],q[0];
cp(1*pi/8) q[2],q[1];
barrier q[0],q[1],q[2];
p(13*pi/8) q[0];
barrier q[0],q[1],q[2];
p(1*pi/8) q[0];
barrier q[0],q[1],q[2];
p(13*pi/8) q[0];
barrier q[0],q[1],q[2];
p(1*pi/8) q[0];
barrier q[0],q[1],q[2];
p(13*pi/8) q[0];
barrier q[0],q[1],q[2];
p(3*pi/8) q[0];
barrier q[0],q[1],q[2];
p(1*pi/8) q[0];
barrier q[0],q[1],q[2];

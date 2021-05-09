clear
clc

rol=7800;
specific_heat=125;
Conductivity=15;

MASS=load('D:\SIMULIA\Temp\3D\3D_M\SquarePlateWithHole3D_M_MASS1.mtx');
m_num=length(MASS(:,1));
nodes_num=1685;
m1=m_num/3;
M(1:nodes_num,1:nodes_num)=0;

for i=1:1:m1
    a1=MASS(3*i-2,1);
    a2=MASS(3*i-2,3);
    M(a1,a2)=MASS(3*i-2,5);
    M(a2,a1)=MASS(3*i-2,5);
end

M1=M*specific_heat;

clear
clc
STIFF=load('D:\SIMULIA\Temp\3D\3D_K\SquarePlateWithHole3D_KTHERM1_STIF1.mtx');
k_num=length(STIFF(:,1));
nodes_num=1685;
for i=1:1:k_num
    b1=STIFF(i,1);
    b2=STIFF(i,3);
    K(b1,b2)=STIFF(i,5);
    K(b2,b1)=STIFF(i,5);
end

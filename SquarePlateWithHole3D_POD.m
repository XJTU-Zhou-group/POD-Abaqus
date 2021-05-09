clear
clc

num=500;
dt=0.1;
rol=7800;
specific_heat=125;
Conductivity=15;

load('DATA_3D.mat');

load('3D_loadless_K.mat');
K=K1;

load('3D_M.mat');

load('3D_L.mat');

%初始化
T(:,1)=DATA_3D(:,1);
nodes_num=length(T(:,1));

%寻找边界条件节点编号
n=1;
for i=1:1:nodes_num
    T_initial=DATA_3D(i,2);
    if T_initial==200
        initial_200(n)=i;
        n=n+1;
    end
end

%初始化边界条件
l_initial=length(initial_200);

for in=1:1:l_initial
    in_id=initial_200(in);
    T(in_id,1)=200;
end

[U,S,V] = svd(DATA_3D(:,1:100),'econ');
U1=U(:,1:17);

T2=U1*U1'*DATA_3D;

%降阶
TT=U1'*T;
% T1=U1*TT1;
KK=U1'*K*U1;

MM=U1'*M*U1;

MM1=inv(MM);

LL=U1'*L;

%降阶后求解
num2=500;
dt=0.1;
for t=1:1:num2
%     F=M1*L(:,t);
    FF=MM1*LL(:,t);
    TTq(:,t)=MM1*-KK*TT(:,t)+FF;
    TT(:,t+1)=TT(:,t)+TTq(:,t)*dt;
    time(t+1,1)=t*dt;
    T_ran2=U1*TT(:,t+1);
    for in=1:1:l_initial       
        in_id=initial_200(in);
        T_ran2(in_id,1)=200;
    end
    TT(:,t+1)=U1'*T_ran2;
end

Tcheck=U1*TT;

T16=DATA_3D(16,:)';
T16check=Tcheck(16,:)';

T504=DATA_3D(504,:)';
T504check=Tcheck(504,:)';

T148=DATA_3D(148,:)';
T148check=Tcheck(148,:)';

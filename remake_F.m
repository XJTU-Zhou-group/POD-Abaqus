clear
clc
num=500;
node_num=1685;
L(1:node_num,1)=0;
for t=1:1:500
    name=num2str(t, '%d');
    txt_name=['D:\SIMULIA\Temp\3D\3D_L\SquarePlateWithHole3D_LTHERM1_LOAD',name,'.mtx'];
    f=fopen(txt_name);
    ALL=textscan(f,'%s','Delimiter',{','},'HeaderLines',2);

    all=ALL{1};
    len=length(ALL{1,1})/3;

    for i=1:1:len
        
        node_2=all{i*3-2};
        node_id=str2num(node_2);
        load_2=all{i*3};
        load_val=str2num(load_2);
        L(node_id,t)=load_val;
    end
    fclose('all');
end

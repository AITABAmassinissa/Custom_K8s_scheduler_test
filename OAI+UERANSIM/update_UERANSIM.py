import os

namespace='oai'
ip_adress="10.244.0.1"
network="cni0"
dnn=["oai1","oai2","oai3"]
gnbfiles=["OAI-gnb.yaml","OAI-gnb2.yaml","OAI-gnb3.yaml"]
uefiles=["OAI-ue.yaml","OAI-ue2.yaml","OAI-ue3.yaml"]
nci=["0x000000010","0x000000020","0x000000030"]
sst=[1,2,3]

retour=os.popen("kubectl get pods -n "+namespace).read() 
amf_ip=os.popen("kubectl get pod -n "+namespace+" $(kubectl get pods --namespace "+namespace+" -l "+"app.kubernetes.io/name=oai-amf"+" -o jsonpath="+"{.items[0].metadata.name}"+") --template '{{.status.podIP}}'").read()

os.system("sudo ifconfig "+network+":"+str(1)+" "+str(ip_adress)+" up")
#update OAI-gnb file for UERANSIM 
data={}
for i in range(0,len(dnn)):
    with open(r'OAI-gnb.yaml', 'r') as file:
        data[i] = file.read()
        file.close()
    
    data[i] = data[i].replace("xxx", str(ip_adress))
    data[i] = data[i].replace("yyy", str(amf_ip))
    data[i] = data[i].replace("zzz", str(sst[i]))
    data[i] = data[i].replace("ttt", str(nci[i]))
    with open(r'UERANSIM/build/'+gnbfiles[i], 'w') as file:
        file.write(data[i])
        file.close()
#update OAI-ue file for UERANSIM 
    with open(r'OAI-ue.yaml', 'r') as file:
        data[i] = file.read()
        file.close()
    data[i] = data[i].replace("xxx", str(ip_adress))
    data[i] = data[i].replace("yyy", dnn[i])
    data[i] = data[i].replace("zzz", str(sst[i]))
    with open(r'UERANSIM/build/'+uefiles[i], 'w') as file:
        file.write(data[i])
        file.close()
print("UERANSIM files configuration updated")
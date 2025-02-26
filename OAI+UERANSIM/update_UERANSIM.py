import os

namespace='oai'
ip_adress="10.244.0.1"
network="cni0"
dnn=["oai","oai2","oai3"]
gnbfiles=["OAI-gnb.yaml","OAI-gnb2.yaml","OAI-gnb3.yaml"]
uefiles=["OAI-ue.yaml","OAI-ue2.yaml","OAI-ue3.yaml"]
sst=[1,128,130]

retour=os.popen("kubectl get pods -n "+namespace).read() 
Running=0
amf_ip=os.popen("kubectl get pod -n "+namespace+" $(kubectl get pods --namespace "+namespace+" -l "+"app.kubernetes.io/name=oai-amf"+" -o jsonpath="+"{.items[0].metadata.name}"+") --template '{{.status.podIP}}'").read()
os.system("sudo ifconfig "+network+":"+str(1)+" "+str(ip_adress)+" up")
#update OAI-gnb file for UERANSIM 
with open(r'OAI-gnb.yaml', 'r') as file:
    data = file.read()
    file.close()
data = data.replace("xxx", str(ip_adress))
data = data.replace("yyy", str(amf_ip))
for i in range(0,len(dnn)):
    data = data.replace("zzz", sst[i])
    with open(r'UERANSIM/build/'+gnbfiles[i], 'w') as file:
        file.write(data)
        file.close()
#update OAI-ue file for UERANSIM 
with open(r'OAI-ue.yaml', 'r') as file:
    data = file.read()
    file.close()
data = data.replace("xxx", str(ip_adress))

for i in range(0,len(dnn)):
    data = data.replace("yyy", dnn[i])
    data = data.replace("zzz", sst[i])
    with open(r'UERANSIM/build/'+uefiles[i], 'w') as file:
        file.write(data)
        file.close()
print("UERANSIM files configuration updated")
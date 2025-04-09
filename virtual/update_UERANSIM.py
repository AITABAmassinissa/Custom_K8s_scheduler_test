import os

namespace='oai'
ip_adress="10.244.0.1"
network="cni0"
dnn=["oai","oai2","oai3","oai4"]
nci=["0x000000010","0x000000020","0x000000030","0x000000040"]
sst=[1, 2, 3, 4]
UERANSIM_name="ueransim-sst-1"
amf_ip=os.popen("kubectl get pod -n "+namespace+" $(kubectl get pods --namespace "+namespace+" -l "+"app.kubernetes.io/name=oai-amf"+" -o jsonpath="+"{.items[0].metadata.name}"+") --template '{{.status.podIP}}'").read()
UERANSIM_ip=os.popen("kubectl get pod -n "+namespace+" $(kubectl get pods --namespace "+namespace+" -l "+"app.kubernetes.io/name="+UERANSIM_name+" -o jsonpath="+"{.items[0].metadata.name}"+") --template '{{.status.podIP}}'").read()
os.system("sudo ifconfig "+network+":"+str(1)+" "+str(ip_adress)+" up")
#update OAI-gnb file for UERANSIM 
data={}
for i in range(0,len(dnn)):
    with open(r'OAI-gnb.yaml', 'r') as file:
        data[i] = file.read()
        file.close()
    data[i] = data[i].replace("xxx", str(UERANSIM_ip))
    data[i] = data[i].replace("yyy", str(amf_ip))
    data[i] = data[i].replace("ttt", str(nci[i]))
    data[i] = data[i].replace("zzz", str(sst[i]))
    with open(r'UERANSIM/'+"OAI-gnb-"+str(sst[i])+".yaml", 'w') as file:
        file.write(data[i])
        file.close()
#update OAI-ue file for UERANSIM 
    with open(r'OAI-ue.yaml', 'r') as file:
        data[i] = file.read()
        file.close()
    data[i] = data[i].replace("xxx", str(UERANSIM_ip))
    data[i] = data[i].replace("yyy", dnn[i])
    data[i] = data[i].replace("zzz", str(sst[i]))
    with open(r'UERANSIM/'+"OAI-ue-"+str(sst[i])+".yaml", 'w') as file:
        file.write(data[i])
        file.close()
print("UERANSIM files configuration updated")

#kubectl apply -f UERANSIM.yaml 
#kubectl cp ./UERANSIM/OAI-gnb-1.yaml oai/ueransim-sst-1:/UERANSIM/build
#kubectl cp ./UERANSIM/OAI-ue-1.yaml oai/ueransim-sst-1:/UERANSIM/build
#kubectl exec -it ueransim-sst-1 -n oai -- /bin/bash
#./UERANSIM/build/nr-gnb -c UERANSIM/build/OAI-gnb-1.yaml
#./UERANSIM/build/nr-ue -c UERANSIM/build/OAI-ue-1.yaml -i imsi-208950000000031
#ping -c 3 -I uesimtun0 google.com

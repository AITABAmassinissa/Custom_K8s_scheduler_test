all : clean


scenario1:
	python3 sim.py 0 my-schedulerpy logs/my-schedulerpy

clean:
	-(! (ps -elf|pgrep nr-ue)) ||sudo kill -9 $$(ps -elf|pgrep nr-ue)
	-(! (ps -elf|pgrep nr-gnb)) ||sudo kill -9 $$(ps -elf|pgrep nr-gnb)
	-(! (ps -elf|pgrep nr-binder)) ||sudo kill -9 $$(ps -elf|pgrep nr-binder)
	-(! (pgrep -f UE.py)) ||sudo kill -9 $$(pgrep -f UE.py)
	-(! (pgrep -f sim.py)) ||sudo kill -9 $$(pgrep -f sim.py)

multus:
	kubectl delete -f ./multus-cni/deployments/multus-daemonset-thick.yml
	kubectl delete ns oai --ignore-not-found=true
	kubectl apply -f ./multus-cni/deployments/multus-daemonset-thick.yml
	kubectl create ns oai
push:
	git add .
	git commit -m "p" 
	git push
pull: 
	git pull 
	sleep 5
	helm dependency update 5gc/oai-5g-advance/
	helm install basic 5gc/oai-5g-advance/ -n oai

nrf:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-nrf | head -n 1) -n oai | grep OAI-SMF
nrf2:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-nrf2 | head -n 1) -n oai
amf:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-amf | head -n 1) -n oai
smf:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-smf | head -n 1) -n oai
smf2:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-smf2 | head -n 1) -n oai
smf3:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-smf3 | head -n 1) -n oai
upf:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-upf | head -n 1) -n oai
upf2:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-upf2 | head -n 1) -n oai
upf3:
	kubectl logs $$(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-upf3 | head -n 1) -n oai
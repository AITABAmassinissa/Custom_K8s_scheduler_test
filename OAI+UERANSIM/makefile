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

pull: 
	git pull 
	helm dependency update oai-5g-core-3slices/oai-5g-advance/
	helm install basic oai-5g-core-3slices/oai-5g-advance/ -n oai

logs:
	kubectl logs $(kubectl get pods -n oai --no-headers -o custom-columns=":metadata.name" | grep oai-nrf | head -n 1) -n oai | grep OAI-SMF

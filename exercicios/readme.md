
# Agenda
1) Ambiente
2) Rancher HA - Preparação
3) Rancher HA - Instalação
4) Ambiente desenvolvimento
5) Ambiente Homologação
6) Ambiente de Produção
7) NFS
8) ArgoCD - Instalação
9) Pipeline - Desenvolvimento
10) Pipeline - Homologação
11) Pipeline - Produção






# rancher-ha

Repositorio usado para mostrar instalação do Rancher em HA.

https://rancher.com/docs/rancher/v2.x/en/installation/how-ha-works/



## Requisitos

1 DNS
1 máquina para load balancer
3 máquinas para o rancher-server

Usando na aula: UBUNTU 22.04 LTS

## Docker instalado em todas as máquinas

```sh
#!/bin/sh
sudo su
curl https://releases.rancher.com/install-docker/20.10.sh | sh
usermod -aG docker ubuntu

```

## Portas

https://rancher.com/docs/rancher/v2.x/en/installation/requirements/ports/


## RKE

https://rancher.com/docs/rancher/v2.x/en/installation/k8s-install/create-nodes-lb/


Why three nodes?

In an RKE cluster, Rancher server data is stored on etcd. This etcd database runs on all three nodes.

The etcd database requires an odd number of nodes so that it can always elect a leader with a majority of the etcd cluster. If the etcd database cannot elect a leader, etcd can suffer from split brain, requiring the cluster to be restored from backup. If one of the three etcd nodes fails, the two remaining nodes can elect a leader because they have the majority of the total number of etcd nodes.


## INCIO

Logar na máquina do ELB - onde tudo será realizado
Instalar o kubectl nela também
Instalar o RKE nela também.

```sh
ssh -i devopsdevops.pem ubuntu@18.223.118.90                  # - NGINX - LB

ssh -i devopsdevops.pem ubuntu@18.216.214.80   172.31.33.192   # - rancher-server-1
ssh -i devopsdevops.pem ubuntu@18.222.165.115  172.31.32.92   # - rancher-server-2
ssh -i devopsdevops.pem ubuntu@52.14.242.42    172.31.45.230    # - rancher-server-3
```

### Copiar chave PEM para máquina NGINX para ela logar nas outras.

Para servidores com senha, olhar arquivo ssh-no-cloud.md

```sh
# USAR user ubuntu
# Copiar o PEM e colar no ARQUIVO.
vi ~/.ssh/id_rsa
chmod 600 /home/ubuntu/.ssh/id_rsa

ssh ubuntu@172.31.45.101
ssh ubuntu@172.31.44.10
ssh ubuntu@172.31.45.120
```


# Instalar Kubectl
```sh
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```


# Instalar RKE
```sh
curl -LO https://github.com/rancher/rke/releases/download/v1.4.1/rke_linux-amd64
mv rke_linux-amd64 rke
chmod +x rke
sudo mv ./rke /usr/local/bin/rke
rke --version
```


# Rodar RKE

https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-cluster-setup/high-availability-installs



```sh
rke up --config ./rancher-cluster.yml

# Após o cluster subir:...
export KUBECONFIG=$(pwd)/kube_config_rancher-cluster.yml

kubectl get nodes
kubectl get pods --all-namespaces

# SALVAR OS ARQUIVOS


# Instalar HELM
curl -LO https://get.helm.sh/helm-v3.3.1-linux-amd64.tar.gz
tar -zxvf helm-v3.3.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm

```


# Parte 2 - Instalação rancher

https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-cluster-setup/high-availability-installs

## Cert Manager
```sh


# Certificate Manager
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.yaml

# kubectl create namespace cert-manager

#helm repo add jetstack https://charts.jetstack.io

#helm repo update
#helm install \
# cert-manager jetstack/cert-manager \
# --namespace cert-manager \
# --version v1.7.0

kubectl get pods --namespace cert-manager
```


## Rancher

```sh

# Instalar o Rancher - Preparar
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
kubectl create namespace cattle-system

# Instalar Rancher
helm install rancher rancher-stable/rancher \
 --namespace cattle-system \
 --set hostname=rancher.devopsforlife.io 
# --set ingress.tls.source=letsEncrypt
 

helm upgrade rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=rancher.devopsforlife.io 


# Verificar deployment
kubectl -n cattle-system rollout status deploy/rancher
kubectl -n cattle-system get deploy rancher


# RODAR O NGINX
sudo vi /etc/nginx.conf
docker run -d --restart=unless-stopped \
 -p 80:80 -p 443:443 \
 -v /etc/nginx.conf:/etc/nginx/nginx.conf \
 nginx:1.14
```




DEV

ssh -i devopsdevops.pem ubuntu@3.20.234.67






# Kubernetes-HA - Alta Disponibilidade


Repositorio usado para mostrar instalação do Rancher em HA.

https://rancher.com/docs/rancher/v2.x/en/troubleshooting/kubernetes-components/etcd/

https://rancher.com/learning-paths/building-a-highly-available-kubernetes-cluster/


## Requisitos

Cluster Kubernetes HA de Produção

3 instâncias para ETCD - Podendo perder 1
2 instâncias para CONTROLPLANE - Podendo perder 1
4 instâncias para WORKER - Podendo perder todas

Usando na demonstração: UBUNTU 16.04 LTS

## Docker instalado em todas as máquinas

```sh
#!/bin/bash
curl https://releases.rancher.com/install-docker/20.10.sh | sh
usermod -aG docker ubuntu
```


## INCIO

Abrir o Rancher e criar um novo cluster.

Adicionar novo cluster com Existing Nodes


```sh
$ ssh -i devops-ninja.pem ubuntu@3.227.241.169   # - Rancher-server

#ETCD
$ ssh -i devops-ninja.pem ubuntu@34.200.230.114  # - etcd-1
$ ssh -i devops-ninja.pem ubuntu@3.238.62.131    # - etcd-2
$ ssh -i devops-ninja.pem ubuntu@3.230.119.189   # - etcd-3

#CONTROLPLANE
$ ssh -i devops-ninja.pem ubuntu@3.238.34.100  # - controlplane-1
$ ssh -i devops-ninja.pem ubuntu@3.236.176.198 # - controlplane-2

#WORKER
$ ssh -i devops-ninja.pem ubuntu@34.205.53.204 # - worker-1
$ ssh -i devops-ninja.pem ubuntu@3.236.174.43  # - worker-2
$ ssh -i devops-ninja.pem ubuntu@3.80.162.150  # - worker-3
$ ssh -i devops-ninja.pem ubuntu@3.237.75.239  # - worker-4


# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name etcd-1 --etcd

# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name etcd-2 --etcd

# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name etcd-3 --etcd

# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name controlplane-1 --controlplane

# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name controlplane-2 --controlplane

# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name worker-1 --worker

# docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.5.0 --server https://3.227.241.169 --token zw9dgzb99n7fkg7l7lsb4wn6p49gmhcfjdp9chpzllzgpnjg9gv967 --ca-checksum 7c481267daae071cd8ad8a9dd0f4c5261038889eccbd1a8e7b0aa1434053731b --node-name worker-2 --worker


```















## NFS Server para Infra e demais clusters

```sh
K8S-NFS-PROD
SSH: 170.231.14.234:41492 
Login: ubuntu
Senha: uYP3Z97*L
```
ssh -p 41492 ubuntu@170.231.14.234

NFS Server IP: 10.40.80.19
NFS Clients IPs: From the 10.40.80.0/24 range


```sh
sudo apt install nfs-kernel-server -y

# verificar versão

sudo cat /proc/fs/nfsd/versions
# -2 +3 +4 +4.1 +4.2

  # /etc/default/nfs-kernel-server
  # /etc/default/nfs-common

# DIRETORIO
# /srv/nfs4  

sudo mkdir -p /srv/nfs4/infra
sudo mkdir -p /srv/nfs4/qa
sudo mkdir -p /srv/nfs4/prod

sudo chown nobody:nogroup /srv/nfs4/infra
sudo chown nobody:nogroup /srv/nfs4/qa
sudo chown nobody:nogroup /srv/nfs4/prod

sudo chmod -R 777 /srv/nfs4/infra
sudo chmod -R 777 /srv/nfs4/qa
sudo chmod -R 777 /srv/nfs4/prod

sudo vi /etc/exports

/srv/nfs4/infra 10.40.80.27(rw,sync,no_subtree_check) 10.40.80.24(rw,sync,no_subtree_check) 10.40.80.29(rw,sync,no_subtree_check)
/srv/nfs4/qa 10.40.80.28(rw,sync,no_subtree_check) 10.40.80.16(rw,sync,no_subtree_check) 10.40.80.26(rw,sync,no_subtree_check)

# /srv/nfs4/prod 10.40.80.0/24 (rw,sync,no_subtree_check)


# SEMPRE QUE NOVAS MAQUINAS FOREM ADICIONADAS AO CLUSTER, É PRECISO INSERILAS NO NFS

sudo exportfs -a

systemctl status nfs-server

systemctl restart nfs-server
sudo ufw status
```



## Configurar o cliente NFS para teste na máquina

```sh
sudo apt update
sudo apt install nfs-common -y

sudo mkdir -p /mnt/client_infra2
sudo mount 10.40.80.19:/srv/nfs4/infra /mnt/client_infra2
cd /mnt/client_infra2
touch nfs_share.txt

sudo umount -l /mnt/client_infra2
```

## Helm Chart - NFS Driver for Kubernetes

StorageClass para Kubernetes para NFS
https://github.com/kubernetes-csi/csi-driver-nfs

```sh
helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs --namespace kube-system --version v4.1.0
```


## nfs-infra.yaml
```yaml
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-csi
provisioner: nfs.csi.k8s.io
parameters:
  server: 10.40.80.19
  share: /srv/nfs4/infra
reclaimPolicy: Delete
volumeBindingMode: Immediate
mountOptions:
  - hard
  - nfsvers=4.1
```


## nfs-qa.yaml
```yaml
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-csi
provisioner: nfs.csi.k8s.io
parameters:
  server: 10.40.80.19
  share: /srv/nfs4/qa
reclaimPolicy: Delete
volumeBindingMode: Immediate
mountOptions:
  - hard
  - nfsvers=4.1
```


# pvc.yaml
```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  storageClassName: nfs-csi
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 5Gi
```

```sh
kubectl describe pvc my-pvc
```




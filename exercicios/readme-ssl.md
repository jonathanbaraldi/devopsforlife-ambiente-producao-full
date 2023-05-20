
# Agenda
1) Rancher HA - Preparação
2) Rancher HA - Instalação

3) Aplicação - Preparação
4) Aplicação - Build
5) Aplicação - Deploy
6) Aplicação - SSL

7) ArgoCD - Repositório privado

8) Ambiente de Produção - Considerações

9) Revisão 


# rancher-ha

Repositorio usado para mostrar instalação do Rancher em HA.

https://rancher.com/docs/rancher/v2.x/en/installation/how-ha-works/



## Requisitos

1 DNS
1 máquina para load balancer - 1/1 
1 máquinas para o rancher-server - 2/8 -50gb 

Usando na aula: UBUNTU 22.04 LTS

## Docker instalado em todas as máquinas

```sh
#!/bin/sh
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


 
 
# Aula 1 - Rancher HA - Preparação

 
## INCIO

Logar na máquina do ELB - onde tudo será realizado
Instalar o kubectl nela também
Instalar o RKE nela também.

```sh
 
ssh -i devops-full.pem ubuntu@3.143.213.134                  # - NGINX - LB

ssh -i devops-full.pem ubuntu@3.135.65.84       172.31.17.104   # - rancher-server-1
# ssh -i devopsdevops.pem ubuntu@18.222.165.115  172.31.32.92    # - rancher-server-2
# ssh -i devopsdevops.pem ubuntu@52.14.242.42    172.31.45.230   # - rancher-server-3
 
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
 
ssh ubuntu@172.31.33.192
ssh ubuntu@172.31.32.92
ssh ubuntu@172.31.45.230
 
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
 
# Aula 3 - Rancher HA - Instalação rancher


https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-references/helm-chart-options#external-tls-termination


## Rancher


## Instalar o Rancher - Preparar 

```sh
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
kubectl create namespace cattle-system

helm install rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=rancher.devopsforlife.io  \
  --set replicas=1 \
  --set tls=external 

helm upgrade rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=rancher.devopsforlife.io  \
  --set replicas=1 \
  --set tls=external   


helm uninstall rancher

kubectl -n cattle-system rollout status deploy/rancher
kubectl -n cattle-system get deploy rancher

https://ranchermanager.docs.rancher.com/v2.5/pages-for-subheaders/install-upgrade-on-a-kubernetes-cluster#3-choose-your-ssl-configuration
```


## Pegar a senha de admin para logar

If this is the first time you installed Rancher, get started by running this command and clicking the URL it generates:

```sh
echo https://rancher.isthmus.com.br/dashboard/?setup=$(kubectl get secret --namespace cattle-system bootstrap-secret -o go-template='{{.data.bootstrapPassword|base64decode}}')
```

To get just the bootstrap password on its own, run:

```sh
kubectl get secret --namespace cattle-system bootstrap-secret -o go-template='{{.data.bootstrapPassword|base64decode}}{{ "\n" }}'

# sht6cp57wg4qwh69dsdk7mn8d2zfzb7ccs59p45v2fxj26jnpwp2bf
# sht6cp57wg4qwh69dsdk7mn8d2zfzb7ccs59p45v2fxj26jnpwp2bf

kubectl -n cattle-system rollout status deploy/rancher
```

mpjlnfdl9qxqndc7plxldtz25rdqjwvr7qlkgdxmj9qn2rnnxdxz89




## 8 - Criação do certificado
Criar certificado para nossos dominios:

 *.devopsforlife.io
```sh
> openssl genrsa -out privkey.pem 2048

> openssl req -new -key privkey.pem -out cert.csr

> openssl x509 -req -days 365 -in cert.csr -signkey privkey.pem -out fullchain.pem



```




# RODAR O NGINX
```
sudo vi /etc/nginx.conf
docker run -d --restart=unless-stopped \
 -p 80:80 -p 443:443 \
 -v /etc/nginx.conf:/etc/nginx/nginx.conf \
 -v /home/ubuntu:/certs \
 nginx:1.14
```




 
# Kubernetes-HA - Alta Disponibilidade
 
 *.dev.devopsforlife.io
```sh
openssl genrsa -out tls.key 2048
openssl req -new -key tls.key -out tls.csr
openssl x509 -req -in tls.csr -signkey tls.key -out tls.crt -days 365

kubectl create secret tls prod-devopsforlife --key tls.key --cert tls.crt

# default

```

# Aula 3 - Ambiente Produção


## Kubernetes-HA - Alta Disponibilidade
 
Repositorio usado para mostrar instalação do Rancher em HA.

https://rancher.com/docs/rancher/v2.x/en/troubleshooting/kubernetes-components/etcd/

https://rancher.com/learning-paths/building-a-highly-available-kubernetes-cluster/


# Aula 3 - Aplicação - Preparação
  Pasta /app

# Aula 4 - Aplicação - Build
  Pasta /app

# Aula 5 - Aplicação - Deploy
  Pasta /app


# Aula 6 - Aplicação - SSL

Criação do certificado

Criar certificado para nossos dominios:

*.prod.devopsforlife.io


```sh
> openssl req -new -x509 -keyout server.key -out server.crt -days 365 -nodes
Country Name (2 letter code) [AU]:DE
State or Province Name (full name) [Some-State]:Germany
Locality Name (eg, city) []:nameOfYourCity
Organization Name (eg, company) [Internet Widgits Pty Ltd]:nameOfYourCompany
Organizational Unit Name (eg, section) []:nameOfYourDivision
Common Name (eg, YOUR name) []:*.example.com
Email Address []:webmaster@example.com
```

```sh
kubectl create secret tls my-tls-secret --key server.key --cert server.crt
```

Update do Ingress.









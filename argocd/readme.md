
# Aula 8 - ArgoCD - Instalação

https://www.digitalocean.com/community/tutorials/how-to-deploy-to-kubernetes-using-argo-cd-and-gitops


```sh
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

watch kubectl get pods -n argocd

# kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

biMzQUT5oCuWpTjm
```


# Instalar Kubectl
```sh
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```

# ArgoCD
```sh
sudo curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd
```


# Ingress

```
kubectl apply -f ingress.yaml
```

# KUBECTL

```sh
kubectl config use-context dev-ip-172-31-37-33
kubectl config use-context dev-ip-172-31-37-33
```


## Argo Login

```sh
argocd login localhost:8080

argocd login argocd.infra.devopsforlife.io:443

kubectl config get-contexts -o name
```

## ADICIONANDO O CLUSTER DE DEV PARA O ARGOCD

Usar o arquivo com o IP interno do kubeconfig

```sh
argocd cluster add dev-ip-172-31-37-33

qa-ip-172-31-41-237
```

## ADICIONANDO O CLUSTER DE QA PARA O ARGOCD


```sh
argocd cluster add qa-ip-172-31-41-237

```


## ADICIONANDO O CLUSTER DE PROD PARA O ARGOCD



```sh
argocd cluster add prod-ip-172-31-41-5

```





# Criando Apps


https://github.com/jonathanbaraldi/argocd-example-apps


## Aula 9 - dev
```sh
argocd app create helm-guestbook-dev  --repo https://github.com/jonathanbaraldi/argocd-example-apps --path helm-guestbook --dest-server https://172.31.37.33:6443 --dest-namespace default

argocd app set helm-guestbook-dev --values values-dev.yaml

argocd app get helm-guestbook-dev
argocd app sync helm-guestbook-dev
```


## Aula 10 - qa
```sh
argocd app create helm-guestbook-qa  --repo https://github.com/jonathanbaraldi/argocd-example-apps --path helm-guestbook --dest-server https://172.31.41.237:6443 --dest-namespace default


argocd app set helm-guestbook-qa --values values-qa.yaml

argocd app get helm-guestbook-qa
argocd app sync helm-guestbook-qa
```



## Aula 11 - prod
```sh
argocd app create helm-guestbook-prod  --repo https://github.com/jonathanbaraldi/argocd-example-apps --path helm-guestbook --dest-server https://172.31.41.5:6443 --dest-namespace default

argocd app set helm-guestbook-qa --values values-prod.yaml

argocd app get helm-guestbook-prod
argocd app sync helm-guestbook-prod
```



*** 
argocd app set guestbook -p image=example/guestbook:abcd123
argocd app sync guestbook
*** 







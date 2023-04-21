
## 2 - Criação da instância do RancherServer pela aws-cli.

```sh 

# RANCHER SERVER

# --image-id              ami-07638e60c0d01f44f
# --instance-type         t3.medium 
# --key-name              multicloud 
# --security-group-ids    sg-0b0e8363b215900f0 
# --subnet-id             subnet-4f5e7705

aws ec2 run-instances --image-id ami-0ab0629dba5ae551d --count 1 --instance-type t3.medium --key-name devops2 --security-group-ids sg-0b0e8363b215900f0 --subnet-id subnet-4f5e7705 --user-data file://rancher.sh --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=rancherserver}]' 'ResourceType=volume,Tags=[{Key=Name,Value=rancherserver}]' 

```


## 3 - Configuração do Rancher
Acessar o Rancher e configurar

https://3.134.108.24

## 4 - Configuração do Cluster Kubernetes.
Criar o cluster pelo Rancher e configurar.



## 5 - Deployment do cluster pela aws-cli

```sh
# --image-id ami-01e7ca2ef94a0ae86
# --count 3 
# --instance-type t3.large 
# --key-name multicloud 
# --security-group-ids sg-0b0e8363b215900f0 
# --subnet-id subnet-09c5a4961e6056757 
# --user-data file://k8s.sh



aws ec2 run-instances --image-id ami-0ab0629dba5ae551d --count 1 --instance-type t3.2xlarge --key-name devops2 --security-group-ids sg-0b0e8363b215900f0 --subnet-id subnet-4f5e7705 --user-data file://node.sh   --block-device-mapping "[ { \"DeviceName\": \"/dev/sda1\", \"Ebs\": { \"VolumeSize\": 70 } } ]" --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=k8s}]' 'ResourceType=volume,Tags=[{Key=Name,Value=k8s}]'     
```
```sh
sudo su
mkdir -p /home/root/.ssh
chmod -R 777 /root/ubuntu
# CRIAR a key pair
ssh-keygen
# Irá popular o diretório...
~/.ssh/

# NAO EXISRTIA E NAO TINHA PERMISSAO
Your identification has been saved in /your_home/.ssh/id_rsa
Your public key has been saved in /your_home/.ssh/id_rsa.pub

vi ~/.ssh/authorized_keys
#colar o conteudo do   cat ~/.ssh/id_rsa.pub  -  da maquina de origem

# ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7PbBtktoId0/mTmEkJ11wdUh8xbFP2Tmz7xM+XamPu8dyfjdUnJAyRFHiu4eIJtFWwdAH4s8ri5aOoXPoh33nwnvcZWc41XtBPlU/RNgfXhluUy44B/vm+TRg9OUSLQTf5jxfSdD8M9EnCwjNFybpYjwnTz2gTZ2b18bgYb0wW2myWKe2gf5V7IgJzKvSri2bPOheg6LTXKFlUqkgI2Iq+QxYzaiKGhBi5i1V+xiDHr0px85fyo8Du/grFtiiixwCaGPN5EMFsjKkXAo6S1v1zwDeT+GTPVUqkyQxS517fyeJrzk1oT2Ebr24DYEBhxqVJsv/oEod3bdlZYREN32rTWhJPub1XJAHUS3i/1q7VhUfho0RftrTaHSVcvRDnywgDAUr4h4hJMB+lN4UOv/utfhxGG0ZImk/dktKNtlucGa74OemocXU5BT3a1DeCm05CYgP7s04cGltl/pCDqLgvcKrvvbFEIu1SNSiMmkOXfcq9OHJmmOYPEllAqU/rWM= root@gaucha-b2b1

chown -R root:root ~/.ssh

vi /etc/ssh/sshd_config
# PERMITIR LOGIN COMO ROOT
# TIRAR A SENHA
# PERMIRIT O ARQUIVO authorized_keys
systemctl restart ssh
```
#!/bin/sh
sudo su
curl https://releases.rancher.com/install-docker/20.10.sh | sh
usermod -aG docker ubuntu

docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run  rancher/rancher-agent:v2.6.9 --server https://rancher.devopsforlife.io --token 8zz86hzx4r6mx7m24tq4btsfq6hpz2xj5x4bqpr96fgv9qb2sh98rv --ca-checksum 4450a037829632e47b844843b1af96b7f5c2fbec075e4df8ff15254b36e1b1d3 --etcd --controlplane --worker
#!/bin/bash


# cleaning the existings files
mkdir -p ./output/client
rm ./output/client/*.key
rm ./output/client/*.csr
rm ./output/client/*.srl
rm ./output/client/*.crt
rm ./output/client/*.p12





# Get the current username using whoami
username=$(whoami)

# create a client key and csr
openssl req \
   -newkey rsa:2048 \
   -nodes \
   -days 365 \
   -subj "/CN=${username}/O=Thoughtworks" \
   -keyout ./output/client/client.key \
   -out ./output/client/client.csr

# create a client certificate
openssl x509 \
   -req \
   -in ./output/client/client.csr \
   -out ./output/client/client.crt \
   -CA ./output/client-ca/client-ca.crt \
   -CAkey ./output/client-ca/client-ca.key \
   -CAcreateserial \
   -days 365 \
   -extfile ./configs/client-ext.cnf

openssl pkcs12 \
  -export \
  -out ./output/client/client.p12 \
  -inkey ./output/client/client.key \
  -in ./output/client/client.crt


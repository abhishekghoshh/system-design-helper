# create server certificate with extension file

# cleaning the existings files
mkdir -p ./output/server
rm ./output/server/*.key
rm ./output/server/*.csr
rm ./output/server/*.srl
rm ./output/server/*.crt
rm ./output/server/*.p12



# Generate web server's private key and certificate signing request (CSR)
openssl req \
    -newkey rsa:4096 \
    -nodes \
    -keyout ./output/server/server.key \
    -out ./output/server/server.csr \
    -subj "/C=IN/ST=Maharastra/L=Pune/O=Thoughtworks/OU=Research/CN=*.e4r.internal"

# Use CA's private key to sign web server's CSR and get back the signed certificate
openssl x509 \
    -req \
    -in ./output/server/server.csr \
    -days 60 \
    -CA ./output/ca/ca.crt \
    -CAkey ./output/ca/ca.key \
    -CAcreateserial \
    -out ./output/server/server.crt \
    -extfile ./configs/server-ext.cnf


echo "Server's signed certificate"
openssl x509 \
  -in ./output/server/server.crt \
  -noout -text

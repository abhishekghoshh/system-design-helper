# intermediate client ca and client ca


# cleaning the existings files
mkdir -p ./output/client-ca
rm ./output/client-ca/*.key
rm ./output/client-ca/*.csr
rm ./output/client-ca/*.srl
rm ./output/client-ca/*.crt
rm ./output/client-ca/*.p12




openssl req \
   -newkey rsa:2048 \
   -nodes \
   -days 3650 \
   -keyout ./output/client-ca/client-ca.key \
   -out ./output/client-ca/client-ca.csr \
   -subj "/C=IN/ST=Maharastra/L=Pune/O=Thoughtworks/OU=Research/CN=*.iam.io"

# intermediate client certificate
openssl x509 \
   -req \
   -in ./output/client-ca/client-ca.csr \
   -out ./output/client-ca/client-ca.crt \
   -CA ./output/ca/ca.crt \
   -CAkey ./output/ca/ca.key \
   -CAcreateserial \
   -days 3650 \
   -extfile ./configs/client-ca-ext.cnf

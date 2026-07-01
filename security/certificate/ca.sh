# create self-sgned ca cert file
# -nodes for without encryption

# cleaning the existings files
mkdir -p ./output/ca
rm ./output/ca/*.key
rm ./output/ca/*.csr
rm ./output/ca/*.srl
rm ./output/ca/*.crt
rm ./output/ca/*.p12

openssl req \
    -newkey rsa:2048 \
    -nodes \
    -x509 \
    -days 3650 \
    -keyout ./output/ca/ca.key \
    -out ./output/ca/ca.crt \
    -subj "/C=IN/ST=Maharastra/L=Pune/O=Thoughtworks/OU=Research/CN=*.iam.io"


echo "CA's self-signed certificate"

openssl x509 \
  -in ./output/ca/ca.crt \
  -noout -text

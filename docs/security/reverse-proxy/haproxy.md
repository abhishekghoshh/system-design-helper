# HAProxy basics



## config file

**Create a cfg file and add the following contents**

Sample config
```
frontend https-in
    bind *:80
    bind *:443  ssl crt server-cert.crt verify required ca-file intermediate-client-ca.crt ca-verify-file client-root-ca.crt
    http-request redirect scheme https unless { ssl_fc }
    default_backend apiservers
```

Advanced config with certificates
```
defaults
   mode http
   timeout connect 5000
   timeout client 50000
   timeout server 50000

frontend echo-fontend
   bind *:443 ssl crt server-cert.pem verify required ca-file intermediate.crt alpn h2,http/1.1
   mode http
   default_backend echo-backend
   option forwardfor
   option http-server-close
   http-request set-header X-Client-Certificate %[ssl_c_der,base64]
   http-request set-header X-SSL-Client-Cert          %{+Q}[ssl_c_der,base64]
   http-request set-header X-SSL-Client-CN            %{+Q}[ssl_c_s_dn(cn)]
   http-request set-header X-SSL-Client-Verify        %[ssl_c_verify]

backend echo-backend
   mode http
   server echo 127.0.0.1:8000
```





### Sample blogs and configs
- [test.cfg](https://github.com/hnasr/javascript_playground/blob/master/proxy/test.cfg)
- [Restrict API Access With Client Certificates (mTLS)](https://www.haproxy.com/blog/restrict-api-access-with-client-certificates-mtls)
- [Client Certificate Authentication with HAProxy](https://www.loadbalancer.org/blog/client-certificate-authentication-with-haproxy/)

### Youtube videos
- [HAProxy Basics](https://www.youtube.com/playlist?list=PLfnwKJbklIxwxXKiPv5nAgWwmaUvDjW_t)
- [HAProxy](https://www.youtube.com/playlist?list=PLQnljOFTspQUhgfvpgfxc-uFlWElKIBr-)



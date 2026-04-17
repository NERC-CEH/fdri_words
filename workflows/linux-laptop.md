# Developers Guide to working on a linux laptop

There's a few extra steps needed if working on a linux laptop.


## Contents
- Connecting to eduroam
- Intune
- Working without the VPN

## Connecting to Eduroam

1. Install eduroam cat from here https://cat.eduroam.org/
2. Select UK Centre for Ecology and Hydrology (not lancaster university)
3. Login with your UKCEH username/password

## Intune
- Intune is required to access teams/outlook/etc
- There is a guide here: https://cehacuk.sharepoint.com/sites/Hub-ITFAQ/SitePages/How-do-I-get-access-to-corporate-resources-from-Linux-(BYOD).aspx

When I run intune, I get this error pop up
<img width="706" height="574" alt="image" src="https://github.com/user-attachments/assets/7b5866ae-5345-4fe6-97c2-8463981c8cec" />


Everything still works though, so can be ignored.


## Working without the VPN

To access deployed services on aws without connecting to the company network, we have the following work around.

### 1. Add the following to /etc/hosts
```
127.0.0.1 dri-ui.staging.eds.ceh.ac.uk dri-api.staging.eds.ceh.ac.uk dri-metadata-api.staging.eds.ceh.ac.uk dri-data-api.staging.eds.ceh.ac.uk
127.0.0.1 dri-ui.staging.dri.ceh.ac.uk dri-data-api.staging.dri.ceh.ac.uk dri-metadata-api.staging.dri.ceh.ac.uk
127.0.0.1 dri-ui.dri.ceh.ac.uk dri-data-api.dri.ceh.ac.uk dri-metadata-api.dri.ceh.ac.uk
```
### 2. Setup Caddy
#### 1. follow the install instructions here https://caddyserver.com/docs/install#debian-ubuntu-raspbian
#### 2. Install caddy ca cert
```bash
sudo cp /var/lib/caddy/.local/share/caddy/pki/authorities/local/root.crt /usr/local/share/ca-certificates/caddy-local.crt
sudo update-ca-certificates
```
#### 3. Update Caddyfile
```yaml
$ cat /etc/caddy/Caddyfile
# The Caddyfile is an easy way to configure your Caddy web server.
:80 {
        root * /usr/share/caddy
        file_server
}

(cors) {
    @cors_preflight method OPTIONS
    handle @cors_preflight {
        header Access-Control-Allow-Origin "*"
        header Access-Control-Allow-Methods "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        header Access-Control-Allow-Headers "Authorization, Content-Type"
        header Access-Control-Max-Age "3600"
        respond "" 204
    }
    header Access-Control-Allow-Origin "*"
}

dri-metadata-api.staging.eds.ceh.ac.uk {
    import cors
    reverse_proxy localhost:9990
    tls internal
}

dri-api.staging.eds.ceh.ac.uk {
    import cors
    reverse_proxy localhost:9992 {
        header_down -Access-Control-Allow-Origin
    }
    tls internal
}

dri-ui.staging.eds.ceh.ac.uk {
    reverse_proxy localhost:9993
    tls internal
}

dri-metadata-api.staging.dri.ceh.ac.uk {
    import cors
    reverse_proxy localhost:9990
    tls internal
}

dri-data-api.staging.dri.ceh.ac.uk {
    import cors
    reverse_proxy localhost:9992 {
        header_down -Access-Control-Allow-Origin
    }
    tls internal
}

dri-ui.staging.dri.ceh.ac.uk {
    reverse_proxy localhost:9993
    tls internal
}

dri-metadata-api.dri.ceh.ac.uk {
    import cors
    reverse_proxy localhost:9990
    tls internal
}

dri-data-api.dri.ceh.ac.uk {
    import cors
    reverse_proxy localhost:9992 {
        header_down -Access-Control-Allow-Origin
    }
    tls internal
}

dri-ui.dri.ceh.ac.uk {
    reverse_proxy localhost:9993
    tls internal
}
```

```bash
sudo systemctl restart caddy
sudo systemctl status caddy # to verify it is running correctly
```
### 3. Run port-forward script

```bash
#!/bin/bash

kubectl --namespace metadata-service port-forward svc/ms-api 9990:8080 \
& kubectl port-forward -n timeseries deployment/dri-data-api 9992:8000 \
& kubectl port-forward -n timeseries deployment/dri-ui 9993:3000
```

Save the above as a script, `chmod +x port-forward.sh`, then run to port forward 3 services as once.

##### Steps:
1. aws-vault exec dri-staging
2. kubectl use-context dri-staging
3. ./port-forward.sh

### 4. Add cert to browser

Navigate to dri-ui.staging.dri.ceh.ac.uk in a web browser, if your browser is using the OS certs this should just work. If there is a warning about the cert, download it as pem and add to the authorities section in your browser, for firefox this is in settings > Privacy & Security > Security > certificates > Manage certificates > Authorities > Import... .
### 5. dri-ui.staging.dri.ceh.ac.uk etc should work

The ui, api and metadata api should all work from the browser now.

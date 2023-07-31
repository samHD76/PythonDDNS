# PythonDDNS
### python based ddns service that syncs your current public IP to CloudFlare



you need to pass following environments for it to work as intended :
 #### - email: your cloudFlare Email Address 
  #### - domain: your full domain name to add/update with this script example: test.domain.com
  #### - zoneID: every domain in CloudFlare has a zoneID of it's own . adding zoneID of root domain (ex: domain.com) will do the job.
####  - globalAPI: globalAPI key of your CloudFlare Account . you can find it in "My Profile" -> "API Tokens" -> "Global API TOKEN"
####  -  wait: this is the time script waits( in seconds) before checking your public IP Again



and here is a sample docker-compose file  that updates the IP section of test.domain.com every 5 minutes:
```
version: '3'
services:
  DDNS:
    image: samhdabd/ddns:0.1
    environment:
      email: "test@gmail.com"
      domain: "Test.domain.com"
      zoneID: "YOUR ZONEID"
      globalAPI: "YOUR API KEY"
      wait: "300"  
    networks:
      my_network:
        ipv4_address: 10.10.1.10 
    command: ["python3", "./ddns.py"]
    dns:
      - 1.1.1.1

networks:
  my_network:
    ipam:
      driver: default
      config:
        - subnet: 10.10.1.0/24
          gateway: 10.10.1.1    
```

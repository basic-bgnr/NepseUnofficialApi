# NepseUnofficialApi
Unofficial library to interface with nepalstock.com.np
Deciphers the authentication key to access the api.

# How to Use
1. Make sure your python version >= 3.8.0
1. Download this git repo into your local computer. 
1. Change the directory to NepseUnofficialApi 
1. Install the dependencies 
1. Run the module. (running the module returns the current market status) 
```
git clone https://github.com/basic-bgnr/NepseUnofficialApi.git 
cd NepseUnofficialApi
pip3 install -r Requirements.txt
python3 -m nepse 
```
The example folder contains `/example/NepseServer.py` an implementation of
this library. The following runs a local flask server on `localhost:8000`.  
```
cd example
python3 NepseServer.py
``` 


# Development
1. [Oct 20, 2023] moved api_endpoints, headers, and dummy_data to loadable json file 
1. [Oct 10, 2023] Module(files, folders) restructuring
1. [Sep 24, 2023] [Fixed SSL CERTIFICATE_VERIFY_FAILED](#Fixed:-SSL-Error).
1. [Sep 24, 2023] Branch `15_feb_2023` is now merged with the master branch. 
1. [Feb 15, 2023] ~~checkout new branch 15_feb_2023 to adjust for new change in Nepse.~~


# Fix Details 
## Fixed: SSL Error
Recently there was a [PR](https://github.com/basic-bgnr/NepseUnofficialApi/pull/3) in this repo by [@Prabesh01](https://github.com/Prabesh01) to merge few changes to fix SSL issue that he was facing.  

```
requests.exceptions.SSLError: 
HTTPSConnectionPool(host='www.nepalstock.com.np', port=443): 
Max retries exceeded with url: /api/authenticate/prove 
(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] 
certificate verify failed: unable to get local issuer certificate (_ssl.c:1002)')))
``` 
The day when I actually received that PR, I too was facing similar issue with Nepse's website, so I thought the issue was serverside and left it as it is. 

Fast-forward today, upon diving a little deeper, It appears that the issue can be solved entirely from clientside. But it has nothing to do with code in this repository, it was because my linux distribution(and maybe others too, I haven't checked) doesn't have ca-certificate of Certificate Authority [GeoTrust](http://cacerts.geotrust.com/) that signs the ssl certificate of Nepse. The mistake is primarily due to Nepse as it means that the certificate chain used by Nepse is incomplete.

> ### Solution:

1. Find out the ssl [certificate details of Nepse](https://www.ssllabs.com/ssltest/analyze.html?d=nepalstock.com.np) using [ssllabs.com](https://www.ssllabs.com).
1. Copy the .pem file from the ssllabs and save it into your `/usr/local/share/ca-certificates/` folder using the following command[^1].  
```
sudo curl -A "Mozilla Chrome Safari" "https://www.ssllabs.com/ssltest/getTestCertificate?d=nepalstock.com.np&cid=3a83c9a7e960f29b48e5719510e2e8582c37f72f3abf35e6f400eaacec38aad2&time=1695547628855" >> geotrust.pem
sudo curl -A "Mozilla Chrome Safari" "https://www.ssllabs.com/ssltest/getTestChain?d=nepalstock.com.np&cid=3a83c9a7e960f29b48e5719510e2e8582c37f72f3abf35e6f400eaacec38aad2&time=1695547628855" >> geotrust_alt.pem 
```
3. and, finally you've to run the following command[^1] to include the added CA details into the system.  
``` sudo update-ca-certificates```
[^1]: The command uses root access so first verify before carrying out the operation.

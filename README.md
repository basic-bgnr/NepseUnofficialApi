[![Status](https://github.com/basic-bgnr/NepseUnofficialApi/actions/workflows/actions.yml/badge.svg)](https://github.com/basic-bgnr/NepseUnofficialApi/actions/workflows/actions.yml)  
# NepseUnofficialApi
Unofficial library to interface with nepalstock.com
Deciphers the authentication key to access the api.

# How to Install?
### A. Using Git + pip
1. Make sure your python version >= 3.8.0
1. Download this git repo into your local computer. 
1. Change the directory to NepseUnofficialApi 
1. Install the package
```
git clone https://github.com/basic-bgnr/NepseUnofficialApi.git 
cd NepseUnofficialApi
pip3 install .
```
### B. Using pip only(install directly from git)
```
pip install git+https://github.com/basic-bgnr/NepseUnofficialApi
```
# How to use?
### A. API usage
```
from nepse import Nepse
nepse = Nepse()
nepse.setTLSVerification(False) #This is temporary, until nepse sorts its ssl certificate problem
nepse.getCompanyList()
```
### B. Cli tool
After installing the package, `nepse-cli` cmdline tool is available
```
dev└─ $ nepse-cli --help
usage: nepse-cli [-h] [--start-server] [--show-status]

cmdline iterface to nepalstock.com

options:
  -h, --help      show this help message and exit
  --start-server  starts local server at 0.0.0.0:8000
  --show-status   dumps Nepse status in the standard output
```
### C. Example
The example folder contains `/example/NepseServer.py` an implementation of
this library. The following runs a local flask server on `localhost:8000`.  
```
cd example
python3 NepseServer.py
``` 

# Uninstallation
Running the following command will remove the package from the system.
```
pip uninstall nepse
```

# Development
1. [Apr 09, 2024]
   * APIs now make use of HTTP2 request to nepse's server
   * Added tool `nepse-cli` which can be directly used from the terminal after installing the package
2. [Apr 08, 2024]
   * APIs can now be called without rate limitation or raising Exception (no need to add delay between API calls),
   * Speed Improvement ( getFloorSheet() and getFloorSheetOf() calls are ~3 times faster)
3. [Apr 07, 2024] getFloorSheet and getFloorSheetOf now works without raising exception
4. [Apr 05, 2024] Speed Improvement (remove dependency from requests to httpx, http calls are now faster)
5. [Mar 23, 2024] add setup.py to ease installation process.
6. [Oct 20, 2023] moved api_endpoints, headers, and dummy_data to loadable json file
7. [Oct 10, 2023] Module(files, folders) restructuring
8. [Sep 24, 2023] [Fixed SSL CERTIFICATE_VERIFY_FAILED](#Fixed:-SSL-Error).
9.  [Sep 24, 2023] Branch `15_feb_2023` is now merged with the master branch.
10. [Feb 15, 2023] ~~checkout new branch 15_feb_2023 to adjust for new change in Nepse.~~


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

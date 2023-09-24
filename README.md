# NepseUnofficialApi
Unofficial library to interface with nepalstock.com.np
Deciphers the authentication key to access the api


# Development
1. [Sep 24, 2023] [Fixed SSL CERTIFICATE_VERIFY_FAILED](#Fixed:-SSL-Error).
1. [Sep 24, 2023] Branch `15_feb_2023` is now merged with the master branch. 
1. [Feb 15, 2023] ~~checkout new branch 15_feb_2023 to adjust for new change in Nepse.~~


# Fix Details 
## Fixed: SSL Error
Recently there was a [PR](https://github.com/basic-bgnr/NepseUnofficialApi/pull/3) in this repo by [@Prabesh01](https://github.com/Prabesh01) to merge changes to fix SSL issue that he was facing.  

```
requests.exceptions.SSLError: 
HTTPSConnectionPool(host='www.nepalstock.com.np', port=443): 
Max retries exceeded with url: /api/authenticate/prove 
(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] 
certificate verify failed: unable to get local issuer certificate (_ssl.c:1002)')))
``` 
The day when I actually received that PR, I too was facing similar issue with nepse's website, so I thought the issue was serverside and left it as it is. 

Fast-forward today, upon diving a little deeper, It appears that the issue is entire clientside. But has nothing to do with code in this repository, it was because my linux distribution(and maybe others too, I haven't checked) doesn't have ca-certificate of Certificate Authority [GeoTrust](http://cacerts.geotrust.com/) that signs the ssl certificate of nepse. 

```

Distributor ID: LinuxMint
Description:    Linux Mint 19 Tara
Release:        19
Codename:       tara

```
> ### Solution:

1. Find out the ssl [certificate details of Nepse](https://www.ssllabs.com/ssltest/analyze.html?d=nepalstock.com.np) using [ssllabs.com](https://www.ssllabs.com).
1. Copy the .pem file from the ssllabs and save it into your `/usr/local/share/ca-certificates/` folder.  
```
curl https://www.ssllabs.com/ssltest/getTestCertificate?d=nepalstock.com.np&cid=3a83c9a7e960f29b48e5719510e2e8582c37f72f3abf35e6f400eaacec38aad2&time=1695547628855 >> geotrust.pem
curl https://www.ssllabs.com/ssltest/getTestChain?d=nepalstock.com.np&cid=3a83c9a7e960f29b48e5719510e2e8582c37f72f3abf35e6f400eaacec38aad2&time=1695547628855 >> geotrust_alt.pem 
```
3. and, finally you've to run the following command to include the added CA details into the system.  
  

``` sudo update-ca-certificates```  
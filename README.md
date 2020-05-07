# waseda-mochida

Official Homepages for Waseda Mochida  

Technology stacks  

- Python + Flask
- Heroku and its addons
- LINE Online API v3 and its Python SDK

***

## Runtimes

All the Python programs in this sub-directory are expected to run correctly under the environments below:  

| Components | Version |
| --- | --- |
| OS | 10.15.4 (Catalina) |
| Python | 3.6.4 |
| pyenv | 1.2.18 |
| Flask | 1.1.2 |

Run the `pip install -r requirements.txt` to install dependent packages.  
If you use `virtualenv`, create your private environment first with `python -m venv venv`, then install dependencies with pip.  

***

## Environment

This app is deployed on Heroku PaaS environments with `Procfile` in this repository.  
Dependent packages are described in `requirements.txt` and auto-deployment will be run with GitHub and Heroku integrations.  

cf. Heroku CLI configurations  

```bash
$ heroku --version
heroku/7.39.5 darwin-x64 node-v12.16.2
```

This app uses some features of Heroku.  

- App connection with GitHub/Heroku
- Automatic Deploy with `master` branch
- Python buildpack, configured automatically with initial deployment on Heroku
- SSL Certification (ACM: Automated Certification Manager)
- Custom domain configuration: `www.waseda-mochida.com` with PointDNS

Some environmental variables should be retrived by `heroku config`.  
Before runing apps on local environment, it's required to run `heroku config:set VAR_NAME:VAR_VALUE --app waseda-mochida`.  

| Name | Description | Syntax | Example value |
| --- | --- | --- | --- |
| LINE_PAY_CHANNEL_ID | TokenID for LINE OnlineAPI to execute payment requests | 10 digts numbers | 1234567890 |
| LINE_PAY_CHANNEL_SECRET | Token Password for confirm accounts with LINE OnlineAPI | 32 digits password | abcdefghijklmnopqrstuvwxyz123456 |
| EMAIL_BCC_ADDRESS | Bcc email address when app user would post from contact form | valid email address | youremailaddress@example.com |
| EMAIL_GOOGLE_PASSWORD | Google application password for sending email via contact form | 16 digits password | abcdefghijkl |

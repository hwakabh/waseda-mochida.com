# waseda-mochida
Official Homepages for Waseda Mochida

Technology stacks
- Python + Flask
- [Heroku](https://www.heroku.com) and its addons
  - Heroku Pipeline (for stage/prod Environment)
  - Review Apps (for deployments of PR Environment)
  - Heroku CI (for testing)
  - ACM
  - Heroku Postgres
  - Heroku Key-Value Store
- [LINE Online API v3](https://pay.line.me/jp/developers/apis/onlineApis?locale=ja_JP) with several Python packages
- [Mend Renovate](https://www.mend.io/renovate/) (for dependencies updates)


## Build
For application deployments in Heroku environment, [`heroku-python-buildpack`](https://github.com/heroku/heroku-buildpack-python) will be used, and all the depenedencies file should be configured in `requirements.txt` by its design. \
Please also check [its official documentations](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python) of `heroku-python-buildpack` for further information.


## Deployment
This app is deployed on Heroku PaaS environments with [GitHub Integrations](https://devcenter.heroku.com/articles/github-integration) features of Heroku. \
Thanks to this features, the application deployment will be automatically updated when we merged any commits to `main` branch.

This app uses some additional features releated to application deployment
- SSL Certification (ACM: Automated Certification Manager)
  - Docs: <https://devcenter.heroku.com/articles/automated-certificate-management>
- Custom domain configuration: `www.waseda-mochida.com` by Squarespace Domain
  - Docs: <https://www.squarespace.com>
  - Formerly known as [Google Domain](http://domains.google)

Some environmental variables should be retrived by `heroku config`.
Before runing apps as Heroku Dynos, we need to configure environmental variables with running `heroku config:set VAR_NAME:VAR_VALUE --app waseda-mochida`, or from UI.

| Name | Description | Syntax | Example value |
| --- | --- | --- | --- |
| PIPELINE | String values for determine apps in Heroku pipeline | `production` or `stage` or `local` | `local` |
| LINE_PAY_CHANNEL_ID | TokenID for LINE OnlineAPI to execute payment requests | 10 digts numbers | `1234567890` |
| LINE_PAY_CHANNEL_SECRET | Token Password for confirm accounts with LINE OnlineAPI | 32 digits password | `abcdefghijklmnopqrstuvwxyz123456` |
| EMAIL_BCC_ADDRESS | (Optional) Bcc email address when app user would post from contact form | valid email address | `youremailaddress@example.com` |
| EMAIL_GOOGLE_PASSWORD | (Optional) Google application password for sending email via contact form | 16 digits password | `abcdefghijkl` |


## Local development
Run the `pip install -r requirements.txt` to install dependent packages for running application. \
If you use `virtualenv`, we recommend to create your private environment first with `python -m venv venv`, then install dependencies with pip.

Since this app requires to run with Python3 and Flask, you need to install Python3 to your environmet first.
Also you can use `pyenv`, you might know if you're good at Python.

Here is the instructions to install this app to your local with `pyenv`.

```bash
# Create your private environment for this app, and activate them
$ python -m venv YOUR_ENV_NAME
$ source venv/bin/activate

# Install dependencies for this app
$ pip install -r requirement.txt
```

## Run apps

```shell
# Database setup
$ docker run -d --name postgres -p 5432:5432 -e POSTGRESQL_PASSWORD=postgres  bitnami/postgresql:latest

$ docker exec -u root -it postgres psql -U postgres -c 'CREATE DATABASE mochida;'
$ export DATABASE_URL='postgres://postgres:postgres@0.0.0.0:5432/mochida'

# Cache setup
$ docker run -d --name redis -p 6379:6379 -e ALLOW_EMPTY_PASSWORD=yes bitnami/redis:latest
$ export REDIS_URL='redis://0.0.0.0:6379'
```


```shell
# for development purpose
$ FLASK_APP=apps.index:app flask run
```

```shell
# same as production commands
$ gunicorn apps.index:app --log-file -
```

Then you can access via `http://127.0.0.1:5000/` with your browser.

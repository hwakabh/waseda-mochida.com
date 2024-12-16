# waseda-mochida

Official Homepages for Waseda Mochida

Technology stacks
- Python + Flask
- Heroku and its addons
- LINE Online API v3 and its Python SDK
- Slack integrations with Heroku and Heroku
- Mend Renovate (for dependencies updates)

## Runtimes
All the Python programs in this sub-directory are expected to run correctly under the environments below:

| Components | Version |
| --- | --- |
| OS | macOS 15.1.1 (Sequoia) |
| pyenv | 2.4.19 (installed via brew) |

Run the `pip install -r requirements.txt` to install dependent packages for running application. \
If you use `virtualenv`, we recommend to create your private environment first with `python -m venv venv`, then install dependencies with pip.


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
If you'd like to edit this app, for example to modify/add some features, of course you can install this app to your local development environment.
Since this app requires to run with Python3 and Flask, described in `Runtimes` of this page, you need to install Python3 to your environmet first.
Also you can use `pyenv`, you might know if you're good at Python.

Here is the instructions to install this app to your local with `pyenv`.

```bash
# Create your private environment for this app, and activate them
$ python -m venv YOUR_ENV_NAME
$ source venv/bin/activate

# Install dependencies for this app
$ pip install -r requirement.txt
```

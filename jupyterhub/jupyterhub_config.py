import os

c.JupyterHub.port = 8000
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.proxy_api_ip = '0.0.0.0'

c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.password = 'admin'
c.Authenticator.admin_users = {'admin'}

c.JupyterHub.spawner_class = 'simple' 

c.JupyterHub.db_url = os.environ.get('JUPYTERHUB_DB_URL', 'sqlite:///jupyterhub.sqlite')

c.ConfigurableHTTPProxy.auth_token = os.environ.get('CONFIGPROXY_AUTH_TOKEN', '')
c.JupyterHub.proxy_auth_token = os.environ.get('CONFIGPROXY_AUTH_TOKEN', '')

c.JupyterHub.cookie_secret = os.environ.get('JUPYTERHUB_COOKIE_SECRET', '').encode('utf-8')
c.JupyterHub.crypt_key = os.environ.get('JUPYTERHUB_CRYPT_KEY', '').encode('utf-8')

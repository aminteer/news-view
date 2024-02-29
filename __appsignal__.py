from appsignal import Appsignal
import subprocess
 
revision = None
 
try:
    revision = subprocess.check_output(
        "git log --pretty=format:'%h' -n 1", shell=True
    ).strip()
except subprocess.CalledProcessError:
  pass

appsignal = Appsignal(
    active=True,
    name="ucb-softarch-final",
    # Please do not commit this key to your source control management system.
    # Move this to your app's security credentials or environment variables.
    # https://docs.appsignal.com/python/configuration/options.html#option-push_api_key
    push_api_key="e2052fe2-9957-49f6-a2a7-857485f6858c",
    revision=revision
)

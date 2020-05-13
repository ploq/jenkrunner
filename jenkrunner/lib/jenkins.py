import datetime
import requests
import sys
import time
from requests import session as rsession, auth as rauth


class JenkinsBuild(object):
    def __init__(self, build_info, auth):
        self.build_info = build_info
        self.auth = auth
        self.build_url = self.build_info.get("url")
        self.build_api_url = self.build_url + "api/json"
        self.session = rsession()

    def get_console_output(self):
        console_url = self.build_url + "/consoleText"
        r = self.session.get(console_url, auth=self.auth)
        return r.text

    def show_progressive_console_output(self, show_time=False):
        def _handle_line(line):
            if line:
                if show_time is True:
                    line = "%s %s\r\n" % (datetime.datetime.now().strftime("%H:%M:%S"), line)
                else:
                    line = "%s\r\n" % line
            return line

        log_text_url = self.build_url + "/logText/progressiveText?start="
        more_data = True
        prev_text_size = 0
        while more_data is True:
            r = self.session.get(log_text_url + str(prev_text_size), auth=self.auth)
            text_size = int(r.headers.get("X-Text-Size"))
            if text_size != prev_text_size:
                for line in r.text.split("\r\n"):
                    sys.stdout.write(_handle_line(line))
                prev_text_size = text_size
            more_data = r.headers.get("X-More-Data", False) == "true"
            time.sleep(0.5)


class JenkinsRunner(object):
    def __init__(self, jenkins_url, username, password):
        self.jenkins_url = jenkins_url
        self.jenkins_job_url = self.jenkins_url + "/job"
        self.username = username
        self.password = password
        self.auth = rauth.HTTPBasicAuth(self.username, self.password)
        self.session = rsession()

    def _create_build_info(self, build_info):
        return JenkinsBuild(build_info, self.auth)

    def _create_jenk_job_url(self, job_name, job_type, token):
        base_url = "{url}/{job_name}".format(url=self.jenkins_job_url, job_name=job_name)
        if job_type == "normal":
            url = "{base}/build?token={token}".format(base=base_url,
                                                      job_name=job_name, token=token)
            return url
        elif job_type == "parameters":
            url = "{base}/buildWithParameters?token={token}".format(base=base_url,
                                                                    job_name=job_name, token=token)
            return url

    def _get_jenkins_build(self, queue_url):
        if queue_url is None:
            return None
        queue_url = queue_url + "/api/json"

        while True:
            resp_json = self.session.get(queue_url, auth=self.auth).json()
            if resp_json.get("why") is None:
                return self._create_build_info(resp_json.get("executable"))
            time.sleep(1)

    def start_job(self, job, token):
        url = self._create_jenk_job_url(job, "normal", token)
        r = self.session.get(url, auth=self.auth)
        r.raise_for_status()
        return self._get_jenkins_build(r.headers.get("Location"))

    def start_parameterized_job(self, job, token, parameters=None, files=None):
        url = self._create_jenk_job_url(job, "parameters", token)
        r = self.session.post(url, data=parameters, files=files, auth=self.auth)
        r.raise_for_status()
        return self._get_jenkins_build(r.headers.get("Location"))

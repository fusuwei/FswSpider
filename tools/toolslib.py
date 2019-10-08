import hashlib
import traceback
import sys
import threading

# url去重MD5
def get_md5(url):
    if isinstance(url, list) or isinstance(url, tuple):
        url = ''.join([str(u) if u else '' for u in url])
    m = hashlib.md5()
    if isinstance(url, str):
        url = url.encode('utf-8')
    m.update(url)
    return m.hexdigest()


class ExceptErrorThread(threading.Thread):
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName
        self.exitcode = 0
        self.exception = None
        self.exc_traceback = ''

    def run(self):  # Overwrite run() method, put what you want the thread do here
        try:
            self._run()
        except Exception as e:
            self.exitcode = 1  # 如果线程异常退出，将该标志位设置为1，正常退出为0
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))  # 在改成员变量中记录异常信息

    def _run(self):
        try:
            self.funcName(*(self.args))
        except Exception as e:
            raise e
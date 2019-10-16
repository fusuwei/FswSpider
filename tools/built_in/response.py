import chardet


class Response:
    def __init__(self, url, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, error=None, request=None):
        self.url = url
        self.content = content
        self.status_code = status_code
        self.charset = charset
        self.cookies = cookies
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.error = error
        self.request = request
        self.text = self._parse_content(charset, content)

    def _parse_content(self, charset, content):
        if not content:
            return
        if charset:
            try:
                text = content.decode(charset)
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(content)
                    if char:
                        text = content.decode(char)
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = content.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            text = content.decode("GBK")
                        except UnicodeDecodeError:
                            text = content.decode('utf-8', "ignore")
        else:
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(content)
                    if char:
                        text = content.decode(char)
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = content.decode('gb2312')
                    except UnicodeDecodeError:
                        text = content.decode('utf-8', "ignore")
        return text


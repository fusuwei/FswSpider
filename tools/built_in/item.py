

class Item:
    def __init__(self, table_name=None, method="insql", request=None, **kwargs):
        self._kwargs = kwargs
        self.table_name = table_name
        self.method = method
        self.request = request
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def to_dict(self,):
        dic = {}
        for key in self.__dict__.keys():
            if self.__dict__[key]:
                if key not in ["table_name", "method", "request", "_kwargs"]:
                    dic[key] = self.__dict__[key]
        return dic


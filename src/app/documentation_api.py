import inspect


class DocumentationApi:
    def __init__(self):
        self.docs = {}

    def _format_documentation(self, prev_docs, docs):
        prev_docs += "\n"

    def _load_documentation(self, doc_name, doc):
        self.docs[doc_name] = doc

    def _generate_documentation(self, api_list):
        for api in api_list:
            class_name = api.__class__.__name__
            class_name = class_name[:-3]
            docs = []
            for method in api.__class__.__dict__:
                doc = ''
                method = getattr(api.__class__, method)
                if callable(method) and method.__name__[:1] != '_':
                    method_name = method.__name__.replace('_', '-')
                    doc = f'{method_name}: '
                    sig = list(
                            inspect.signature(method).parameters.values())[1:]
                    if not sig:
                        doc = doc[:-1]
                    for parameter in sig:
                        parameter = str(parameter)
                        if '=' not in parameter:
                            doc += parameter+' '
                        else:
                            doc += '--'+parameter.split('=')[0]+' '
                    docs.append(doc[:-1])
            self.docs[class_name] = docs

    def _function_documentation(self, func_name, doc_name=None):
        if doc_name is not None:
            return self.docs.get(doc_name, {}).get(
                    func_name, "Command doesn\'t exist")
        for doc in list(self.docs.keys()):
            if func_name in self.docs[doc]:
                return self.docs[doc]
        return "Command doesn\'t exist"

    def help(self):
        doc = ''
        for class_name, methods in self.docs.items():
            doc += f'\n{class_name}'
            for method in methods:
                doc += f'\n\t{method}'
        return doc

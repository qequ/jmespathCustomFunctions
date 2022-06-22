import jmespath
from jmespath import functions


class RemoveFunctions(functions.Functions):

    @functions.signature({'types': ['object'], "variadic": True}, {'types': ['boolean']})
    def _func_remove_null(self, obj, recursive):
        if recursive:
            return self._func_remove_recursive(obj, None)
        else:
            return self._func_remove(obj, None)

    @functions.signature({'types': ['object'], "variadic": True}, {'types': ['boolean']})
    def _func_remove_empty(self, obj, recursive):
        if recursive:
            return self._func_remove_recursive(obj, None, '')
        else:
            return self._func_remove(obj, None, '')

    def _func_remove(self, obj, *args):
        return {k: v for k, v in obj.items() if not v in list(args)}

    def _func_remove_recursive(self, obj, *args):
        ret_dict = {}
        for k in obj:
            if not obj[k] in list(args):
                ret_dict[k] = obj[k]

            if isinstance(obj[k], dict):
                ret_dict[k] = self._func_remove_recursive(obj[k], *args)

        return ret_dict


options = jmespath.Options(custom_functions=RemoveFunctions())

# print: {'a': 'a', 'd': {'b': 'b'}}
print(
    jmespath.search(
        '{a: `a`, c: null, d: {a: null, b: `b`}} | remove_empty(@, `true`)', {}, options=options)
)


# print {'a': 'a', 'd': {'b': 'b'}}
print(
    jmespath.search(
        '{a: `a`, c: null, d: {a: null, b: `b`, c:``}} | remove_empty(@, `true`)', {}, options=options)
)

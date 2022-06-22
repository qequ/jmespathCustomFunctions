jmespathCustomFunctions
========


Custom Functions
~~~~~~~~~~~~~~~~

(Reference: `jmespath.py repo <https://github.com/jmespath/jmespath.py>`__)
The JMESPath language has numerous
`built-in functions
<http://jmespath.org/specification.html#built-in-functions>`__, but it is
also possible to add your own custom functions.  Keep in mind that
custom function support in jmespath.py is experimental and the API may
change based on feedback.

**If you have a custom function that you've found useful, consider submitting
it to jmespath.site and propose that it be added to the JMESPath language.**
You can submit proposals
`here <https://github.com/jmespath/jmespath.site/issues>`__.

To create custom functions:

* Create a subclass of ``jmespath.functions.Functions``.
* Create a method with the name ``_func_<your function name>``.
* Apply the ``jmespath.functions.signature`` decorator that indicates
  the expected types of the function arguments.
* Provide an instance of your subclass in a ``jmespath.Options`` object.

Below are a few examples:

.. code:: python

    import jmespath
    from jmespath import functions

    # 1. Create a subclass of functions.Functions.
    #    The function.Functions base class has logic
    #    that introspects all of its methods and automatically
    #    registers your custom functions in its function table.
    class CustomFunctions(functions.Functions):

        # 2 and 3.  Create a function that starts with _func_
        # and decorate it with @signature which indicates its
        # expected types.
        # In this example, we're creating a jmespath function
        # called "unique_letters" that accepts a single argument
        # with an expected type "string".
        @functions.signature({'types': ['string']})
        def _func_unique_letters(self, s):
            # Given a string s, return a sorted
            # string of unique letters: 'ccbbadd' ->  'abcd'
            return ''.join(sorted(set(s)))

        # Here's another example.  This is creating
        # a jmespath function called "my_add" that expects
        # two arguments, both of which should be of type number.
        @functions.signature({'types': ['number']}, {'types': ['number']})
        def _func_my_add(self, x, y):
            return x + y

    # 4. Provide an instance of your subclass in a Options object.
    options = jmespath.Options(custom_functions=CustomFunctions())

    # Provide this value to jmespath.search:
    # This will print 3
    print(
        jmespath.search(
            'my_add(`1`, `2`)', {}, options=options)
    )

    # This will print "abcd"
    print(
        jmespath.search(
            'foo.bar | unique_letters(@)',
            {'foo': {'bar': 'ccbbadd'}},
            options=options)
    )




Another example


.. code:: python

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

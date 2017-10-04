#!/usr/bin/env python3.6


class FinalGlobal:
    def __init__(self):
        # per-object value so that we don't have to attach the value to the var
        self.__vals = {}

    def __get__(self, obj, objtype=None):
        try:
            return self.__vals[obj]
        except KeyError:
            attr_name = self.name
            class_name = objtype.__name__

            raise AttributeError(
                f"'{class_name}' object has attribute '{attr_name}' unset"
            )

    def __set__(self, obj, value):
        if obj in self.__vals:
            attr_name = self.name
            class_name = type(obj).__name__

            raise ValueError(
                f"'{class_name}' object already has a value for attribute '{attr_name}'"
            )
        else:
            self.__vals[obj] = value

    def __set_name__(self, obj, name):
        self.name = name


class Final:
    def __get__(self, obj, objtype=None):
        attr_name = self.name
        class_name = objtype.__name__

        try:
            return getattr(obj, '__{}_final'.format(attr_name))
        except AttributeError:
            raise AttributeError(
                f"'{class_name}' object has attribute '{attr_name}' unset"
            )

    def __set__(self, obj, value):
        attr_name = self.name
        class_name = type(obj).__name__

        if hasattr(obj, '__{}_final'.format(attr_name)):
            raise ValueError(
                f"'{class_name}' object already has a value for attribute '{attr_name}'"
            )
        else:
            setattr(obj, '__{}_final'.format(attr_name), value)

    def __set_name__(self, obj, name):
        self.name = name


class Foo:
    bar = Final()


class Monty:
    spam = FinalGlobal()

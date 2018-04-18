# -*- coding: UTF-8 -*-


class ReturnStatus:
    code=""
    msg=""


class ReturnEntity:
    status=None
    data=None


class LoginReturn:
    auth_code=""


class CheckbookReturn:
    checkbooks=[]


def convert_to_builtin_type(obj):
    # Convert objects to a dictionary of their representation
    d = {
        }
    d.update(obj.__dict__)
    return d
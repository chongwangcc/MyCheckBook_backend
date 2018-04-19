# -*- coding: UTF-8 -*-


class ReturnStatus:
    code=""
    msg=""


class ReturnEntity:
    status=None
    data=None


class LoginReturn:
    auth_code=""


class CheckbookListReturn:
    checkbooks=[]


class CheckbookAddReturn:
    checkbook_id=""


class CheckbookGetReturn:
    checkbook = None


class CheckbookInvitationReturn:
    invitation_code = None


class AccountListReturn:
    accounts=[]

class AccountDeleteReturn:
    account_id=""


def convert_to_builtin_type(obj):
    # Convert objects to a dictionary of their representation
    d = {
        }
    d.update(obj.__dict__)
    return d
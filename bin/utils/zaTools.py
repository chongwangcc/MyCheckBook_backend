# -*- coding: UTF-8 -*-
import uuid
def genID():
    """
    生成id
    :return:
    """
    return str(uuid.uuid1()).replace("-", "")
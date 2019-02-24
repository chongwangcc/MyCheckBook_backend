# -*- coding: UTF-8 -*-

from models.Models import UserInfo
from tools import orm,db
import uuid


def main():
    u=UserInfo.find_by("where name = ?","cc");
    print(u)
    pass



if __name__ == "__main__":
    initUser()
    main()

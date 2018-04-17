from subprocess import Popen, PIPE



def excSQLFile(host, db, user, passwd, charset, filename):
    """
    执行sql文件
    :param host:
    :param db:
    :param user:
    :param passwd:
    :param charset:
    :param filename:
    :return:
    """
    process = Popen('mysql -h%s -D%s -u%s -p%s --default-character-set=%s' \
        % (host, db, user, passwd, charset),
        stdout=PIPE, stdin=PIPE, shell=True)
    output = process.communicate('source ' + filename)[0]
    return output



def create_table():

    pass
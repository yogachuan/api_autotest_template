import os.path


def aaa(**kwargs):
    head = dict(**kwargs)
    print(head)


if __name__ == '__main__':
    idc = {
        "name": "yujiachuan",
        "age": "24"
    }

    print(*idc)

    aaa(name='zhangsan', age='25')

    print(os.path.dirname(os.path.realpath('__file__')))
    print(os.path.dirname(os.path.realpath(__file__)))

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
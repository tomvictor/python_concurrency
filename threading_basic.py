import threading


def do_work(val):
    print("working...")
    print(val)
    print("work completed")
    return


if __name__ == "__main__":
    val = "Some test string"
    t = threading.Thread(target=do_work,args=(val,))
    t.start()
    j = threading.Thread(target=do_work,args=(val,))
    j.start()
    t.join()
    j.join()
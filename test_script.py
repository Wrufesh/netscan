import subprocess

import time

airodump = subprocess.Popen(['airodump-ng','prism0'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              # universal_newlines=True
                            )

for i in [1, 2, 3, 4 ,5]:
    time.sleep(10)
    # try:
    #     # o_airodump, unused_stderr = airodump.communicate(timeout=10)
    # except:
    #     print('hey')
    #     print(o_airodump)
    #     print('heyo')
    print(airodump.stdout.read())
    # print('One file printed')
    # # import ipdb
    # ipdb.set_trace()
    # time.sleep(300)
    # print(x)
airodump.kill()
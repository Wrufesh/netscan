import subprocess

import time

airodump = subprocess.Popen(['airodump-ng','prism0'],stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True
                            )

for i in [1, 2, 3, 4 ,5]:
    # time.sleep(10)
    try:
        # o_airodump, unused_stderr = airodump.communicate(timeout=10)
    except:
        print('hey')
        print(o_airodump)
        print('heyo')
    # o_file = airodump.stdout
    # x = o_file.read()
    # print(x)
    # print('One file printed')
    # # import ipdb
    # ipdb.set_trace()
    # time.sleep(300)
    # print(x)
airodump.kill()
import os
import subprocess

from netscan.celery import app
from netscan.settings import AIRODUMP_CSV_ROOT


@app.task
def start_airodump(monitor_interface):
    output_path = os.path.join(AIRODUMP_CSV_ROOT, monitor_interface)
    subprocess.Popen(
        'airodump-ng %s -w %s --write-interval 30 -o csv' % (
            monitor_interface,
            output_path
        ),
        shell=True
    )

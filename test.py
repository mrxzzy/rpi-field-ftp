import shutil

usage = shutil.disk_usage('/media/dest')

print(usage.used)

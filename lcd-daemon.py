#!/usr/bin/env python

import stat
import os
import sched, time
import shutil

import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.create_char(0,bytes([0x0,0x10,0x8,0x4,0x2,0x1,0x0,0x0]))

# read rsync status from /tmp/rsync_status
# * figure out files synced
# * files to sync
# * transfer rate

media_dest = '/dev/MediaDest'
mnt_dest = '/media/dest'
sequence_current = 0
task_current = 'I'
line1 = 'STARTUP'

prev_usage = 0
transfer_rate = 0

# checks used capacity on the destination media
def StatusMedia():
  global prev_usage
  global transfer_rate

  status = StatusDest()
  if status == 'M':
    # mounted, report usage and maybe data rate
    total, used, free = shutil.disk_usage(mnt_dest)

    # convert disk usage to GB
    used = used / 1024 / 1024 / 1024
    total = total / 1024 / 1024 / 1024

    if prev_usage == 0:
      rate = 0
    else:
      # estimate transfer rate in MB/s
      transfer_rate = (used - prev_usage) / 1024 / 1024

    prev_usage = used

    return '%.2f/%.1f GB' % (used,total)

  elif status == 'U':
    # disk is not mounted
    return 'SSD Unmounted'
  elif status == 'X':
    # disk not plugged in
    return 'SSD Unplugged'


# icon for SSD attached/missing
# * check if /dev/MediaDest exists

def StatusDest():
  global task_current

  if os.path.ismount(mnt_dest):
    #print("destination mounted")
    task_current = 'I'
    return 'M'
  elif os.path.exists(media_dest):
    if stat.S_ISBLK(os.stat(media_dest).st_mode):
      #print("destination present, not mounted")
      return 'U'
    else:
      #print('Destination storage missing')
      return 'X'
  else:
    #print('destination storage missing')
    return 'X'

# scan for button presses
# * shutdown (status icon: down arrow)
# * idle (status icon: I)

# spinner icon to indicate this script is working

def UpdateSpinner():
  global sequence_current

  sequence = ['-','\x00','|','/']
  sequence_current = (sequence_current + 1) % (len(sequence))
  return sequence[sequence_current]

# icon to indicate startup/shutdown/performin

# 0001/9999 55mb/s
# x V SD:M SSD:M

def UpdateLCD(schedule):
  global task_current
  global line1

  if task_current == 'S':
    line1 = 'SHUTDOWN ISSUED'
    lcd.message = '%-16s\n%s %s %1s %.0f MB/s' % (line1,UpdateSpinner(),task_current,StatusDest(),transfer_rate)
    os.system("/usr/sbin/shutdown -h now")
    task_current = 'D'
  elif task_current == 'D':
    pass
  else:
    line1 = StatusMedia()

  lcd.message = '%-16s\n%s %s %1s %.0f MB/s' % (line1,UpdateSpinner(),task_current,StatusDest(),transfer_rate)

  lcdupdater.enter(1,2, UpdateLCD, (schedule,))

def ReadInput(schedule):
  global task_current

  # Button mapping:
  # * select_button == shutdown

  if lcd.select_button:
    #shutdown system
    task_current = 'S'

  lcdupdater.enter(0.05,1,ReadInput, (schedule,))
    

lcdupdater = sched.scheduler(time.time, time.sleep)
lcdupdater.enter(1,1, UpdateLCD, (lcdupdater,))
lcdupdater.enter(0.05,1, ReadInput, (lcdupdater,))
lcdupdater.run()


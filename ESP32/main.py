import utime

TIMEOUT = 3 # Seconds

print('CTRL-C within 3 seconds to enter python REPL ...') 
utime.sleep(TIMEOUT)
print('Launching main robot controller...')

import go

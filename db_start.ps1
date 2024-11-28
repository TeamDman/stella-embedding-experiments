# pg_ctl -D data -l logfile start
# pg_ctl -D data -l logfile start -w
postgres -D data
# we have to run in blocking mode
# when starting using pgctl this happens lol


# ❯ .\db_start.ps1
# waiting for server to start.... done
# server started
# (hf) stella-embedding-experiments on  main [!?] via 🐍 v3.10.15 via 🅒 hf  
# ❯ python
# Python 3.10.15 | packaged by conda-forge | (main, Oct 16 2024, 01:15:49) [MSC v.1941 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>>
# KeyboardInterrupt
# >>> ^D
# KeyboardInterrupt
# >>>   
# >>> ^Z


# 2024-11-28 00:13:05.070 EST [13296] LOG:  received fast shutdown request
# 2024-11-28 00:13:05.071 EST [13296] LOG:  aborting any active transactions
# 2024-11-28 00:13:05.074 EST [13296] LOG:  background worker "logical replication launcher" (PID 3584) exited with exit code 1
# 2024-11-28 00:13:05.076 EST [36396] LOG:  shutting down
# 2024-11-28 00:13:05.077 EST [36396] LOG:  checkpoint starting: shutdown immediate
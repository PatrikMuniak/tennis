from datetime import datetime
ts = 720*60

print(datetime.fromtimestamp(ts).strftime('%H:%M:%S'))

import glob
from datetime import date

visitorscounter = len(glob.glob1('/home/ubuntu/arpe/data/app_uploaded_files/',"*.txt"))

today = date.today()

visitorStats =  open('/home/ubuntu/arpe/data/Stats/' + str(today) + ".txt", "w")
visitorStats.write(str(visitorscounter))
visitorStats.close()

print(visitorscounter)
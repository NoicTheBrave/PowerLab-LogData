import datetime
 
# using now() to get current time
current_time = datetime.datetime.now()
 
# Printing value of now.
print("Time now at greenwich meridian is:", current_time)

temp = str(current_time)

temp = temp[0:10] + "_" +temp[11:13] + "-" + temp[14:16] + "-" + temp[17:19]

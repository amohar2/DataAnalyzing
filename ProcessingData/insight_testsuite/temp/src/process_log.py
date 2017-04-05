
# This file studies information gathered from NASA site in log.txt for following features:
# Feature 1: top 10 most active host/IP
# Feature 2: top 10 resources that consume the most bandwidth
# Feature 3: top 10 busiest resources 60-minute periods
# Feature 4: patterns of three failed login attempts

# We also study three addition features:
# Feature 5: top 10 users that have the more number of failure attempts 
# Feature 6: top 10 users that got more amount of bytes from a site
# Feature 7: checking total number of failure attempt for IP and non-IP user

###################### HELPER FUNCTIONS #######################
#check if byte is a number, if not 0 will be considered for it
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#computing seconds between two date_time s
list_months = {"Jan": 1, "Feb": 2, "March": 3, "April": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12}

from datetime import date
def delay(date_new, time_new, date_old, time_old):
	d1 = date_new.split('/')
	d2 = date_old.split('/')

	delta = date(int(d1[2]), list_months[d1[1]], int(d1[0])) - date(int(d2[2]), list_months[d2[1]], int(d2[0]))
	delay_time = delta.days * 3600 + (time_new - time_old)

	return delay_time

#check if user_name is IP or host(non-IP)
def if_ip(user_name):
	for c in user_name:
		if c.isdigit() or c == '.':
			return False
	return True

###################### STORING USER AND WEB INFORMATION ###################### 
class user_info(object):												#Storing infromation for a user
	def __init__(self):
		self.number_of_user_access = 0 									#Counting how many times a user accessed a site		
		self.total_failed_access = 0 									#Counting total number of the failure attempts  
		self.consecutive_failed_access = 0 								#Counting 3 consecutive failure attempts        
		self.failed_access_time = 0 									#Recording time for the first failure attempts  
		self.failed_access_date = "" 									#Recording date for the first failure attempts  
		self.block_time = 0 											#Recording time for the first block 			
		self.block_date = "" 											#Recording date for the first block 			
		self.if_block = 0 												#Stating if a user account is blocked for 5 min 
		self.time_seconds = 0 											#Recording time (sec) user accessed a site
		self.date = ""													#Recording date (DD/MON/YYYY) user accessed a site
		self.web = "" 													#Recording website a user accessed
		self.byte = 0 													#Recording total amount of bytes user used		
	def convert_time_to_seconds(self, date_time):						#Splitting DD/MON/YYYY:HH:MM:SS into date = DD/MON/YYYY and time_seconds = seconds(HH:MM:SS) 
		raw_time_info = date_time.split(':')
		self.time_seconds = int(raw_time_info[1]) * 60 * 60 \
			+ int(raw_time_info[2]) * 60 + int(raw_time_info[3])
		self.date = raw_time_info[0]
	def update_user_info(self, date_time, web_, usage_byte):			#Updating user information included in __init__
		self.number_of_user_access += 1
		self.web = web_
		#removing last character of web if it is "
		if web_.endswith('"'):									
			self.web = self.web[:-1]
		self.convert_time_to_seconds(date_time)
		if is_number(usage_byte):
			self.byte += int(usage_byte)

	def first_failure_update(self, time_, date_):						#Updating user information regards for its first failure
		self.total_failed_access += 1
		self.consecutive_failed_access = 1
		self.failed_access_time = time_
		self.failed_access_date = date_
	def first_blocking_update(self):									#Updating user information regards for its first blocking occurance
		self.block_time = self.time_seconds
		self.block_date = self.date
		self.if_block = 1


class web_info(object):													#Storing information for each accessed website
	def __init__(self):	
		self.number_of_web_access = 0 									#Counting how many times a website was accessed 		
		self.byte = 0 													#Counting how many bytes was trasfrred in each attempts	
	def update_web_info(self, usage_byte): 								#Updating web information included in __init__
		self.number_of_web_access += 1
		if is_number(usage_byte):
			self.byte += int(usage_byte)

###################### PRINTING STORED INFORMATION ###################### 
def print_user_info(user_):
	print user_.number_of_user_access, ",", user_.total_failed_access, "," \
		, user_.time_seconds, "," , user_.web, "," , user_.byte

def print_web_info(web_):
	print web_.number_of_web_access, ",", web_.byte

def print_user_map(user_name, user_map_):
	print "[" + user_name + "]: " , print_user_info(user_map_[user_name])

def print_web_map(web_name, web_map_):
	print "[" + web_name + "]: " , print_web_info(web_map_[web_name])

###################### HASH MAPS ###################### 
#hashmap for users: user_map["user_name"] = user_info (class)
user_map = {}

#hashmap for web: web_map["web_ID"] = web_info (class)
web_map = {}

#hashmap for nasa: nasa_map["time"] = number_of_site_access (int)
nasa_map = {}

#hashmap for studying if IP fails more or non-IP: failure_map["IP" or "non-IP"] = number_of_failures
failure_map = {"IP": 0, "non-IP": 0}

###################### STUDYING DATA ######################
import time
start_time = time.time()

#////// FEATURE 4 : patterns of three failed login attempts \\\\\\
feature_4_data = open("../temp/log_output/blocked.txt", "w")

#reading first line from log.txt
file_data = open("../temp/log_input/log.txt", "r")
first_line_data = file_data.readline().split(' ') #10 elements per line

#recoding accessong to NASA site per 60 min
site_access = 0
site_date_time = first_line_data[3][1:]
raw_time_info = site_date_time.split(':')

#initial time for recording accessong to NASA site per 60 min
init_time = int(raw_time_info[1]) * 60 * 60 + int(raw_time_info[2]) * 60 + int(raw_time_info[3])
nasa_map[site_date_time] = site_access

#reading log.txt line by line
with open('../temp/log_input/log.txt') as f:
	for line in f:
		content_line = line.split(' ')
		user_name = content_line[0]
		date_time = content_line[3][1:]
		transferred_byte = content_line[len(content_line) - 1]

		#information in some of the line are not organized clearly, 
		#which needs below command to extract requested web_address correctly:
		#web_address exists after / and before HTTP/1.0" or "
		start_of_request_pos = line.find('"')
		start_of_web_address = line.find('/', start_of_request_pos + 1)
		end_of_web_address = line.find('"', start_of_web_address + 1) - 1
		HTTP_pos = line.find("HTTP/1.0")
		if HTTP_pos == -1:
			HTTP_pos = end_of_web_address

		#getting raw web address
		web_address = line[start_of_web_address:HTTP_pos]

		#cleaning web_address from extra spaces
		web_address.replace(" ", "")

		#////////// USER INFORMATION \\\\\\\\\\\\\\
		#storing information per line for a user
		#if new_user already exists in user_map, so update its info
		#else add new_user in user_map
		if user_name in user_map:
			prev_access_time = user_map[user_name].time_seconds
			prev_access_date = user_map[user_name].date
			prev_web_accessed = user_map[user_name].web

			#updating user information
			user_map[user_name].update_user_info(date_time, web_address, transferred_byte)

			#check if previous web access was failed within less than 20 sec
			if (prev_web_accessed == user_map[user_name].web):

				#check if this is the first failure
				if (user_map[user_name].consecutive_failed_access == 0 and \
					delay(user_map[user_name].date, user_map[user_name].time_seconds\
						, prev_access_date, prev_access_time) < 20):
					user_map[user_name].first_failure_update(prev_access_time, prev_access_date)

					#is IP or non-IP is failed
					if(if_ip(user_name)):
						failure_map["IP"] += 1
					else:
						failure_map["non-IP"] += 1

				#check if this failure happend within 20 sec from the first one
				elif user_map[user_name].consecutive_failed_access >= 1:
					if (delay(user_map[user_name].date, user_map[user_name].time_seconds\
						, user_map[user_name].failed_access_date, user_map[user_name].failed_access_time) <= 20):
						user_map[user_name].total_failed_access += 1
						user_map[user_name].consecutive_failed_access +=1

						#is IP or non-IP is failed
						if(if_ip(user_name)):
							failure_map["IP"] += 1
						else:
							failure_map["non-IP"] += 1

						#turn on blocker if this failure reaches 3 times within less than 20 sec
						if(user_map[user_name].consecutive_failed_access == 3):
							user_map[user_name].first_blocking_update()

			#block for 5 min if failed occures 3 times within less than 20 seconds
			if user_map[user_name].if_block == 1:
				if (delay(user_map[user_name].date, user_map[user_name].time_seconds\
					, user_map[user_name].block_date, user_map[user_name].block_time) < 300):
					feature_4_data.write(line)
				else:
					user_map[user_name].consecutive_failed_access = 0
					user_map[user_name].if_block == 0

		else:
			new_user = user_info()

			#updating user information	
			new_user.update_user_info(date_time, web_address, transferred_byte)
			user_map[user_name] = new_user

		#////////// WEB INFORMATION \\\\\\\\\\\\\\
		#storing information for web
		#if new_web already exists in web_map, so update its info
		#else add new_web in web_map
		if web_address in web_map:
			web_map[web_address].update_web_info(transferred_byte)

		else:
			new_web = web_info()

			#updating web information	
			new_web.update_web_info(transferred_byte)
			web_map[web_address] = new_web

		#////////// NASA site acccess \\\\\\\\\\\\\\ 
		#in each 60 min store data in nasa_map
		site_access += 1
		nasa_map[site_date_time] += 1

		if ((init_time + 3600) < user_map[user_name].time_seconds):
			init_time += 3600
			nasa_map[site_date_time] -= 1
			site_access = 1
			site_date_time = date_time
			nasa_map[site_date_time] = site_access

###################### PRINTING INFORMATION ######################
#printing user_map info	
#print "users information are as below:\n"
#for user_name in user_map:
#	print_user_map(user_name, user_map)

#printing web_map info
#print "webs information are as below:\n"
#for web_name in web_map:
#	print_web_map(web_name, web_map)

#printing nasa_map info
#print "NASA access-houre-priod information are as below:\n"
#for date_time in nasa_map:
#	print date_time, nasa_map[date_time]

###################### FEATURE 1 ######################
#using nlargest 
from heapq import nlargest

#listing 10 most active host/IP
list_10_most_active_host = nlargest(10, user_map, key=lambda k: user_map[k].number_of_user_access) 

feature_1_data = open("../temp/log_output/hosts.txt","w") 
for host_name in list_10_most_active_host:
	feature_1_data.write(host_name + ",")
	feature_1_data.write(str(user_map[host_name].number_of_user_access) + "\n")
feature_1_data.close()

###################### FEATURE 2 ######################
#10 resources that consume the most bandwidth (summation of total obtained bytes)
list_10_most_resouce_bandwidth = nlargest(10, web_map, key=lambda k: web_map[k].byte)

feature_2_data = open("../temp/log_output/resources.txt", "w")
for web_name in list_10_most_resouce_bandwidth:
	feature_2_data.write(web_name + "\n")
feature_2_data.close()

###################### FEATURE 3 ######################
#top 10 busiest 60-minute periods
list_10_most_busiest_hours = nlargest(10, nasa_map, key=lambda k:nasa_map[k])

feature_3_data = open("../temp/log_output/hours.txt", "w")
for time_ in list_10_most_busiest_hours:
	feature_3_data.write(time_ + " -0400,")
	feature_3_data.write(str(nasa_map[time_]) + "\n")
feature_3_data.close()

###################### FEATURE 4 ######################
#already included within a blocked.txt during execution
feature_4_data.close()

###################### FEATURE 5 ######################
#top 10 users that have the more number of failure attempts 
list_10_most_failure_host = nlargest(10, user_map, key=lambda k: user_map[k].total_failed_access)

feature_5_data = open("../temp/log_output/failure_hosts.txt", "w")
for host_name in list_10_most_failure_host:
	feature_5_data.write(host_name + ",")
	feature_5_data.write(str(user_map[host_name].total_failed_access) + "\n")
feature_5_data.close()

###################### FEATURE 6 ######################
#top 10 users that got the most byte
list_10_most_consumer_host = nlargest(10, user_map, key=lambda k: user_map[k].byte)

feature_6_data = open("../temp/log_output/consumer_hosts.txt", "w")
for host_name in list_10_most_consumer_host:
	feature_6_data.write(host_name + ",")
	feature_6_data.write(str(user_map[host_name].byte) + "\n")
feature_6_data.close()

###################### FEATURE 7 ######################
#check if the most failer is IP or non-IP user
feature_7_data = open("../temp/log_output/IP_failure.txt", "w")
feature_7_data.write("IP:" + str(failure_map["IP"]) + "\n")
feature_7_data.write("non-IP:" + str(failure_map["non-IP"]) + "\n")

print("--- %s seconds ---" % (time.time() - start_time))


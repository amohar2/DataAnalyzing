
# Table of Contents
1. [Studied Features](README.md#studied-features)
2. [Data Structure Used For Analyzing Data](README.md#data-structure-used-for-analyzing-data)
3. [Helper functions](README.md#helper-functions)
4. [Analyzing Data and Sorting](README.md#analyzing-data-and-storing)
5. [Additional Notes](README.md#additional-notes)

# Studied Features
In this project, the following features are studied on a NASA site data included in log.txt:

## Required features
### Feature 1 : [hosts.txt]
Top 10 most active hosts/IP addresses. 						
### Feature 2 : [resources.txt]
Top 10 resources that consume the most bandwidth. 					
### Feature 3 : [hours.txt]
Top 10 busiest resources 60-minute periods. 						
### Feature 4 : [blocked.txt]
Patterns of three failed login attempts. 						


## Additional features:
### Feature 5 : [failure_hosts.txt]
Top 10 users that have the more number of failure attempts. 				
### Feature 6 : [consumer_hosts.txt]
Top 10 users that got more amount of bytes from a site. 				
### Feature 7 : [IP_failure.txt]
Checking total number of failure attempt for IP and non-IP user. 			


## More details about additional features (features 5, 6, 7)
We added three more additional features for analyzing data from log.txt:

Feature 5 : studies about the failure attempts of the hosts/IP and lists 10 top of them in failure_hosts.txt.

Feature 6 : studies about the total amount of bytes each user gets in his access and lists 10 top of them in consumer_hosts.txt.

Feature 6 : also studies about the failure attempts of the hosts/IP to check how many of these attempts are failed for a user with IP address and for a user with non-IP address and lists the total number for all IP’s failure attempts and all non-IP’s failure attempts in IP_failure.txt.


# Data Structure Used For Analyzing Data
## Storing information for each user and website
Since we want to explore the features of the users and websites, so we use two `class` for storing their information: 
- **user_info** for storing information for each user:
1. How many times a user accessed a site.		
2. The total number of the failure attempts.  
3. 3 consecutive failure attempts.        
4. Time for the first failure attempts.  
5. Date for the first failure attempts.  
6. Time for the first blocked attempts. 			
7. Date for the first block attempts.		
8. Time (seconds) user accessed a site.
9. Date (DD/MON/YYYY) user accessed a site.
10. Website a user accessed.
11. Total amount of bytes user used.	

- **web_info** for storing information for each web address:
1. How many times a website was accessed .		
2. How many bytes was transferred in each attempts.	

## Storing all information 
In order to use less possible amount of memory and having efficient data access, we use hashmaps:
- **user_map** : hashmap for user: user_map["user_name"] = user_info.
- **web_map** : hashmap for web: web_map["web_ID"] = web_info.
- **nasa_map** : hashmap for nasa: nasa_map[“date_time"] = number of site access (60-minute period).
- **failure_map** : hashmap for studying if IP fails more or non-IP: failure_map["IP" or "non-IP"] = number of IP/non-IP failure attempts.

# Helper functions
For analyzing data, three helper functions are used:
* `is_number` : checks if byte is a number, if not 0 will be considered for it.
* `if_ip` : checks if user_name is IP or host(non-IP).
* `delay` : computing seconds between two date_time s.

# Analyzing Data and Sorting
We study data to find 10 top users/websites for each feature. So heap queue algorithm (or priority queue algorithm) can be implemented here. We use `heapq.nlargest` that returns a list with the n largest elements from the dataset, where its time complexity is `O(log(m) * n)` : m = total number of elements and n = finding n largest elements.


# Additional Notes 
I think the provided test in the `insight_testsuite` folder is not correct as the its output `hours.txt` file includes following data for the small tested log.txt within a path `insight_testsuite/temp/log_input`:

    01/Jul/1995:00:00:02 -0400,9
    01/Jul/1995:00:00:03 -0400,9
    01/Jul/1995:00:00:04 -0400,9
    01/Jul/1995:00:00:05 -0400,9
    01/Jul/1995:00:00:06 -0400,9
    01/Jul/1995:00:00:07 -0400,8
    01/Jul/1995:00:00:08 -0400,8
    01/Jul/1995:00:00:09 -0400,8
    01/Jul/1995:00:00:10 -0400,7
    …

These outputs are not correct, as based on explanation for feature 3, it should list in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period. However as we can wee, the provided output results are printed per each second, not each 60-min!

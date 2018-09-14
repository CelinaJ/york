
import requests
import random
import time
import urllib3
import certifi
import argparse
import os

def random_user_agent():
	user_agents = \
		["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
		 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
		 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
		 "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
		 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
		 "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
		 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
		 "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
		 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
		 "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
		 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
		 "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
		 "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
		 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
		 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"]
	return random.choice(user_agents)

class Google:
	def __init__(self):
		self.session = requests.Session()

	def get_num_searches(self, query):
		url = "http://www.google.com/search?q="
		about_tag = '''id="resultStats">About '''
		no_results_tag = '''No results found for <b>"'''
		tag = '''id="resultStats">'''
		is_blocked = True
		wait = 0	
		# time.sleep(random.randint(3, 10))
      
		while is_blocked == True:
			time.sleep(wait)

			self.session.headers.update({"User-Agent": random_user_agent()})
			search_result = self.session.get(url + query, verify=True)
			raw_html = search_result.text

			# check if there are exact results
			if raw_html.find(no_results_tag) > 0:
				num_results = 0
				print(query + "\t" + str(num_results)) 
			elif raw_html.find(about_tag) > 0:
				ind = raw_html.find(about_tag) + len(about_tag)
				end_ind = ind

				while raw_html[end_ind].isdigit() or raw_html[end_ind] == ",":
					end_ind += 1

				num_results = raw_html[ind:end_ind] 
				print(query + "\t" + str(num_results))  
			else:
				ind = raw_html.find(tag) + len(tag)
				end_ind = ind

				while raw_html[end_ind].isdigit() or raw_html[end_ind] == ",":
					end_ind += 1

				num_results = raw_html[ind:end_ind] 
				print(query + "\t" + str(num_results))       

			if raw_html.find("Our systems have detected unusual traffic from your computer network.") == -1:
				is_blocked = False  # search went through
			else:	
				wait += 60
				print("WAITING FOR " + str(wait) + " SECONDS BEFORE RETRYING GOOGLE QUERY...")

		return num_results

	def get_recommanded_query(self, query):
		autocomplete_url = "http://google.com/complete/search?output=toolbar&q="
		suggestion_tag = '''<CompleteSuggestion><suggestion data="'''
		self.session.headers.update({"User-Agent": random_user_agent()})
		print(query)
		recommanded_searches = self.session.get(autocomplete_url + query, verify=True)
		raw_html = recommanded_searches.text
			
		# check if there are auto suggestions
		end_ind = 0
		result = []
		while raw_html.find(suggestion_tag, end_ind) > 0:
			ind = raw_html.find(suggestion_tag, end_ind) + len(suggestion_tag)
			end_ind = ind

			while raw_html[end_ind] != '''"''':
				end_ind += 1

			suggestion = '"' + raw_html[ind:end_ind] + '"'
			if query[:-1].lower() in suggestion.lower():
				result.append(suggestion)

		return result

def main(adjective_file, verb_file):
	# Open files and initialize variables
	adj_file = open(adjective_file, "r")
	adj_lines = adj_file.readlines()
	adj_file.close()

	verb_file = open(verb_file, "r")
	verb_lines = verb_file.readlines()
	verb_file.close()

	f = open("results_main.txt", "w")
	vowels = ["a", "e", "i", "o", "u"]
	google = Google()

	# start reading txt files line by line and extract adjectives/verbs
	for i in range(len(adj_lines)):
		adj = adj_lines[i].strip().split("\t")[0]

		# find google recommanded searches
		query = '''"I am {} because "'''.format(adj)
		suggestions = google.get_recommanded_query(query)
		for suggestion in suggestions:
			num_results = google.get_num_searches(suggestion)
			f.write(suggestion + "\t" + str(num_results) + "\n")

		query = '''"You are {} because "'''.format(adj)
		suggestions = google.get_recommanded_query(query)
		for suggestion in suggestions:
			num_results = google.get_num_searches(suggestion)
			f.write(suggestion + "\t" + str(num_results) + "\n")

		query = '''"They are {} because "'''.format(adj)
		suggestions = google.get_recommanded_query(query)
		for suggestion in suggestions:
			num_results = google.get_num_searches(suggestion)
			f.write(suggestion + "\t" + str(num_results) + "\n")

		query = '''"We are {} because "'''.format(adj)
		suggestions = google.get_recommanded_query(query)
		for suggestion in suggestions:
			num_results = google.get_num_searches(suggestion)
			f.write(suggestion + "\t" + str(num_results) + "\n")

		query = '''"She is {} because "'''.format(adj)
		suggestions = google.get_recommanded_query(query)
		for suggestion in suggestions:
			num_results = google.get_num_searches(suggestion)
			f.write(suggestion + "\t" + str(num_results) + "\n")

		query = '''"He is {} because "'''.format(adj)
		suggestions = google.get_recommanded_query(query)
		for suggestion in suggestions:
			num_results = google.get_num_searches(suggestion)
			f.write(suggestion + "\t" + str(num_results) + "\n")
		
		# google clauses made from adj and verb files
		for j in range(len(verb_lines)):
			verb = verb_lines[j].strip().split("\t")[0]

			# simple present tense
			query = '''"I am {} because I {}"'''.format(adj, verb)
			num_results = google.get_num_searches(query)
			f.write(query + "\t" + str(num_results) + "\n") 

			query = '''"You are {} because you {}"'''.format(adj, verb)
			num_results = google.get_num_searches(query)
			f.write(query + "\t" + str(num_results) + "\n")	

			query = '''"They are {} because they {}"'''.format(adj, verb)
			num_results = google.get_num_searches(query)
			f.write(query + "\t" + str(num_results) + "\n")

			query = '''"We are {} because we {}"'''.format(adj, verb)	
			num_results = google.get_num_searches(query)
			f.write(query + "\t" + str(num_results) + "\n")

			if (len(verb) >= 3) and (verb[-2:-1] in vowels) and (verb[-1] == "y"):
				verb2 = verb + "s"
			elif len(verb) >= 3 and (verb[-2:-1] not in vowels) and (verb[-1] == "y"):
				verb2 = verb[:-1] + "ies"
			elif (verb.endswith("o") or verb.endswith("ch") or verb.endswith("sh") or
			    verb.endswith("ss") or verb.endswith("x") or verb.endswith("z")):
				verb2 = verb + "es"
			elif verb == "have":
				verb2 = "has"
			else:
				verb2 = verb + "s"

			query = '''"She is {} because she {}"'''.format(adj, verb2)	
			num_results = google.get_num_searches(query)
			f.write(query + "\t" + str(num_results) + "\n")	

			query = '''"He is {} because he {}"'''.format(adj, verb2)	
			num_results = google.get_num_searches(query)
			f.write(query + "\t" + str(num_results) + "\n")		 

	f.close()

def is_valid_file(parser, arg):
	abs_arg = os.path.abspath(arg)
	if not os.path.exists(abs_arg):
		parser.error("The file %s does not exist." % arg)
	else:
		return arg

def parse_command():
	parser = argparse.ArgumentParser(description='Generate "I am [adjective] because I [verb]" clauses from given adjective and verb files')
	parser.add_argument('adjective_file', 
						metavar="adjective_file", 
						type=lambda x: is_valid_file(parser, x),
						help='an adjective file in txt')
	parser.add_argument('verb_file',  
						metavar="verb_file", 
						type=lambda y: is_valid_file(parser, y),
						help='a verb file in txt')

	args = parser.parse_args()
	return args


if __name__ == "__main__":
	filenames = parse_command()
	main(filenames.adjective_file, filenames.verb_file)









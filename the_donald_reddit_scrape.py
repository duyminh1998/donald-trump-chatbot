import sqlite3
import json
import requests

connection = sqlite3.connect('database/{}.db'.format('donald_trump_chatbot'))
c = connection.cursor()

# build table
def create_table():
	c.execute("""CREATE TABLE IF NOT EXISTS qa_pair (parent_id TEXT, id TEXT PRIMARY KEY, parent_data TEXT, body TEXT, created_utc INT, score INT)""")

# data processing
def clean_comment(comment):
	comment = comment.replace('\n',' newlinechar ').replace('\r',' newlinechar ').replace('"',"'")
	return comment

# sql insertion
def sql_no_parent(parent_id, comment_id, body, created_utc, score):
	try:
		sql = """INSERT INTO qa_pair (parent_id, id, body, created_utc, score) VALUES ("{}", "{}", "{}", {}, {});""".format(parent_id, comment_id, body, int(created_utc), score)
		c.execute(sql)
		connection.commit()
	except Exception as e:
		print("SQL No Parent Insertion Error: ", str(e))

def sql_has_parent(parent_id, comment_id, parent_data, body, created_utc, score):
	try:
		sql = """INSERT INTO qa_pair (parent_id, id, parent_data, body, created_utc, score) VALUES ("{}", "{}", "{}", "{}", {}, {});""".format(parent_id, comment_id, parent_data, body, int(created_utc), score)
		c.execute(sql)
		connection.commit()
	except Exception as e:
		print("SQL Has Parent Insertion Error: ", str(e))

def sql_update(parent_id, comment_id, parent_data, body, created_utc, score):
	try:
		c.execute("""UPDATE qa_pair SET parent_id = ?, id = ?, parent_data = ?, body = ?, created_utc = ?, score = ? WHERE parent_id = ?;""", (parent_id, comment_id, parent_data, body, int(created_utc), score, parent_id))
		connection.commit()
	except Exception as e:
		print("SQL Update Insertion Error: ", str(e))

# parent existence
def find_parent(parent_id):
	try:
		sql = "SELECT body FROM qa_pair WHERE id = '{}' LIMIT 1".format(parent_id)
		c.execute(sql)
		result = c.fetchone()
		if result != None:
			return result[0]
		else:
			return False
	except Exception as e:
		print("Find Parent Error: ", str(e))

# find score
def existing_score(parent_id):
	try:
		sql = """SELECT score FROM qa_pair WHERE parent_id = '{}' LIMIT 1;""".format(parent_id)
		c.execute(sql)
		result = c.fetchone()
		if result != None:
			return result[0]
		else:
			return False
	except Exception as e:
		print("Find existing score Error: ", str(e))

def accept(data):
        if len(data.split(' ')) > 1000 or len(data) < 1:
                return False
        elif len(data) > 32000:
                return False
        elif data == '[deleted]':
                return False
        elif data == '[removed]':
                return False
        else:
                return True

# main loop
if __name__ == '__main__':
	try:
		create_table()
		after_utc = 0
		number_processed = 0
		paired_rows = 0
		continue_scrape = True
		while continue_scrape:
			url = 'https://api.pushshift.io/reddit/search/comment/?subreddit=The_Donald&size=500&after=' + str(after_utc) + '&fields=parent_id,id,body,created_utc,score'
			r = requests.get(url)
			parsed_json = json.loads(r.text)
			if len(parsed_json['data']) > 0:
				for comment in parsed_json['data']:
					parent_id = comment['parent_id'].split('_')[1]
					comment_id = comment['id']
					body = clean_comment(comment['body'])
					created_utc = comment['created_utc']
					score = comment['score']
					parent_data = find_parent(parent_id)
					if accept(body):
						# parent data exists
						if parent_data:
							old_score = existing_score(parent_id)
							if old_score:
								if score > old_score:
									sql_update(parent_id, comment_id, parent_data, body, created_utc, score)
									paired_rows += 1
								else:
									pass
							else:
								sql_has_parent(parent_id, comment_id, parent_data, body, created_utc, score)
								paired_rows += 1
						# no parent data
						else:
							sql_no_parent(parent_id, comment_id, body, created_utc, score)
				c.execute("""DELETE FROM qa_pair WHERE parent_data IS NULL""")
				connection.commit()
				c.execute("VACUUM")
				connection.commit()
				after_utc = parsed_json['data'][-1]['created_utc']
				number_processed += 1
				print('Number of pages processed: {}'.format(number_processed), 'Current UTC: {}'.format(after_utc), 'Paird rows: {}'.format(paired_rows))
			else:
				continue_scrape = False
	except Exception as e:
		print('Main Loop Error: ', str(e))

import MySQLdb
import mw_util
import wmflabs_queries

class CommmonsCatMetrics:
	"""Wrapper class for the Category Metrics"""
	def __init__(self, category):
		self.catname = category
		self.catsql = category.replace(" ", "_")
		self.db = MySQLdb.connect(host="commonswiki.labsdb", db="commonswiki_p", read_default_file="~/replica.my.cnf")
		self.cursor = self.db.cursor()

	def get_uploaders(self, timestamp1, timestamp2):
		query = wmflabs_queries.count_uploaders_in_category(self.catsql, timestamp1, timestamp2)
		self.cursor.execute(query)
		print self.cursor.fetchall()

	def glamorous(self):
		"""wrapper to glamorous"""
		from glamorous import GlamorousParser
		glamorous = GlamorousParser(self.category)
		glamorous.statistics()

	def close(self):
		self.db.close()

def main():
	"""Commons Cat Metrics."""
	parser = ArgumentParser(description="Commons Cat Metrics")

	parser.add_argument("-c", "--category",
                        type=str,
                        dest="category",
                        metavar="CAT",
                        required=True,
                        help="The Commons category without Category:")
	args = parser.parse_args()
	metrics = CommonsCatMetrics(args.category)
	
	metrics.close()

if __name__ == "__main__":
	main()

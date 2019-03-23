import expanddouban
import bs4
import requests
import operator

location_set_size={}#类型中地区数量的字典
category_set = {}
category_all_size = {}

#任务一
def getMovieUrl(category,location):
	"""
	return a string corresponding to the URL of douban movie lists given category and location.
	"""
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)
	return url
#任务二(此处注掉，在后面任务四中应用)
#html = expanddouban.getHtml(getMovieUrl("剧情","美国"),True)

#任务三
class Movie():
	"""docstring for Movie"""
	def __init__(self, name, rate, location, category, info_link, cover_link):
		self.name = name
		self.rate =rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link
	def print_data(self):
		return "{},{},{},{},{},{}\n".format(self.name,self.rate,self.location,self.category,self.info_link,self.cover_link)

#任务四
def getMovies(category, location):
	"""
	return a list of Movie objects with the given category and location.
	"""
	movies=[]
	for loc in location:
		html = expanddouban.getHtml(getMovieUrl(category,loc),True)
		soup = bs4.BeautifulSoup(html, "html.parser")
		content_a_list = soup.find(id='content').find(class_='list-wp').find_all('a',recursive=False)
		location_set_size[loc] = len(content_a_list)
		for content_a in content_a_list:
			movie_name = content_a.find(class_ = "title").string
			movie_rate = content_a.find(class_='rate').string
			movie_location = loc
			movie_category = category
			movie_info_link = content_a.get('href')
			movie_cover_link = content_a.find('img').get('src')
			movies.append(Movie(movie_name,movie_rate,movie_location,movie_category,movie_info_link,movie_cover_link).print_data())
	category_set[category] = location_set_size
	return movies



#任务五、六
category_list = ["剧情","爱情","喜剧"]
locations=[]
htmls = expanddouban.getHtml("https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,")
soups = bs4.BeautifulSoup(htmls, "html.parser")
location_list = soups.find(id='content').find_all(class_="tag")
for locs in location_list:
	locations.append(locs.string)
for cat in category_list:
	ms = getMovies(cat,locations[27:47])
	category_all_size[cat] = len(ms)
	with open("movies.csv","a") as f:
		for m in ms:
			f.write(m)
	all_size = category_all_size[cat]
	for i in range(3):
		percentage = round(sorted(location_set_size.items(),key=lambda item:item[1],reverse =True)[0:3][i][1]/all_size*100,2)
		with open("output.txt","a") as f_w:
			f_w.write("{}的第{}名的地区是{}所占百分比为{}\n".format(cat,str(i+1),str(sorted(location_set_size.items(),key=lambda item:item[1],reverse =True)[0:3][i][0]),percentage))
	
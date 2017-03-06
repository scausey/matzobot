from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import pprint

# TODO: Check for errors when loading php.

url = "https://www.smith.edu/diningservices/menu_poc/cbord_menus.php"
response = requests.get(url)
bsObj = BeautifulSoup(response.content, "html.parser")

#Check if a menu is empty. Returns true or false.
def isEmpty(block):
	childList = block.contents
	print("List of block's children: " +str(childList))
	for child in childList:
		print("current child in childList: " +str(child))
		print("child type: " +str(type(child)))
		#Check for empty dining hall menus. Make sure element has class attribute.
		if child.get("class") != None:
			childClasses = child.get("class")
			print("childClasses list: " +str(childClasses))
			for childClass in childClasses:
				print("childClass's class: " +str(childClass))
				if childClass == 'smith-menu-empty' or childClass == 'row':
					print("childClass has a div with value smith-menu-empty or row. Returning true.")
					return True
				else: 
					print("childClass does not have a div with value smith-menu-empty or row.")
					return False
		print("Checking if child type is navigablestring.")
		if str(type(child)) == "<class 'bs4.element.NavigableString'>":
			continue
		

#Returns the dininghall. 
def getDiningHall(block):
	print("getDiningHall function called.")
	diningHallBlock = block.find("div", {"class" : "col-md-12"})
	print("diningHallBlock list of col-md-12s: " +str(diningHallBlock))
	print("Length of diningHallBlock list of col-md-12s: " +str(len(diningHallBlock)))
	print("isEmpty function called for getDiningHall function.")
	if isEmpty(diningHallBlock):
		return
	else:
		print("Passed isEmpty test. Getting location.")
		location = diningHallBlock.find("span").get_text().lower().strip()
		print("Location: " +location)
		return location

#Returns a meal.
def getMeal(block, foodDict, location):
	print("getMeal function called.")
	mealBlocks = block.findAll("div", {"class" : "col-xs-4"})
	mealsLs = []
	for mealBlock in mealBlocks:
		#Locate the meal.
		meal = mealBlock.find("h4")
		if isEmpty(mealBlock):
			continue

		if str(type(meal)) == "<class 'NoneType'>":
			continue

		else:
			meal = meal.get_text().lower().strip()
			#Join meal with location. 
			s = '-'
			seq = (location, meal)
			locationAndMeal = s.join(seq)

			#Find the foods for that meal.
			foodItems = mealBlock.findAll("td")
			for foodItem in foodItems:
				food = foodItem.get_text().lower().strip()

				#Add the food item to the dictionary, along with where and when.
				if food in foodDict:
					foodDict[food].append(locationAndMeal)
				else:
					foodDict.setdefault(food, [])
					foodDict[food] = [locationAndMeal]

#Main method.
foodDict = defaultdict(list)
blocks = bsObj.find_all("div", {"class" : "smith-menu-wrapper"})

#Get information.
count = 0
for block in blocks:
	count+=1
	location = getDiningHall(block)
	getMeal(block, foodDict, location)
	if count == 1:
		break

pp = pprint.PrettyPrinter(compact=True)
pp.pprint(foodDict)


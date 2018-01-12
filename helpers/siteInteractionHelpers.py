import base64

def viewCatalog(taskSet):
	taskSet.client.get("/category.html", headers={"User-Agent":taskSet.uaString})

def viewItemDetails(taskSet, item_id):
	taskSet.client.get("/detail.html?id={}".format(item_id), headers={"User-Agent":taskSet.uaString})

def applyFilter(taskSet):
	taskSet.client.get("/category.html?tags=brown", headers={"User-Agent":taskSet.uaString})

def login(taskSet, username, password):
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	taskSet.client.get("/login", headers={"Authorization":"Basic {0}".format(base64string), "User-Agent":taskSet.uaString, "IdentityProvider":taskSet.identityProvider})
	

def clearCart(taskSet):
	taskSet.client.delete("/cart", headers={"User-Agent":taskSet.uaString})

def addItemToCart(taskSet, item_id, quantity):
	taskSet.client.post("/cart", json={"id": item_id, "quantity": quantity}, headers={"User-Agent":taskSet.uaString})

def viewCart(taskSet):
	taskSet.client.get("/basket.html", headers={"User-Agent":taskSet.uaString})

def purchaseCart(taskSet):
	taskSet.client.post("/orders", headers={"User-Agent":taskSet.uaString})

def viewHomepage(taskSet):
	taskSet.client.get("/", headers={"User-Agent":taskSet.uaString})

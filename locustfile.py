import resource

from locust import HttpLocust, TaskSet, task
from locust.exception import StopLocust

import helpers.helpers as helpers
import helpers.siteInteractionHelpers as site
from fake_useragent import UserAgent

ua = UserAgent()

print "To avoid resource exhaustion, attempting to increase number of open files ulimit from {0} to (9999, 9999)".format(resource.getrlimit(resource.RLIMIT_NOFILE))
resource.setrlimit(resource.RLIMIT_NOFILE, (9999, 9999))
print "After ulimit update. Current ulimit values are {0}".format(resource.getrlimit(resource.RLIMIT_NOFILE))

class BaseTaskSet(TaskSet):
    uaString = ""

    def on_start(self):
        self.uaString = ua.random


#Task class for the casual browser
class CasualBrowserTasks(BaseTaskSet):
    @task(4)
    def taskFastBrowseAndLeave(self):
        site.viewHomepage(self)
        helpers.think(2, 5)
        site.viewCatalog(self)
        helpers.think(2, 5)

    @task(2)
    def taskThoroughBrowseAndLeave(self):
        site.viewHomepage(self)
        helpers.think(2, 5)
        site.viewCatalog(self)
        helpers.think(2, 5)
        site.applyFilter(self)
        helpers.think(2, 5)
        site.viewItemDetails(self, "03fef6ac-1896-4ce8-bd69-b798f85c6e0b")
        helpers.think(5, 10)
        site.viewCatalog(self)
        helpers.think(3, 10)

#Task class for the buyer
class BuyerTasks(BaseTaskSet):
    @task
    def taskBrowseAndBuy(self):
        item_id = "3395a43e-2d88-40de-b95f-e00e1502085b"

        site.viewHomepage(self)
        helpers.think(1, 3)
        site.login(self, "user", "password")
        helpers.think(1, 1)
        site.viewCatalog(self)
        helpers.think(2, 5)
        site.viewItemDetails(self, item_id)
        helpers.think(3, 6)
        site.clearCart(self)
        site.addItemToCart(self, item_id, 1)
        helpers.think(0.5, 1)
        site.viewCart(self)
        helpers.think(5, 8)
        site.purchaseCart(self)
        helpers.think(10, 20)
        

class CasualBrowser(HttpLocust):
    weight = 5
    task_set = CasualBrowserTasks
    min_wait = 1000
    max_wait = 1000

class Buyer(HttpLocust):
    weight = 2
    task_set = BuyerTasks
    min_wait = 1000
    max_wait = 1000

import falcon
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import sys

# import R's utility package
utils = rpackages.importr('utils')

# select a mirror for R packages
utils.chooseCRANmirror(ind=1) # select the first mirror in the list

'''
# R package names
packnames = ('blockTools')

# R vector of strings
from rpy2.robjects.vectors import StrVector

# Selectively install what needs to be install.
names_to_install = [x for packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    utils.install_packages(StrVector(names_to_install))
'''

# Finally, import BlockTools
bt = rpackages.importr('blockTools')

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DiagResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        
        out = robjects.r('''
                        seqout <- seqblock(query = FALSE, id.vars = "ID", id.vals = 1, exact.vars = "Party", exact.vals = "Dem", covar.vars = "age", covar.vals = 25, file.name = "sdata.RData")
                        seqout$x[seqout$x['ID'] == 1 , "Tr"]
                       ''')
            
        resp.body = str(out[0])

# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

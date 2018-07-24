import falcon
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import sys

# import R's utility package
utils = rpackages.importr('utils')

# select a mirror for R packages
utils.chooseCRANmirror(ind=1) # select the first mirror in the list

# Finally, import BlockTools
bt = rpackages.importr('blockTools')

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DiagResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        
        # capture each of the blocking vars
        cap_gender = req.params["gender"]
        cap_education = req.params["education"]
        cap_age = req.params["age"]
        cap_party = req.params["party"]
        
        py_exact_var = ["gender", "education", "age", "party"]
        py_exact_val = [cap_gender, cap_education, cap_age, cap_party]
        py_session = "sdata2.RData"
        
        resp.body = str(cap_gender)
        
# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

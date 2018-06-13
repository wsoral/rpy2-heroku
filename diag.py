import falcon
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import sys

# import R's utility package
utils = rpackages.importr('utils')
stats = rpackages.importr('stats')

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DiagResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        
        # start doing stuff here
        try:
            out = 't'
            resp.body = out
            
        # if it doesn't work, tell the user what's wrong
        except:
            resp.body = str(sys.exc_info())

        else:
            # I'll use this later
            resp.body = str('Something  went really wrong. Please email Diag at diag@uchicago.edu; he apparently messed something up.')
            
# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

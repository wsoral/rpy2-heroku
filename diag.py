import falcon
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robj

# import R's utility package
utils = rpackages.importr('utils')
bt = rpackages.importr('blockTools')


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DiagResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        out = str(robj.r('1+2+ nchar("opp")'))
        resp.body = out


# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

import falcon
# import rpy2's package module
# import rpy2.robjects.packages as rpackages
#
# # import R's utility package
# utils = rpackages.importr('utils')


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DiagResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = 'this is a test request'


# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

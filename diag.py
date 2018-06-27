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
        
        if req.params["party"] == "independent":
            robjects.r('''
                           f <- function(id, exact_var, exact_val, covar_var, covar_val, session) {
                            seqout <- seqblock(query = FALSE, id.vars = "ID", id.vals = id, exact.vars = exact_var, exact.vals = exact_val, covar.vars = covar_var, covar.vals = covar_val, file.name = session)
                            seqout$x[seqout$x['ID'] == 1 , "Tr"]
                            }
                           ''')

            r_f = robjects.r['f']
            out = r_f(1, "Party", "Dem", "Age", 9, "sdata.RData")
            resp.body = 'Treatment=' + str(out[0][-1])
            #resp.body = str(list(req.params.keys())[0])
        elif (req.params["party"] == "republican") | (req.params["party"] == "democrat"):
            resp.body = 'Treatment=' + "this"
        else:
            resp.body = 'Treatment=' + "fucked up"

# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

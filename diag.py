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
        
        if (req.params["party"] in  ["22", "14"]):
            robjects.r('''
                           f <- function(id, exact_var, exact_val, session) {
                            
                            seqout <- seqblock(query = FALSE
                                            , id.vars = "ID"
                                            , id.vals = id
                                            , n.tr = 4
                                            , tr.names = c("likert", "likertplus", "QV", "QVN")
                                            , assg.prob = c(2/7, 2/7, 2/7, 1/7)
                                            , exact.vars = exact_var
                                            , exact.vals = exact_val
                                            , file.name = session)
                            
                            seqout$x[seqout$x['ID'] == 1 , "Tr"]
                            }
                           ''')

            r_f = robjects.r['f']
            out = r_f(1, "Party", "Dem", py_session)
            resp.body = 'Treatment=' + str(out[0])
        elif (req.params["party"] == "other"):
            robjects.r('''
               f <- function(id, exact_var, exact_val, session) {

                seqout <- seqblock(query = FALSE
                                , id.vars = "ID"
                                , id.vals = id
                                , n.tr = 7
                                , tr.names = c("likert_C", "likert_T", "likertplus_C", "likertplus_T", "QV_C", "QV_T", "QVN")
                                , assg.prob = c(3/20, 3/20, 3/20, 3/20, 3/20, 3/20, 1/10)
                                , exact.vars = exact_var
                                , exact.vals = exact_val
                                , file.name = session)

                seqout$x[seqout$x['ID'] == 1 , "Tr"]
                }
               ''')

            r_f = robjects.r['f']
            out = r_f(1, "Party", "Dem", py_session)
            resp.body = 'Treatment=' + str(out[0])
        else:
            resp.body = 'Treatment=' + "fucked up" + req.params["party"]
        
# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())

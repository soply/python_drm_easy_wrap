"""
Python wrapper for using R model drm to fit drug response curves with LL4 or L4
model (see fitting.R)
"""
import math
import rpy2.robjects as ro

def python_drc_wrap(input,output):
    """
    Takes x,y data given by input and ouput and fits a LL4, or L4 (if LL4 didn't converge)
    model to the given data using the R model drm. Returns essential fit information in
    a python dict.

    input: python list
        Dose values as floats in a python list

    output: python list
        Response values as floats in a python list

    Returns python dictionary with the following entries
    ==========================================================
    fit_type: string ('L4' or 'LL4') depending on what model was used for fitting
    slope: float, slope fit parameter
    lowerlimit: float, lowerlimit fit parameter
    upperlimit: float, upperlimit fit parameter
    ic50: float, ic50 fit parameter
    n_samples: number of samples used in fit (equal to len(input))
    eval_f: number of evaluations of the function model
    eval_df: number of evaluations of the gradient of the function model
    converged: True if finding parameters has converged
    rse: root square error/residuals
    """
    r=ro.r
    r_input = ro.FloatVector(input)
    r_output = ro.FloatVector(output)
    r.source("fitting.R")
    r_return = r.curveFits(r_input,r_output)
    # Convert r output to python output
    p_return = {}
    try:
        p_return['fit_type'] = r_return.rx2['fit_type'][0]
        p_return['slope'] = r_return.rx2['coefficients'][0]
        p_return['lowerlimit'] = r_return.rx2['coefficients'][1]
        p_return['upperlimit'] = r_return.rx2['coefficients'][2]
        p_return['ic50'] = r_return.rx2['coefficients'][3]
        p_return['n_samples'] = r_return.rx2['sumList'][0][0]
        p_return['eval_f'] = r_return.rx2['fit'][2][0]
        p_return['eval_df'] = r_return.rx2['fit'][2][1]
        p_return['converged'] = r_return.rx2['fit'][3][0]
        p_return['rse'] = math.sqrt(r_return.rx2['fit'][1][0]) # Root squared error
    except:
        print("LL4 and L4 models could not been fitted, returning empty dict")
        p_return = {}
    return p_return

""" Example usage """
if __name__ == "__main__":
    r_return = python_drc_wrap([0.1, 1.0, 10.0, 100.0, 1000.0], [107, 104, 78, 58, 61])
    print(r_return)

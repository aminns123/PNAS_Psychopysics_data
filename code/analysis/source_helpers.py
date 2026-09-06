"""Function definitions extracted from supplied code; source lines in provenance.
No top-level analysis scripts are executed. Numerical bodies are preserved.
"""
import numpy as np
from numpy import real
from math import factorial
from itertools import combinations

# LIB001 source lines 513-523
def indexInListRemove(xAxis,yAxis,indexList):
    
    newX, newY = [], []
    for j in range(len(yAxis)):
        if j in indexList:
            pass
        elif j not in indexList: 
            newX.append(xAxis[j])
            newY.append(yAxis[j])
        
    return newX, newY

# LIB001 source lines 715-722
def findCorrespondingValue(xList, yList, findValue):
    xfit_max = 0
    for i in range(len(yList)):
        if yList[i] == findValue:
            xfit_max = xList[i]
        elif yList[i] == findValue:
            pass
    return xfit_max

# LIB001 source lines 4935-4975
def count_reversals_HighLow(contrastList):
    averageList = []
    TrialNumber = []
    countR      = 0
    checkSign   = 0
    signValue   = -1
    
    j           = 0
    
    if len(contrastList) > 1:
        if contrastList[j+1]-contrastList[j] < 0: # i.e. N12 - N10, then get  j-1
            signValue = -1
        elif contrastList[j+1]-contrastList[j] > 0: 
            signValue = 1
        elif contrastList[j+1]-contrastList[j] == 0: 
            pass
            
        checkSign = signValue
        j         = 0
        while j < len(contrastList)-2:
            j+=1
            if contrastList[j+1]-contrastList[j] < 0: # i.e. N12 - N10, then get  j-1
                signValue = -1
            elif contrastList[j+1]-contrastList[j] > 0: 
                signValue = 1
            elif contrastList[j+1]-contrastList[j] == 0: 
                pass
            
            if checkSign != signValue:
                checkSign = signValue 
                countR   += 1
                averageList.append(contrastList[j])
                TrialNumber.append(j)
            elif checkSign == signValue:
                pass
    elif len(contrastList) <= 1:
        TrialNumber=[1]
        TrialNumber=[0]
        averageList=[0] 
        
    return len(TrialNumber), TrialNumber, averageList

# LIB001 source lines 6564-6568
def makeList(xArray, func, **kwargs):
    newList = []
    for x in xArray:
        newList.append(func(x, **kwargs))
    return newList

# LIB001 source lines 7403-7406
def AoE(x, x0, x1, x2,x3):
    # a:x1 b:x0, f0:x3 , f1:x2
    X = x-x3
    return x0*np.exp(-(X))+(x1*np.exp(-pow((X)/x2,2)))

# LIB001 source lines 21338-21381
def goodnessFit_nrmse(x_original,y_original,x_fitted, y_fitted, rmseCHOICE = 'mean'):
    from scipy import interpolate

    # Interpolate fitted data to original x points
    interp_func     = interpolate.interp1d(x_fitted, y_fitted)#, kind='linear')
    y_fitted_interp = interp_func(x_original)
    
    rmse    = np.sqrt(np.mean((y_original - y_fitted_interp) ** 2))
    mae     = np.mean(np.abs(y_original - y_fitted_interp))
    
    # Normalization methods
    mean_y  = np.mean(y_original)
    range_y = np.max(y_original) - np.min(y_original)
    std_y   = np.std(y_original)

    # Use absolute mean for normalization
    nrmse_abs_mean  = rmse / abs(mean_y)
    nrmse_range     = rmse / range_y
    nrmse_std       = rmse / std_y
    nrmse           = rmse/np.mean(y_original)
    
    if rmseCHOICE == 'mean':
        outnrmse=nrmse
    elif rmseCHOICE == 'std':
        outnrmse=nrmse_std
    elif rmseCHOICE == 'range':
        outnrmse=nrmse_range
    elif rmseCHOICE == 'abs_mean':
        outnrmse=nrmse_abs_mean
    else:    
        outnrmse=nrmse
        
    mape    = np.mean(np.abs((y_original - y_fitted_interp) / y_original)) * 100

    # Now compute goodness of fit metrics
    goodnessFit_r2_score            = 0 # r2_score(y_original, y_fitted_interp)
    goodnessFit_mean_squared_error  = 0 # mean_squared_error(y_original, y_fitted_interp)
    goodnessFit_RMSE                = rmse 
    goodnessFit_mean_absolute_error = mae  
    
    chi2, p = 0,0 # chisquare(y_original, f_exp=y_fitted_interp)
    goodnessFit_chisquare           = [chi2, p]
    
    return outnrmse,mape,goodnessFit_RMSE,goodnessFit_mean_absolute_error

# LIB001 source lines 21385-21392
def getIndex_sortDataRegion(data,a,b):
    indexList   = []
    for i in range(len(data)): 
        if (data[i]>= a) and (data[i]<= b):   
            indexList.append(i)
        elif (data[i]< a) or (data[i]> b):   
            pass
    return indexList

# LIB001 source lines 21483-21495
def fit_to_CSF(xNew, yNew, fitFunction,guessParams, BoundsDW_CSF,BoundsUP_CSF, n_fittingTries, fitRULE):

    #xLimMax         = [min(xNew), max(xNew)+10]
    xLimMax         = [0.1, max(xNew)+10]

    xy3         = fitFunctionLimit(xLimMax, xNew, yNew,fitFunction, guessParams, BoundsDW_CSF,BoundsUP_CSF, fitRULE, n_fittingTries)
    xfit_list3  = xy3[0]
    yfit_list3  = xy3[1]   
    paramsFIT   = xy3[2]

    xMax        = findCorrespondingValue(xfit_list3, yfit_list3, max(yfit_list3))  
          
    return xfit_list3, yfit_list3, paramsFIT, xMax

# LIB001 source lines 21499-21522
def fitFunctionLimit(xLimMax,xdata, ydata,function_fit,guessParams, boundDW, boundUP, fitm, fitNumber=10_000):
    from scipy.optimize import curve_fit
    
    maxX, minX      =  xLimMax[1], xLimMax[0]
    xStep           = (maxX - minX)/1000
    xdataContinuous = list(np.arange(minX, maxX,xStep) )
    params_totalFit = {}
    #try:  # lm, trf, dogbox 
    # fitm = 'lm'
    Rss, Tss, Rsquared= 0,0,0     
    if len(guessParams) > 1 and len(boundUP) > 1: 
        popt, pcov    = curve_fit(function_fit, xdata, ydata,p0=guessParams,method=fitm, maxfev=fitNumber, bounds=(boundDW, boundUP)) ## 20_000
    elif len(guessParams) <=1 and len(boundUP) > 1:
        popt, pcov    = curve_fit(function_fit, xdata, ydata,method=fitm, maxfev=fitNumber, bounds=(boundDW, boundUP)) ## 20_000
    elif len(guessParams) <=1 and len(boundUP) <= 1:
        popt, pcov    = curve_fit(function_fit, xdata, ydata,method=fitm, maxfev=fitNumber) 
    #nan_policy='omit'    
    for indexKey in range(len(popt)):
        params_totalFit.update({'x'+str(indexKey):popt[indexKey]})
        
    fitfunction_array = makeList(xdataContinuous, function_fit, **params_totalFit)


    return xdataContinuous, fitfunction_array, params_totalFit, pcov

# LIB001 source lines 21716-21739
def fitFunction(xdata, ydata,function_fit,guessParams, boundDW, boundUP, fitm):
    from scipy.optimize import curve_fit
    
    maxX, minX      = max(xdata), min(xdata)
    xStep           = (maxX - minX)/1000
    xdataContinuous = list(np.arange(minX, maxX,xStep) )
    params_totalFit = {}
    #try:  # lm, trf, dogbox 
    # fitm = 'lm'
    Rss, Tss, Rsquared= 0,0,0     
    if len(guessParams) > 1 and len(boundUP) > 1: 
        popt, pcov    = curve_fit(function_fit, xdata, ydata,p0=guessParams,method=fitm,max_nfev=5000, maxfev=5000, bounds=(boundDW, boundUP)) ## 20_000, 100_000
    elif len(guessParams) <=1 and len(boundUP) > 1:
        popt, pcov    = curve_fit(function_fit, xdata, ydata,method=fitm,max_nfev=5000, maxfev=5000, bounds=(boundDW, boundUP)) ## 20_000
    elif len(guessParams) <=1 and len(boundUP) <= 1:
        popt, pcov    = curve_fit(function_fit, xdata, ydata,method=fitm,max_nfev=5000, maxfev=5000) 
    #nan_policy='omit'    
    for indexKey in range(len(popt)):
        params_totalFit.update({'x'+str(indexKey):popt[indexKey]})
        
    fitfunction_array = makeList(xdataContinuous, function_fit, **params_totalFit)


    return xdataContinuous, fitfunction_array, params_totalFit


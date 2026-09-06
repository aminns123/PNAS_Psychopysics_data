r"""Relevant source excerpts from SUP11, preserved as reference text only.
These are not an executable experiment driver.

Source lines 299-309:
    nRetreat         = 8 # 6, 8, 9
    bkg_crt          = kwargs_total['bkg_intensity']
    nTrial_Index     = 24
    NinBins =6
    
    step_w          = 1
    th_percent      = 0.8584 # 0.79
    bkg_contrast    = kwargs_total['bkg_intensity']
    max_contrast    = 1.00 
    step_weber      = 1#400  #1
    weberCrt        = 0.016 #0.01

Source lines 445-475:
        ADM_webFit_list.append(contrast_W_ADM)
        ADM_position_probe.append(data_ADM_full[0][1])
        ADM_frequency_probe.append(data_ADM_full[0][8])
         
        weberLIST_TH                   = funcs.weberContrast(contrastComb, bkg_contrast, max_contrast,logFunction, False)
        rev_COUNT, rev_LIST, rev_CONTR = funcs.count_reversals_HighLow(weberLIST_TH)
        thV, indexR, conrtR            = funcs.averageADM_TH_reversals_HighLow(weberLIST_TH,nRetreat) ## <- new code +1
        print('1: thV:', thV)
        ADM_Reverse_Count.append(rev_COUNT)
        ADM_Reverse_Index.append(rev_LIST)
        ADM_Reverse_Contr.append(rev_CONTR)
        
        # conrtR = rev_CONTR[len(rev_CONTR)-nRetreat:]
        # indexR = rev_LIST[len(rev_CONTR)-nRetreat:]
        #thV    = np.median(rev_CONTR[len(rev_CONTR)-nRetreat:])
        #nRetreat = len(rev_CONTR)-2
        conrtR = rev_CONTR[len(rev_CONTR)-nRetreat:]
        indexR = rev_LIST[len(rev_CONTR)-nRetreat:]
        
        thV_median  = np.median(rev_CONTR[len(rev_CONTR)-nRetreat:])
        thV_mean    = np.mean(rev_CONTR[len(rev_CONTR)-nRetreat:])
        
        print('2: thV:', thV)
        # nTrial_Index      = len(weberLIST_TH)-10
        zTH,indexZ,arrayZ = funcs.thresholdContrast_trialN_Indexed(weberLIST_TH, nTrial_Index, 'MEAN')
        
        ADM_IndexReversal_List.append(indexR)
        ADM_findReversal_List.append(conrtR)
        
        ADM_averageADM_TH_mean.append(thV_mean)
        ADM_averageADM_TH_median.append(thV_median)

Source lines 901-924:
listTH_THC = [listTH_mean, listTH_median]
colourFit  = ['red', 'dodgerblue', 'purple']
labelList  = [r'$\mu$ ',r'Mdn ']
if (experimentNAME == 'Indirect_Flanker_Experiment')  or (experimentNAME == 'Base_Experiment'):
    pass
elif experimentNAME == 'Flanker_Selectivity_Experiment' and experimentNAME != 'Line_Flicker_Experiment':
    if logStatement == False:
        fig, axs    = plt.subplots(figsize=(10, 10))  
        axs.set_title(ExperimnetTYPE+'\n #R-median(P)_mean(G)') 
        #for i in range(len(sampleDict['ADM_averageADM_TH'])):
                
        #    axs.scatter(round((conditionList[i]/40)*1.2,3),1.0/sampleDict['ADM_averageADM_TH'][i], c='cyan', alpha = 0.5)    
        for z in range(len(listTH_THC)):
            listTH = listTH_THC[z]
            listX=[]
            listY=[]
            for j in range(len(arrayPOS)):
                for n in range(len(listTH[j])):
                    axs.scatter(round((arrayPOS[j]/deg1PCD),3),1.0/listTH[j][n], c='grey', alpha = 0.5)
                axs.scatter(round((arrayPOS[j]/deg1PCD),3),1.0/np.median(listTH[j]), c='purple', alpha = 1)
                axs.scatter(round((arrayPOS[j]/deg1PCD),3),1.0/np.mean(listTH[j]), c='green', alpha = 1)
                listX.append(round((arrayPOS[j]/deg1PCD),3))
                listY.append(1.0/np.mean(listTH[j]))
            axs.set_ylabel('Contrast sensetivity', fontsize =20)

"""

"""Reference only: original plotting functions; see model limitations.
Private path comments removed. Use the packaged replay scripts for execution.
"""
def plot_PSF_Pars_latex(kwargs):
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib.gridspec as gridspec 
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    from matplotlib.ticker import ScalarFormatter
    import matplotlib.patches as patches
    
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['pdf.fonttype'] = 42
    
    ### ==== ####
    
    xData_isf,yData_isf=kwargs['xData1'],kwargs['yData1']
    xData_csf,yData_csf=kwargs['xData2'],kwargs['yData2']

    xData_isf_fit = kwargs['xData1_fit']
    yData_isf_fit = kwargs['yData1_fit']
    
    errorBarsUP = kwargs['errorBarsUP']
    errorBarsDW = kwargs['errorBarsDW']
    medianBar   = kwargs['medianBar']
    first_FitCSF= kwargs['first_FitCSF']
    nreversals  = kwargs['nreversals']
    
    xData_csf_fit_a = kwargs['xData2_fit_a']
    yData_csf_fit_a = kwargs['yData2_fit_a']
    
    xData_csf_fit_b = kwargs['xData2_fit_b']
    yData_csf_fit_b = kwargs['yData2_fit_b']
    
    xData_csf_fit_c = kwargs['xData2_fit_c']
    yData_csf_fit_c = kwargs['yData2_fit_c']
    
    xlist_ticks_isf = kwargs['xdata1_ticks']
    ylist_ticks_isf = kwargs['ydata1_ticks']
    
    xlist_ticks_csf = kwargs['xdata2_ticks']
    ylist_ticks_csf = kwargs['ydata2_ticks']
    
    listTitle_ISF   = kwargs['data1_title']
    listTitle_CSF   = kwargs['data2_title']
    
    xLabelData1 = kwargs['data1_xlabel']
    yLabelData1 = kwargs['data1_ylabel']
    
    xLabelData2 = kwargs['data2_xlabel']
    yLabelData2 = kwargs['data2_ylabel']
    
    nRows       = kwargs['nRows']
    nCols       = kwargs['nCols']
    Participants= kwargs['Participants']
    
    ylim_subject    = kwargs['ylim']
    listColour      = kwargs['colours']
    listFuncs       = kwargs['fittedFuncs']
    listPars        = kwargs['participantPlot']
    ### === ###
    #markList = ['o', 'D', 'o', '^', 's']
    markList = ['s', 's', 's', 's', 's']

    rows, cols      = 1, 1
    fig, aXs        = plt.subplots(rows, cols,figsize=(8, 24), sharex=False,sharey=False)  
    #fig.patch.set_facecolor('0.9')  # light grey

    aXs.axis("off")
    
    # Define frame positions for each column (covering both rows)

    
    frame_positions = [(0.03, 0.01, 0.47,  0.98),
                        #(0.54, 0.02, 0.42,  0.94)
                        ] 
                      
    """
    for (x, y, w, h) in frame_positions:
        colourCount+=1
        frame = patches.FancyBboxPatch(
            (x, y), w, h, transform=fig.transFigure,  
            boxstyle="round,pad=0.00", linewidth=0.5, edgecolor="black", 
            linestyle='solid',
            facecolor='none', zorder=0  # Keep behind subplots, whitesmoke
        )
        fig.patches.append(frame)
    
    gridR, gridC    = rows*nRows, cols*nCols
    listc = [1 for x in range(gridC)]
    listr = [1 for x in range(gridR)]
    """
    
    # Outer grid: 2 rows (top half, bottom half), 2 columns of block groups
    figure_gs = fig.add_gridspec(4, 1, hspace=0.0, wspace=0.0) # , height_ratios=[1, 1]
    

    gs_PSF = figure_gs[:].subgridspec(3, 1, hspace=0.15, wspace=0.3)
    

    dictPotsCSF = ({})
    
    dictPotsCSF.update({
                        
                        'B0':fig.add_subplot(gs_PSF[0],zorder=1),
                        'B1':fig.add_subplot(gs_PSF[1],zorder=1),
                        'B2':fig.add_subplot(gs_PSF[2],zorder=1),
                        #'B3':fig.add_subplot(gs_PSF[3],zorder=1),
                        })
    
    """    
    top=0.97,
    bottom=0.0,
    left=0.135,
    right=1.0,
    hspace=0.2,
    wspace=0.2
    """
    fig.subplots_adjust(
    top=0.995,
    bottom=0.065,
    left=0.17,
    right=0.795,
    hspace=0.2,
    wspace=0.2
    )
    fig.canvas.draw()

    
    countx=-1
    j     = 0
    ynow  = 0
    listax1 = ['A0','A1','A2','A3','A4','A5']
    listax2 = ['B0','B1','B2','B3']
    
    # ---- SHIFT ONLY THE LEFT COLUMN (gs_CSF) DOWN ----
    shift = 0.02   # adjust this value (0.01 to 0.10 is typical)

    """
    keys_A = ['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11']
    rows   = [keys_A[i:i+2] for i in range(0, len(keys_A), 2)]  # 6 rows

    new_top, new_bottom = 0.88, 0.12  # compressed vertical region
    n_rows = len(rows)
    new_centers = np.linspace(new_top, new_bottom, n_rows)

    for (row_keys, cy_new) in zip(rows, new_centers):
        for key in row_keys:
            ax  = dictPotsCSF[key]
            box = ax.get_position()
            h   = box.height
            new_y0 = cy_new - h/2
            ax.set_position([box.x0, new_y0, box.width, h])
    """    
    scaleft = ScalarFormatter()
    scaleft.set_useOffset(1)
    
    list_subplots = ['A','B','C','D', 'E', 'F', 'G','H','I','J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

    list_subplots2 = ['J', 'K', 'L', 'M', 'N']

    
    cordCount=-1
    xLENGTH = np.log10(500-5)
    #xMove    =[0.63, 0.79, 0.88] # par1

    xMove    =[0.61, 0.705, 0.77] # par4

    #xMove    =[np.log10(100)/xLENGTH, np.log10(204)/xLENGTH, np.log10(300)/xLENGTH]

    yMove    =[1.0, 1.0, 1.0]
    
    xyPrev = [[0.45, -0.2],[0.7, -0.2],[-0.05, 0.0]]
    
    coord2list = [[100, 10], [204, 10], [300, 10]]

    
    axCount=-1
    
    listLb_pars = []
    listPSF_pars= []
    
    countx = -1
    for y in listPars[1:]: # i.e. 1: participant ...
        axCount += 1
        ax2      = dictPotsCSF[listax2[axCount]]

        countx+=1


        list_psf = []
        list_lb  = []
        for x in range(len(xData_csf[y])): 
            
            #DoEx, DoEy   = xData_csf_fit_a[y][x],yData_csf_fit_a[y][x]
            #listSF,listS = xData_csf[y][x],yData_csf[y][x]
            xMax         = findCorrespondingValue(xData_csf_fit_a[y][x],yData_csf_fit_a[y][x],max(yData_csf_fit_a[y][x]))
            
            ## == ##
            list_psf.append(xMax)
            list_lb.append(float(listTitle_CSF[y][x]))
        

        ax2.annotate(
                'S'+str(axCount+2)+'',
                xy=(0.0, 0.125), xycoords='axes fraction',
                xytext=(+0.5, -0.5), textcoords='offset fontsize',
                fontsize=20, verticalalignment='top', fontfamily='serif',
                rotation=0,
                bbox=dict(facecolor='none', edgecolor='none', pad=3.0))
       
        ax2.annotate(
            ' '+list_subplots[countx]+' ',
            xy=(-0.2, 1.05), xycoords='axes fraction',
            xytext=(+0.5, -0.5), textcoords='offset fontsize',
            fontsize=22, verticalalignment='top', fontfamily='serif',
            rotation=0,
            bbox=dict(facecolor='none', edgecolor='none', pad=3.0))
       
        #ax2.plot(list_lb,list_psf,c=listColour[y],linestyle='solid',alpha=0.5,label='PSF')#r'Prefered'+' '+r'spatial frequency')
        #ax2.scatter(list_lb,list_psf,c='red',s=40,alpha=1)
        
        lolims = errorBarsDW[y]
        uplims = errorBarsUP[y]
        error  = 0.1

        #ax2.plot(list_lb,medianBar[y], c=listColour[y])
        ax2.scatter(list_lb,medianBar[y],c=listColour[y], marker=markList[y],s=90,alpha=1, zorder=20, edgecolors='black')
        #ax2.scatter(list_lb,first_FitCSF[y],c='black', marker='o',s=50,alpha=1, zorder=20, edgecolors='black', label='R'+str(nreversals))

        """
        if axCount == 0:
            for j in range(6, 9, 1):
                #ax2.scatter(list_lb[j],list_psf[j],c='black',s=160,alpha=0.3)
                ax2.vlines(x=list_lb[j], ymin=medianBar[y][j]+0.5+uplims[j], ymax=14, color='black', linestyle='dotted', linewidth=0.8)
        """  
        list_short_psf = [] 
        for j in range(0, len(list_psf), 1):
            yCentre = medianBar[y][j] # list_psf[j]
            list_short_psf.append(yCentre)
            ax2.vlines(x=list_lb[j], ymin=lolims[j], ymax=uplims[j], color=listColour[y], linestyle='solid', linewidth=1.0)
            ax2.scatter(list_lb[j],uplims[j], marker='_',c=listColour[y],s=80,alpha=1)
            ax2.scatter(list_lb[j],lolims[j], marker='_',c=listColour[y],s=80,alpha=1)
            
        minY = int(min(list_psf)-1)
        maxY = int(max(list_psf)+2)
        ax2.set_ylim(minY,14)
        """
        if maxY < 12:
            ax2.set_ylim(minY,14) #maxY)
        else:
            ax2.set_ylim(minY,maxY)
        """
        
        if axCount in [1]:
            ax2.set_ylabel("Peak spatial "+""+" frequency (cpd)",rotation=90, fontsize=18,labelpad=30)#, y=-0.3)
        
        if axCount in [len(dictPotsCSF.keys())-1]:
            ax2.set_xlabel(r'Average background luminance (cd/m$^2$)',fontsize=18, rotation=0,labelpad=8)#, x=0.55)            
        
        ax2.tick_params(which='major', width=1.5, length=7,labelsize=12)


        ax2.set_xlim(5, 500)
        ax2.set_xscale("log", base=10) 
        ax2.set_xticks([10,100, 500])
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        #ax2.legend( loc='lower center', fontsize=12,ncol=1, facecolor='white',edgecolor='black')
        listLb_pars.append(list_lb)
        listPSF_pars.append(list_short_psf)
        
        
        # --- fit model isf ---
        fitFind_Function_k = model_EI_fn # model_EI_SF 
        # model_EI_SF_reduced# model_EI_SF 
        
        indexListRemove = [[7,9],[],[4,6],[],[]]
        for listSF in [[list_lb, list_psf]]:
            xNewn, yNewn = listSF[0],listSF[1]
            xNew, yNew   = indexInListRemove(xNewn, yNewn, indexListRemove[axCount+1]) 
            
            guessParams_k, boundDW_k, boundUP_k = [],[],[]
            
            """
            model_EI_SF(x, x0, x1, x2, x3, x4, x5,x6,x7,x8,x9,x10,x11):
            wEE       = x0
            wEI       = x1
            wIE       = x2
            wII       = x3
            
            wEe       = x4
            wEi       = x5
            wIe       = x6
            wIi       = x7
           
            alpha     = x8
            rI0       = x9
            rE0       = x10
            """
            
            wEi   = 2.76
            wIE   = 7.05 # 7.05
            alPha = 0.99 # 0.99
            #     # [x0 , x1    , x2  ,   x3,     x4,   x5  ,  x6  ,  x7]
            #p0_kp=[ 4.3, 6.47, 0.85, 0.86, 0.96]
            if y==0:
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, wEi, 0.84, 2.63, alPha+0.01, 0.79, 0.92]   #  <---
                #p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2, alPha, 0.79, 0.92] 
            elif y==1:
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2.63, alPha+0.01, 0.79, 0.92]   #  <---
                #p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2, alPha, 0.79, 0.92]  
            elif y == 4:
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2.63, alPha, 0.79, 0.92] # par4
            elif y==3:
                xNew.extend([500,600, 900]), yNew.extend([yNewn[-1],yNewn[-1],yNewn[-1]])
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2.63, alPha+0.01, 0.79, 0.92]  #  <---
                #p0_kp=[1.0, 0.41, 6.99, 1.73, 1.0, 2.71, 1.06, 2.88, 1.0, 0.88, 0.95]
                #p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2, alPha, 0.79, 0.92]  
            
            
            
            wEE = 6.0 # increase -> shift "jump" backwards.
            wEe = 6.4 # decrease value -> stabillity later on for greater x axis
            wEI = 14.0 # Increase --> shoves down rE0 vs Lb 
            wEi = 100 # Increase <-- shifts "jump" back for increasing value (keeps total length)
            wIE = 12.0 # Increase <---  shifts "jump" back  (moves entire length)
            wIe = 3.6 # Increase <--- shoves rE0 vs Lb down
            wII = 500.0 ## 22.6 #<-- stabalises all kn curves (does not let kn shoot to 1000s)
            wIi = 1.0 # increase <--- rE0 vs Lb more curve ( if descrease -> creates kink/knee)  

            #weights = [wEE, wEe, wEI, wEi,wIE,wIe,wII,wIi]
            #weights.extend([0.98, 1.0, 1.0])
            weights = [0.99, 0.54, 7.02, 2.14, 0.88, 2.75, 0.84, 2.63, 1.0, 0.78, 0.92]
            
            xFit = np.linspace(5,500, 1000)
            #ax2.plot(xFit,fitFind_Function_k(xFit,*weights),alpha=1,linestyle='dashed',linewidth=1.0,c='black')
            maxW=10
            #
            guessParams_k   = p0_kp
            boundDW_k       = [  0.0,0.0,   0  ,0,0,0.0,0.0,0,0.9,0,0]
            boundUP_k       = [  1,  maxW, maxW,  3, 1,  maxW, 3,3,1,1,1]
            
            #try:
            colorm = ['red', 'blue']
            countm =-1
            for fitm in ['trf']:#, 'dogbox']:
                countm+=1
                xy          = fitFunctionLimit([1, 1_000], xNew, yNew, fitFind_Function_k, guessParams_k, boundDW_k, boundUP_k, fitm, 5_000_000)
                xFit        = xy[0]
                yFit        = xy[1]
                yParam      = xy[2]
                pcov        = xy[3]
                if countx < 1:
                    ax2.plot(xFit,yFit,alpha=1,linestyle='solid',linewidth=1.0,c='forestgreen', label=r'Intrinsic SF')
                else:
                    ax2.plot(xFit,yFit,alpha=1,linestyle='solid',linewidth=1.0,c='forestgreen')

                listRound = [round(elem.astype(float),2) for elem in list(yParam.values())]
                #print('listRound', listRound)
                print(fitm+' par:'+str(y)+' (yParam.values-PSF) \n ', np.array(listRound).tolist())#.astype(float))
                
                #wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.1, 0.1, 1.2, 18.3, 9.3,1.77, 50, 1.66, 0.75
                
                # wEE, wEI, wIE, wII : 4.5, 6.9, 28.4, 64.5
                # wEe, wEi, wIe, wIi : 0.5, 10.5, 14.9, 3.0
                if y==1:
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.4 ,  0.8 ,  22.4,  3.9  ,7.4  ,2.8,  42.5  ,1.4,  0.67 # par 1
                    [wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha] = [
                                0.32003916328219695 ,
                                0.715921029304315 ,
                                22.21051367834623 ,
                                4.679936898718579 ,
                                8.879958591521905 ,
                                2.7164184598713987 ,
                                51.0 ,
                                1.6799643300873932 ,
                                0.6506055004303203 ,
                                ]# par 1
                elif y==3:
                    #wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 23 , 0.11 , 52.2 , 9.1, 16.2, 19.2, 90.3,  4 , 0.87 # par 3
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.8 ,  0.8 ,  28,  3.9  ,7.4  ,2.8,  42.5  ,2,  0.67
                elif y==4:
                    #(wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha) = (6.8  , 0.09 , 10.4 , 9.10, 7.3, 19.2, 68.6,  2.50 , 0.74) # par 4
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.4 ,  0.8 ,  24,  3.9  ,7.4  ,2.8,  42.5  ,1.4,  0.67
                    [wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha] = [
                                0.44337839559557307 ,
                               0.7748562874958744 ,
                               29.55207279916166 ,
                               6.257549814840517 ,
                               9.886334434742476 ,
                               4.648267054008116 ,
                               73.44 ,
                               2.417966477726506 ,
                               0.6780964711047098 ,
                                ]# par 4
                elif y==0:
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.8 ,  0.8 ,  22.4,  3.9  ,7.4  ,2.8,  42.5  ,0.9,  0.67 # par 0
                else:
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 4.5,  0.5,6.9,     10.5, 28.4,  14.9,64.5,  3.0,  0.92

                params = [wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha]
                xFit   = np.linspace(0, 40, 1_000)
                scaled_xaxis, y_predict = model_psf_function(params, xFit)
                if countx < 1:
                    ax2.plot(scaled_xaxis, y_predict,alpha=1,linestyle='solid',linewidth=1.0,c='black', label=r'Resonance SF')
                else:
                    ax2.plot(scaled_xaxis, y_predict,alpha=1,linestyle='solid',linewidth=1.0,c='black')
            #except:
            #    print('no fit found')
            #    pass
            #else:
            #    print('no fit found')
            #    pass
            
            
        minY = int(min(list_psf)-1)
        maxY = int(max(list_psf)+2)
        ax2.set_ylim(0,12)
        ax2.set_yticks([2,4,6,8,10])


        ax2.tick_params(axis='both', which='major', width=1.5,labelsize=12, length=7)
        ax2.set_xlim(1, 1000)#505
        ax2.set_xscale("log", base=10) 
        ax2.set_xticks([1, 10,100, 1000])
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        #ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("left")
        ax2.set_box_aspect(1)
        
        
        ax2.legend(loc='upper center', bbox_to_anchor=(0.35, 0.9),
                  ncol=1, fancybox=False, shadow=False, fontsize=18, edgecolor='none')
        

    plt.show() 
    #fig.savefig(folder+"portrait_CSF_PSF.png", dpi=300)
    
    return listLb_pars, listPSF_pars






def plot_csf_portrait_onePar(kwargs):
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib.gridspec as gridspec 
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    from matplotlib.ticker import ScalarFormatter
    import matplotlib.patches as patches
    
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['pdf.fonttype'] = 42
    
    
    ### ==== ####
    
    xData_isf,yData_isf=kwargs['xData1'],kwargs['yData1']
    xData_csf,yData_csf=kwargs['xData2'],kwargs['yData2']

    xData_isf_fit = kwargs['xData1_fit']
    yData_isf_fit = kwargs['yData1_fit']
    
    errorBarsUP = kwargs['errorBarsUP']
    errorBarsDW = kwargs['errorBarsDW']
    medianBar   = kwargs['medianBar']
    first_FitCSF= kwargs['first_FitCSF']
    nreversals  = kwargs['nreversals']
    
    xData_csf_fit_a = kwargs['xData2_fit_a']
    yData_csf_fit_a = kwargs['yData2_fit_a']
    
    xData_csf_fit_b = kwargs['xData2_fit_b']
    yData_csf_fit_b = kwargs['yData2_fit_b']
    
    xData_csf_fit_c = kwargs['xData2_fit_c']
    yData_csf_fit_c = kwargs['yData2_fit_c']
    
    xlist_ticks_isf = kwargs['xdata1_ticks']
    ylist_ticks_isf = kwargs['ydata1_ticks']
    
    xlist_ticks_csf = kwargs['xdata2_ticks']
    ylist_ticks_csf = kwargs['ydata2_ticks']
    
    listTitle_ISF   = kwargs['data1_title']
    listTitle_CSF   = kwargs['data2_title']
    
    xLabelData1 = kwargs['data1_xlabel']
    yLabelData1 = kwargs['data1_ylabel']
    
    xLabelData2 = kwargs['data2_xlabel']
    yLabelData2 = kwargs['data2_ylabel']
    
    nRows       = kwargs['nRows']
    nCols       = kwargs['nCols']
    Participants= kwargs['Participants']
    
    ylim_subject    = kwargs['ylim']
    listColour      = kwargs['colours']
    listFuncs       = kwargs['fittedFuncs']
    listPars        = kwargs['participantPlot']
    
    ### === ###
    markList = ['s','o', 'D', 'o', '^', 's']

    rows, cols      = 1, 1
    fig, aXs        = plt.subplots(rows, cols,figsize=(19, 19), sharex=False,sharey=False)  
    #fig.patch.set_facecolor('0.9')  # light grey

    aXs.axis("off")
    
    # Define frame positions for each column (covering both rows)

    
    frame_positions = [(0.03, 0.01, 0.47,  0.98),
                        #(0.54, 0.02, 0.42,  0.94)
                        ] 
                      
    """
    for (x, y, w, h) in frame_positions:
        colourCount+=1
        frame = patches.FancyBboxPatch(
            (x, y), w, h, transform=fig.transFigure,  
            boxstyle="round,pad=0.00", linewidth=0.5, edgecolor="black", 
            linestyle='solid',
            facecolor='none', zorder=0  # Keep behind subplots, whitesmoke
        )
        fig.patches.append(frame)
    
    gridR, gridC    = rows*nRows, cols*nCols
    listc = [1 for x in range(gridC)]
    listr = [1 for x in range(gridR)]
    """
    
    # Outer grid: 2 rows (top half, bottom half), 2 columns of block groups
    figure_gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3) # , height_ratios=[1, 1]
    
    
    gs_CSFa    = figure_gs[:,:].subgridspec(4, 4, hspace=0.3, wspace=0.3)
    #gs_CSFb    = figure_gs[0,1].subgridspec(2, 2, hspace=0.3, wspace=0.3)
    #gs_CSFc    = figure_gs[:,0].subgridspec(4, 2, hspace=0.3, wspace=0.3)

    gs_PSF = figure_gs[1,1].subgridspec(1, 1)#, hspace=0.0, wspace=0.0)
    

    dictPotsCSF = ({})
    
    dictPotsCSF.update({'A0':fig.add_subplot(gs_CSFa[0, 0],zorder=1),
                        'A1':fig.add_subplot(gs_CSFa[0, 1],zorder=1),
                        'A2':fig.add_subplot(gs_CSFa[0, 2],zorder=1),
                        'A3':fig.add_subplot(gs_CSFa[0, 3],zorder=1),
                        
                        'A4':fig.add_subplot(gs_CSFa[1, 0],zorder=1),
                        'A5':fig.add_subplot(gs_CSFa[1, 1],zorder=1),
                        'A6':fig.add_subplot(gs_CSFa[1, 2],zorder=1),
                        'A7':fig.add_subplot(gs_CSFa[1, 3],zorder=1),
                        
                        'A8':fig.add_subplot(gs_CSFa[2, 0],zorder=1),
                        'A9':fig.add_subplot(gs_CSFa[2, 1],zorder=1),
                        'A10':fig.add_subplot(gs_CSFa[3,0],zorder=1),
                        'A11':fig.add_subplot(gs_CSFa[3,1],zorder=1),
                        
                        'B0':fig.add_subplot(gs_PSF[0],zorder=1),

                        })
    
    fig.subplots_adjust(  
    top=0.95,
    bottom=0.085,
    left=0.105,
    right=0.93,
    hspace=0.2,
    wspace=0.2
    )
    fig.canvas.draw()

    
    countx=-1
    j     = 0
    ynow  = 0
    listax1 = ['A0','A1','A2','A3','A4','A5']
    listax2 = ['B0','C0','C1','C2']
    
    # ---- SHIFT ONLY THE LEFT COLUMN (gs_CSF) DOWN ----

    
    ax  = dictPotsCSF['B0']
    box = ax.get_position()
    h   = box.height+0.03
    dxShift = 0.03
    w   = box.width+dxShift
    ax.set_position([box.x0-dxShift, box.y0, w, h])
        
    scaleft = ScalarFormatter()
    scaleft.set_useOffset(1)
    #'A','B',
    list_subplots = ['C','D', 'E', 'F', 'G','H','I','J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

    list_subplots2 = ['J', 'K', 'L', 'M', 'N']

    
    cordCount=-1
    xLENGTH = np.log10(500-5)
    #xMove    =[0.63, 0.79, 0.88] # par1

    xMove    =[0.61, 0.705, 0.77] # par4

    #xMove    =[np.log10(100)/xLENGTH, np.log10(204)/xLENGTH, np.log10(300)/xLENGTH]

    yMove    =[1.0, 1.0, 1.0]
    
    xyPrev = [[0.45, -0.2],[0.7, -0.2],[-0.05, 0.0]]
    
    coord2list = [[100, 10], [204, 10], [300, 10]]
    """
    for axSTR in ['A0', 'A1','A2']:
        cordCount+=1
        
        transFigure = fig.transFigure.inverted()
        coord1 = transFigure.transform(dictPotsCSF[axSTR].transData.transform(xyPrev[cordCount] ))
        coord2 = transFigure.transform(dictPotsCSF['B0'].transData.transform( [xMove[cordCount], 0.0+yMove[cordCount]]))
        arrow = patches.FancyArrowPatch(
            coord1,  # posA
            coord2,  # posB
            shrinkA=0,  # so tail is exactly on posA (default shrink is 2)
            shrinkB=0,  # so head is exactly on posB (default shrink is 2)
            transform=fig.transFigure,
            color="black",
            arrowstyle="-",  # "normal" arrow
            linestyle='dotted',
            mutation_scale=10,  # controls arrow head size
            linewidth=0.5,
            zorder=0,
        )
        fig.patches.append(arrow)
    
    """
    
    for y in [listPars[0]]: # i.e. participant ...

        for x in range(len(xData_csf[y])):
            countx+=1
            
            DoEx, DoEy   = xData_csf_fit_a[y][x],yData_csf_fit_a[y][x]
            listSF,listS = xData_csf[y][x],yData_csf[y][x]
            xMax         = findCorrespondingValue(DoEx, DoEy, max(DoEy))
            
            ax1=dictPotsCSF['A'+str(x)]
            ax1.axvline(xMax,linestyle='solid',c='navy',linewidth=0.5, label=str(np.round(xMax,2)))
            #ax1.set_title(r'  $L_b$: '+str(listTitle_CSF[y][x])+r' $cd/m^2$',fontsize=12,loc='right')
            ax1.plot(DoEx,DoEy,c=listColour[y],alpha=1.0,linestyle='solid', linewidth=0.5)
            ax1.scatter(xData_csf[y][x],yData_csf[y][x],c=listColour[y],edgecolor='black', marker=markList[y],s=70,alpha=1, zorder=20) # ,edgecolors='black'

                        
            ## == ##
            if countx == 0:
                ax1.annotate(
                'D'+str(countx+1)+'',
                xy=(0.0, 1.0), xycoords='axes fraction',
                xytext=(+0.5, -0.5), textcoords='offset fontsize',
                fontsize=18, verticalalignment='top', fontfamily='serif',
                rotation=0,
                zorder=0,
                bbox=dict(facecolor='white', edgecolor='none', pad=3.0))
            else:
                ax1.annotate(
                'D'+str(countx+1)+'',
                xy=(0.0, 1.0), xycoords='axes fraction',
                xytext=(+0.5, -0.5), textcoords='offset fontsize',
                fontsize=18, verticalalignment='top', fontfamily='serif',
                rotation=0,
                zorder=0,
                bbox=dict(facecolor='white', edgecolor='none', pad=3.0))
            
            
            ax1.tick_params(which='major', width=1.5, length=7)
            ax1.set_xlim(0.1, 100)
            ax1.set_ylim(ylim_subject[y][1], 1000)#ylim_subject[y][0])

            ax1.set_yscale("log", base=10) 
            ax1.set_xscale("log", base=10) 
            ax1.set_title(str(listTitle_CSF[y][x])+r' cd/m$^2$',fontsize=16,loc='right')

            if ('A'+str(x) in ['A10']):
                ax1.set_xlabel(xLabelData2,fontsize=18, x=1.25, labelpad=12)#y=-1.0)
            elif ('A'+str(x) not in ['A9']):
                #ax1.set_xlabel(xLabelData2, loc='left',fontsize=9)
                ax1.set_xlabel('')
            
            if countx < 10:
                ax1.set_xticks([1, 10, 100])
                ax1.tick_params(labelbottom=False)  # hides x tick labels only
            else:
                ax1.set_xticks([1,10,100])
            
            ax1.set_yticklabels([]) 
            ax1.set_yticks(ylist_ticks_csf[y])
            if ('A'+str(x) in ['A0','A4','A8','A10']):
                ax1.set_ylabel(yLabelData2, fontsize=18, labelpad=16)#, y=1.0
            else:
                pass
            
            if ('A'+str(x) not in ['A0','A4','A8','A10']):
                ax1.tick_params(labelleft=False)
            
                
            ax1.yaxis.set_major_formatter(scaleft)
            ax1.xaxis.set_major_formatter(scaleft)
            ax1.tick_params(which='major', width=1.5, length=7,labelsize=12)

            #legend = ax1.legend( loc='lower left', fontsize=8,ncol=1, facecolor='white',edgecolor='black')
            # bbox_to_anchor=(0.5, 0.5, 0.5, 0.5)
            ax1.annotate("", xy=(1.0, -2.0), xytext=(0.5, 0.0),
                    textcoords='axes fraction', arrowprops=dict(arrowstyle="->", color='black', lw=2),
                    ha='center', va='center', fontsize=12)
            
            ax1.tick_params(axis='both', which='major', width=1.5,labelsize=12, length=7)
            

    """
    ax1.annotate(
                ' Preferred spatial frequency ',
                xy=(-0.1, 1.55), xycoords='axes fraction',
                xytext=(+0.5, -0.5), textcoords='offset fontsize',
                fontsize=18, verticalalignment='top', fontfamily='serif',
                rotation= 0,
                bbox=dict(facecolor='whitesmoke', edgecolor='black', pad=3.0))
    """
    
    axCount=-1
    
    listLb_pars = []
    listPSF_pars= []
    
    countx = 0
    for y in [listPars[0]]: # i.e. participant ...
        axCount += 1
        ax2      = dictPotsCSF[listax2[axCount]]

        countx+=1


        list_psf = []
        list_lb  = []
        for x in range(len(xData_csf[y])): 
            
            #DoEx, DoEy   = xData_csf_fit_a[y][x],yData_csf_fit_a[y][x]
            #listSF,listS = xData_csf[y][x],yData_csf[y][x]
            xMax         = findCorrespondingValue(xData_csf_fit_a[y][x],yData_csf_fit_a[y][x],max(yData_csf_fit_a[y][x]))
            
            ## == ##
            list_psf.append(xMax)
            list_lb.append(float(listTitle_CSF[y][x]))
        

        ax2.annotate(
                'S'+str(axCount+1)+'',
                xy=(0.0, 0.1), xycoords='axes fraction',
                xytext=(+0.5, -0.5), textcoords='offset fontsize',
                fontsize=20, verticalalignment='top', fontfamily='serif',
                rotation=0,
                bbox=dict(facecolor='none', edgecolor='none', pad=3.0))
        """
        ax2.annotate(
            ' E ',
            xy=(0.0, 1.0), xycoords='axes fraction',
            xytext=(+0.5, -0.5), textcoords='offset fontsize',
            fontsize=18, verticalalignment='top', fontfamily='serif',
            rotation=0,
            bbox=dict(facecolor='white', edgecolor='none', pad=3.0))
        """
        
        #ax2.plot(list_lb,list_psf,c=listColour[y],linestyle='solid',alpha=0.5,label='PSF')#r'Prefered'+' '+r'spatial frequency')
        #ax2.scatter(list_lb,list_psf,c='red',s=40,alpha=1)
        
        lolims = errorBarsDW[y]
        uplims = errorBarsUP[y]
        error  = 0.1

        ax2.scatter(list_lb,medianBar[y],c=listColour[y], marker=markList[y],s=90,alpha=1, zorder=20, edgecolors='black')
        #ax2.scatter(list_lb,first_FitCSF[y],c='black', marker='o',s=50,alpha=1, zorder=20, edgecolors='black', label='R'+str(nreversals))

        """
        if axCount == 0:
            for j in range(6, 9, 1):
                #ax2.scatter(list_lb[j],list_psf[j],c='black',s=160,alpha=0.3)
                ax2.vlines(x=list_lb[j], ymin=medianBar[y][j]+0.5+uplims[j], ymax=14, color='black', linestyle='dotted', linewidth=0.8)
        """  
        list_short_psf = [] 
        for j in range(0, len(list_psf), 1):
            yCentre = medianBar[y][j] # list_psf[j]
            list_short_psf.append(yCentre)
            ax2.vlines(x=list_lb[j], ymin=lolims[j], ymax=uplims[j], color=listColour[y], linestyle='solid', linewidth=1.0)
            ax2.scatter(list_lb[j],uplims[j], marker='_',c=listColour[y],s=80,alpha=1)
            ax2.scatter(list_lb[j],lolims[j], marker='_',c=listColour[y],s=80,alpha=1)
            
        minY = int(min(list_psf)-1)
        maxY = int(max(list_psf)+2)
        ax2.set_ylim(minY,14)
        """
        if maxY < 12:
            ax2.set_ylim(minY,14) #maxY)
        else:
            ax2.set_ylim(minY,maxY)
        """
        
        if axCount in [0]:
            ax2.set_ylabel("Peak spatial "+""+" frequency (cpd)",rotation=-90, fontsize=18,labelpad=30)#, y=-0.3)
        
        if axCount in [0]:
            ax2.set_xlabel(r'Average background luminance (cd/m$^2$)',fontsize=18, rotation=0,labelpad=8)#, x=0.55)            
        
        ax2.tick_params(which='major', width=1.5, length=7,labelsize=12)


        ax2.set_xlim(5, 500)
        ax2.set_xscale("log", base=10) 
        ax2.set_xticks([10,100, 500])
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        #ax2.legend( loc='lower center', fontsize=12,ncol=1, facecolor='white',edgecolor='black')
        listLb_pars.append(list_lb)
        listPSF_pars.append(list_short_psf)
        
        
        # --- fit model isf ---
        fitFind_Function_k = model_EI_fn # model_EI_SF 
        # model_EI_SF_reduced# model_EI_SF 
        
        indexListRemove = [[7,9],[],[2],[],[]]
        for listSF in [[list_lb, list_psf]]:
            xNewn, yNewn = listSF[0],listSF[1]
            xNew, yNew   = indexInListRemove(xNewn, yNewn, indexListRemove[axCount]) 
            
            guessParams_k, boundDW_k, boundUP_k = [],[],[]
            
            """
            model_EI_SF(x, x0, x1, x2, x3, x4, x5,x6,x7,x8,x9,x10,x11):
            wEE       = x0
            wEI       = x1
            wIE       = x2
            wII       = x3
            
            wEe       = x4
            wEi       = x5
            wIe       = x6
            wIi       = x7
           
            alpha     = x8
            rI0       = x9
            rE0       = x10
            """
            
            wEi   = 2.76
            wIE   = 7.05 # 7.05
            alPha = 0.99 # 0.99
            #     # [x0 , x1    , x2  ,   x3,     x4,   x5  ,  x6  ,  x7]
            #p0_kp=[ 4.3, 6.47, 0.85, 0.86, 0.96]
            if y==0:
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, wEi, 0.84, 2.63, alPha+0.01, 0.79, 0.92]   #  <---
                #p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2, alPha, 0.79, 0.92] 
            elif y==1:
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2.63, alPha+0.01, 0.79, 0.92]   #  <---
                #p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2, alPha, 0.79, 0.92]  
            elif y == 4:
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2.63, alPha, 0.79, 0.92] # par4
            elif y==3:
                xNew.extend([100,380, 550]), yNew.extend([1.5,yNewn[5]+0.5, yNewn[6]])
                p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2.63, alPha+0.01, 0.79, 0.92]  #  <---
                #p0_kp=[0.74, 0.0, wIE, 2.12, 0.88, 2.76, 0.84, 2, alPha, 0.79, 0.92]  
            
            
            
            wEE = 6.0 # increase -> shift "jump" backwards.
            wEe = 6.4 # decrease value -> stabillity later on for greater x axis
            wEI = 14.0 # Increase --> shoves down rE0 vs Lb 
            wEi = 100 # Increase <-- shifts "jump" back for increasing value (keeps total length)
            wIE = 12.0 # Increase <---  shifts "jump" back  (moves entire length)
            wIe = 3.6 # Increase <--- shoves rE0 vs Lb down
            wII = 500.0 ## 22.6 #<-- stabalises all kn curves (does not let kn shoot to 1000s)
            wIi = 1.0 # increase <--- rE0 vs Lb more curve ( if descrease -> creates kink/knee)  

            #weights = [wEE, wEe, wEI, wEi,wIE,wIe,wII,wIi]
            #weights.extend([0.98, 1.0, 1.0])
            weights = [0.99, 0.54, 7.02, 2.14, 0.88, 2.75, 0.84, 2.63, 1.0, 0.78, 0.92]
            
            maxW=10
            #
            guessParams_k   = p0_kp
            boundDW_k       = [  0.0,0.0,   0  ,0,0,0.0,0.0,0,0.9,0,0]
            boundUP_k       = [  1,  maxW, maxW,  3, 1,  maxW, 3,3,1,1,1]
            
            #try:
            colorm = ['red', 'blue']
            countm =-1
            for fitm in ['trf']:#, 'dogbox']:
                countm+=1
                xy          = fitFunctionLimit([1, 1_000], xNew, yNew, fitFind_Function_k, guessParams_k, boundDW_k, boundUP_k, fitm, 500_000)
                xFit        = xy[0]
                yFit        = xy[1]
                yParam      = xy[2]
                pcov        = xy[3]
                ax2.plot(xFit,yFit,alpha=1,linestyle='solid',linewidth=1.0,c='forestgreen', label=r'Intrinsic SF')
            
                listRound = [round(elem.astype(float),2) for elem in list(yParam.values())]
                #print('listRound', listRound)
                print(fitm+' par:'+str(y)+' (yParam.values-PSF) \n ', np.array(listRound).tolist())#.astype(float))
                
                if y==1:
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.4 ,  0.8 ,  22.4,  3.9  ,7.4  ,2.8,  42.5  ,1.4,  0.67 # par 1
                elif y==3:
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 23 , 0.11 , 52.2 , 9.1, 16.2, 19.2, 90.3,  4 , 0.87 # par 3
                elif y==4:
                    (wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha) = (6.8  , 0.09 , 10.4 , 9.10, 7.3, 19.2, 68.6,  2.50 , 0.74) # par 4
                elif y==0:
                    #wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 0.8 ,  0.8 ,  22.4,  3.9  ,7.4  ,2.8,  42.5  ,0.9,  0.67 # par 0
                    #wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha =  0.22520748410579075 ,1.679693354680453 ,86.59346335456462 ,5.514539918217548 ,22.547904356124654 ,1.4129878581099353 ,187.3489533696 ,3.9596987461439355 ,0.6536676025398842 ,
                    
                    [wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha] = [
                        1.2 ,
                        0.88 ,
                        38.87 ,
                        3.74 ,
                        10.32 ,
                        1.5 ,
                        75.29 ,
                        1.5 ,
                        0.59 ,
                        ]# par 0
                    # par 0
                else:
                    wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha = 4.5,  0.5,6.9,     10.5, 28.4,  14.9,64.5,  3.0,  0.92


                params = [wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi ,alpha]
                xFit   = np.linspace(0, 40, 1_000)
                scaled_xaxis, y_predict = model_psf_function(params, xFit)
                ax2.plot(scaled_xaxis, y_predict,alpha=1,linestyle='solid',linewidth=1.0,c='black', label=r'Preferred SF')
            #except:
            #    print('no fit found')
            #    pass
            #else:
            #    print('no fit found')
            #    pass
            
            
        minY = int(min(list_psf)-1)
        maxY = int(max(list_psf)+2)
        ax2.set_ylim(0,12)
        ax2.set_yticks([2,4,6,8,10])


        ax2.tick_params(axis='both', which='major', width=1.5,labelsize=12, length=7)
        ax2.set_xlim(1, 1_000)
        ax2.set_xscale("log", base=10) 
        ax2.set_xticks([1, 10,100,1000])
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ax2.legend(loc='upper center', bbox_to_anchor=(0.3, 0.98),
                  ncol=1, fancybox=False, shadow=False, fontsize=18, edgecolor='white')      
        
        """
        fileName    = 'data_isf_psf_lum.txt'
        fileNameSD  = 'data_isf_lum_spread.txt'
        listOutMain = readText_toList(fileGet)

        listOutMainSD = readText_toList(fileGet_SD)

        list_lum_p = listOutMain[0]
        list_psf_p = listOutMain[1]

        list_lum_i = listOutMain[2]
        list_isf_1 = listOutMain[3]
        list_isf_2 = listOutMain[4]
        list_isf_3 = listOutMain[5]
        
        list_isf_1SD = np.array(listOutMainSD[0])
        list_isf_2SD = np.array(listOutMainSD[1])
        list_isf_3SD = np.array(listOutMainSD[2])

        # clean up zeros
        while 0.0 in list_lum_i:
            i0 = list_lum_i.index(0.0)
            list_lum_i.pop(i0)
            list_isf_1.pop(i0)
            list_isf_2.pop(i0)
            list_isf_3.pop(i0)
        """
        
        """
        print('list_isf_1',list_isf_1)
        print('list_isf_1SD',list_isf_1SD)
        ymin = np.array(list_isf_1)-list_isf_1SD/2
        ymax = np.array(list_isf_1)+list_isf_1SD/2
        ax2.scatter(np.array(list_lum_i), ymax, marker='_', s=110, color='red')
        ax2.scatter(np.array(list_lum_i), ymin, marker='_', s=110, color='red')
        ax2.vlines(np.array(list_lum_i), ymin=ymin, ymax=ymax, color='red')
        
        ymin = list_isf_2-list_isf_2SD/2
        ymax = list_isf_2+list_isf_2SD/2
        ax2.scatter(np.array(list_lum_i), ymax, marker='_', s=110, color='red')
        ax2.scatter(np.array(list_lum_i), ymin, marker='_', s=110, color='red')
        ax2.vlines(np.array(list_lum_i), ymin=ymin, ymax=ymax, color='red')
        
        ax2.scatter(np.array(list_lum_i), list_isf_1, marker='o', s=110, color='red', edgecolor='black', zorder=22)
        ax2.scatter(np.array(list_lum_i), list_isf_2, marker='x', s=110, color='firebrick', edgecolor='black', zorder=22)
        ax2.scatter(np.array(list_lum_i), list_isf_3, marker='P', s=110, color='orange', edgecolor='black', zorder=22)
        """
        
    #fig.delaxes(dictPotsCSF[listax2[2]])  
    #fig.savefig("figure2_PSF.svg")
    plt.show() 
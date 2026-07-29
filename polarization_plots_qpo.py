import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from ixpeobssim.binning.polarization import xBinnedPolarizationCube

def create_title(array, string_to_add):
    title=[]
    for i in range(len(array)-1):
        title.append(f'[{array[i]},{array[i+1]}] keV {string_to_add}')
    return title

####################### POLARIZATION PLOT WITH Q and U #######################
"""
    This is a function that plots the polarization
    cubes from the polarization quantities Q, U, PD,
    PA, MDP and errors. This plot tries to be similar
    to xpbinview one.
"""
def pcube_contour(QN,QN_ERR,UN,UN_ERR,PD,PD_ERR,PA,PA_ERR,MDP_99,title,grid=True,ax=None,global_color=None):
    if not ax:
        fig, ax = plt.subplots(figsize=(7, 7), tight_layout=True)
    if not global_color:
        color='C0'
    else:
        color=global_color

    plt.axis('square')
    R = [20,40,60,80,100]
    # if np.max(PD)>0.6:
    #     R = [10,20,30,40,50,60,70,80,90,100]
    # else:
    #     R = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    THETA = [0,15,30,45,60,75,90,-15,-30,-45,-60,-75]

    r_=np.linspace(0,np.sqrt(2),1000)
    theta_=np.linspace(0,2*np.pi,1000)

    if grid==True:
        for r in R:
            ax.plot(r*np.cos(theta_)/100,r*np.sin(theta_)/100,linestyle='--',color='gray',alpha=0.5)
            ax.text(r*np.cos(np.radians(2*np.max(PA))-np.pi/2)/100, r*np.sin(np.radians(2*np.max(PA))-np.pi/2)/100, str(r)+'%', 
                ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))
            # ax.text(r*np.cos(np.radians(2*np.max(PA))+np.pi/2)/100, r*np.sin(np.radians(2*np.max(PA))+np.pi/2)/100, str(r)+'%', 
            #     ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))
            

        for ang in THETA:
            ax.plot(r_*np.cos(2*np.radians(ang)),r_*np.sin(2*np.radians(ang)),linestyle='--',color='gray',alpha=0.5)
            # ax.text(0.075*np.cos(2*np.radians(ang)), 0.075*np.sin(2*np.radians(ang)), str(ang)+'°', 
            #     ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))
            # ax.text(0.2*np.cos(2*np.radians(ang)), 0.2*np.sin(2*np.radians(ang)), str(ang)+'°', 
            #     ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))
            ax.text(0.7*np.cos(2*np.radians(ang)), 0.7*np.sin(2*np.radians(ang)), str(ang)+'°', 
                ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))

    SCALE=[1,2,3]
    linestyle=['solid','dashed','dashed']
    ell=[]
    for i, scale in enumerate(SCALE):
        ell.append(Ellipse(xy=(QN, UN), width=2*scale*PD_ERR, height=2*scale*PD_ERR, angle=0, edgecolor=color, alpha=1-scale*0.05, fc='None',linewidth=2,linestyle=linestyle[i]))
    
    ax.plot(QN,UN,marker='o',label=title,color=color)

    for ell_ in ell:
        ax.add_patch(ell_)

    ax.plot(MDP_99*np.cos(theta_),MDP_99*np.sin(theta_),alpha=1,label='MDP @ 99%',linestyle='dotted',linewidth=2)

    ax.set_xlabel('Q/I')
    ax.set_ylabel('U/I')

    qn_up_lim = np.abs(np.max(QN))+np.abs(6*np.max(QN_ERR))
    un_up_lim = np.abs(np.max(UN))+np.abs(6*np.max(UN_ERR))
    # breakpoint()
    ax.set_xlim([-max(qn_up_lim,un_up_lim),max(qn_up_lim,un_up_lim)])
    ax.set_ylim([-max(qn_up_lim,un_up_lim),max(qn_up_lim,un_up_lim)])

    ax.legend()
    return ax

def pcube_contour_plot(QN,QN_ERR,UN,UN_ERR,PD,PD_ERR,PA,PA_ERR,MDP_99,title,ENERGY_BINNING,grid=True,ax=None,global_color=None):

    for num in range(len(ENERGY_BINNING)-1):
        if num==0:
            grid=grid
        else:
            grid=False
        ax_out = pcube_contour(QN[num],QN_ERR[num],UN[num],UN_ERR[num],PD[num],PD_ERR[num],PA[num],PA_ERR[num],MDP_99[num],title[num],
                               grid=grid,ax=ax,global_color=global_color[num])

    return ax_out

def polarization_plot(QN,QN_ERR,UN,UN_ERR,PD,PD_ERR,PA,PA_ERR,MDP_99,title):
    
    plt.figure(figsize=(7,7))
    plt.axis('square')

    R = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    THETA = [0,15,30,45,60,75,90,-15,-30,-45,-60,-75]

    r_=np.linspace(0,np.sqrt(2),1000)
    theta_=np.linspace(0,2*np.pi,1000)

    for r in R:
        plt.plot(r*np.cos(theta_)/100,r*np.sin(theta_)/100,linestyle='--',color='gray',alpha=0.5)
        plt.text(r*np.cos(np.radians(2*np.max(PA))-np.pi/2)/100, r*np.sin(np.radians(2*np.max(PA))-np.pi/2)/100, str(r)+'%', 
            ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))

    for ang in THETA:
        plt.plot(r_*np.cos(2*np.radians(ang)),r_*np.sin(2*np.radians(ang)),linestyle='--',color='gray',alpha=0.5)
        plt.text(0.9*np.cos(2*np.radians(ang)), 0.9*np.sin(2*np.radians(ang)), str(ang)+'°', 
            ha='center', va='center', color='black', bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))

    xlim, ylim = [], []

    SCALE=[1,2,3]
    for i in range(len(QN)):
        ell=[]
        for scale in SCALE:
            ell.append(Ellipse(xy=(QN[i], UN[i]), width=2*scale*PD_ERR[i], height=2*scale*PD_ERR[i], angle=0, 
                edgecolor='C%.i'%(i), alpha=1-scale*0.1, fc='None',linewidth=2))
        
        plt.plot(QN[i],UN[i],marker='o',color='C%.i'%(i),label=title[i])

        for ell_ in ell:
            plt.gca().add_patch(ell_)

        plt.plot(MDP_99[i]*np.cos(theta_),MDP_99[i]*np.sin(theta_),color='C%.i'%(i),alpha=0.8,label='MDP @ 99%',linestyle='--')
        
        # print(title[i],MDP_99[i])
        # print('QN = ',QN[i],QN_ERR[i])
        # print('UN = ',UN[i],UN_ERR[i])
        # print('PD = ',PD[i],PD_ERR[i])
        # print('PA = ',PA[i],PA_ERR[i])
        xlim.append(np.abs(QN[i])+4*np.abs(PD_ERR[i]))
        ylim.append(np.abs(UN[i])+4*np.abs(PD_ERR[i]))

    plt.xlabel('Q/I')
    plt.ylabel('U/I')
    if np.max(xlim)>=1:
        xmin = -1
        xmax = 1 
    else:
        xmin = -np.max(xlim)
        xmax = np.max(xlim)
    if np.max(ylim)>=1:
        ymin = -1
        ymax = 1
    else:
        ymin = -np.max(xlim)
        ymax = np.max(xlim)    
    plt.xlim([xmin,xmax])
    plt.ylim([ymin,ymax])
    plt.legend()

#### THIS IS A POLARIZATION CONTOUR TOOL VER 3.0 ####
#### RELEASED JAN. 24. 2023. - DAWOON E. KIM ####

#### DEFAULT SETTING ####
#### C.L. = {"50.0%", "90.0%", "99.0%", "99.9%"} ####
#### CALCULATION BASED ON NORMALIZED Q & U ####

#### THIS IS A UNIT SCALING FACTOR FOR THE POLARIZATION DEGREE ####
UNIT = 100

#### PARAMETERS SETTING ####
def CHI_LIST(levels=None, sigma_unit=None):
    # sigma for 99% = 2.57583 in 1 D.O.F.
    # sigma for 99% = 3.03485492 in 2 D.O.F.
    from scipy.stats import chi2, norm

    if not levels:
        result = np.array([0.50, 0.90, 0.99, 0.999])
        labels = ["50.0 %", "90.0 %", "99.0 %", "99.9 %"]

    else:
        result=[]
        labels=[]

        for i in range(len(levels)):
            if not sigma_unit:
                globals()['std'+str(levels[i])] = levels[i]
                print("#### VALUES MUST BE SET WITHIN 0. - 1. ####")
                print("CONTOUR LEVELS :", globals()['std'+str(levels[i])])
            else :
                mean = 0
                SD = 1
                globals()['std'+str(levels[i])] = norm.cdf((levels[i])*SD, mean, SD) - norm.cdf(-(levels[i])*SD, mean, SD)
                print("CONTOUR LEVELS :", globals()['std'+str(levels[i])])
                # based on 1 D.O.F. sigma, [1,2,3] = [68.2689,], [1, 1.645, 2.57583] = [68.2689%, 90%, 99%]

            result.append(globals()['std'+str(levels[i])])
            CL = format(globals()['std'+str(levels[i])]*100, ".4f")
            labels.append(f'{CL}$\%$')

    degree_freedom = 2

    ### CALCULATING CHI_2 FROM PERCENTAGE ###
    list_chi_2 = np.array(np.sqrt(chi2.ppf(result, degree_freedom)))

    print("CONTOUR LEVELS IN CHI_2, SQRT(CHI**2) :", list_chi_2)
    print("CONFIDENCE LEVELS :", labels)

    return list_chi_2, labels

################### POL PROPERTIES CALCULATION ####################
def POL_CALCULATION(QN, UN):
    PD = np.sqrt(QN**2 + UN**2)
    PA = 0.5 * np.arctan2(UN,QN)
    return PD, PA

def TRANS_AND_RADIUS(QN, UN, EPSILON, aspect=True):
    q0 = QN
    u0 = UN
    zeta = np.linspace(0, 2*np.pi, 5000)
    Q_Ec= q0 + EPSILON * np.cos(zeta)
    U_Ec= u0 + EPSILON * np.sin(zeta)
    PI, PSI = POL_CALCULATION(Q_Ec, U_Ec)
    PI_0, PSI_0 = POL_CALCULATION(q0, u0)

    if not aspect:
        for i in range(PSI.size):
            if PSI[i] < 0:
                PSI[i] = PSI[i] + np.pi
        if PSI_0 < 0:
            PSI_0 = PSI_0 +np.pi
    else:
        PI = PI
        PI_0 = PI_0

    return PI_0, PSI_0, PI, PSI

################### PLOT ###################
def POL_CONTOUR_PLOT(QN, UN, QN_ERR, UN_ERR, aspect=True, ax=None, levels=None, sigma_unit=None, legend=True, text=True, rmax=None,global_color=None, obs_label=None, nsigma=None, marker=None, line=None):
    from scipy.stats import chi2, norm

    print("QN(%): ", np.round(QN*UNIT ,2),", UN(%): ", np.round(UN*UNIT ,2))
    print("QN_ERR(%): ", np.round(QN_ERR*UNIT ,2),", UN_ERR(%): ", np.round(UN_ERR*UNIT ,2))

    list_chi_2, labels = CHI_LIST(levels=levels, sigma_unit=None)

    sigma= np.abs(QN_ERR)
    epsilon = list_chi_2 * sigma
    if nsigma is None:
        epsilon = epsilon
    else:
        epsilon = epsilon[:nsigma]

    if not ax:
        cm = 1/2.54
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 7), tight_layout=True)

    # MDP #
    MDP_99 = np.sqrt(chi2.ppf(0.99,2)) * np.abs(QN_ERR) * UNIT

    # MAIN PLOT #
    for i in range(len(epsilon)):
        pi_0, psi_0, pi, psi = TRANS_AND_RADIUS(QN, UN, epsilon[i], aspect=aspect)
        pi_0 = pi_0 * UNIT
        pi = pi * UNIT

        if not global_color:
            color_input = ['red','orange','limegreen','tab:blue']
            ax.scatter(psi, pi, marker='.', color=color_input[i], s=0.02, alpha=0.5)
            ax.scatter(psi_0, pi_0, marker='o', s=20, color='k', edgecolors='k', alpha=0.5)
        else:
            if not marker:
                ax.plot(psi, pi, marker='', linestyle='-',linewidth=1,color=global_color, alpha=1)
                if i==0:
                    ax.scatter(psi_0, pi_0, marker='o', s=20, color=global_color, edgecolors=global_color, alpha=1, label=obs_label)
                else:
                    ax.scatter(psi_0, pi_0, marker='o', s=20, color=global_color, edgecolors=global_color, alpha=1)
            else:
                ax.plot(psi, pi, marker='', linestyle=line,linewidth=1,color=global_color, alpha=1)
                if i==0:
                    ax.scatter(psi_0, pi_0, marker=marker, s=20, color=global_color, edgecolors=global_color, alpha=1, label=obs_label)
                else:
                    ax.scatter(psi_0, pi_0, marker=marker, s=20, color=global_color, edgecolors=global_color, alpha=1)

    POL_DEGREE= np.round(pi_0, 2)
    POL_ANGLE= np.round(np.rad2deg(psi_0), 2)
    # CENTER POINT #
    #ax.arrow(0,0,psi_0,pi_0)
    #ax.scatter(psi_0,pi_0, marker='o', s=15, color='k', lw=1) !!!!!!!!!!!!!!!!!
    stat_signif = np.round(pi_0/(np.abs(sigma)*UNIT), 3)
    print("==================== SUMMARY ====================")
    print("Statistical Significance", np.round(stat_signif,2))
    print("MDP_99, 2 D.O.F. (%): ", np.round(MDP_99,2))

    Detection_CL= np.round(chi2.cdf(stat_signif**2, 2)*UNIT, 2)
    print("Detection Significance (%)", Detection_CL)

    print("PD(%):", POL_DEGREE, "PD_ERR_1D(±)", np.round(np.abs(QN_ERR)*UNIT,2), 'PA(°):', POL_ANGLE, "PA_ERR_1D(±)", np.round(np.rad2deg(np.abs(QN_ERR)*UNIT)/(2*pi_0),2))

    POL_ANGLE_ERR = np.round(np.rad2deg(np.abs(QN_ERR)*UNIT)/(2*pi_0),2)

    ####### MAXIMA PD 100 % ######
    if np.max(pi[-1]) >= 100:
        ax.set_rmax(100)

    elif rmax:
        ax.set_rmax(rmax)

    ax.set_theta_zero_location("N")
    

    ####### ASPECT CHANGE ######
    if not aspect:
        ax.set_thetamax(180)
        tex_info = [[0.69, 1.05, 'N'], [0.69, -0.05,  'S'], [0, 0.5, 'E']]
        # title_pos =-0.2
        legend_pos = [0.3,0.97]
        grid_lines, grid_labels = plt.thetagrids(range(0, 181, 30))
        ax.text(0.95,0.75,'PD\n(%)', horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize='large')
    elif aspect=='half left':
        ax.set_thetamax(180)
        tex_info = [[1., 1.1, 'N'], [-0.13, 0., 'E']]
        # title_pos =-0.1
        legend_pos = [0.3,.95]
        grid_lines, grid_labels = plt.thetagrids(range(0, 181, 30))
    elif aspect=='half right':
        ax.set_thetamin(-180)
        ax.set_thetamax(0)
        tex_info = [[0., 1.2, 'N'], [1.25, 0, 'W']]
        # title_pos =-0.27
        legend_pos = [.98,0.92]
        grid_lines, grid_labels = plt.thetagrids(range(-181, 1, 30))
    elif aspect=='half top':
        ax.set_thetamin(-90)
        ax.set_thetamax(90)
        tex_info = [[0., 1.2, 'N'], [1.25, 0, 'W'], [-0.13, 0., 'E']] # original code
        # tex_info = [[0.5, 1.2, 'N'], [1.1, 0.5, 'W'], [-1.5, 0.5, 'E']] # modified per swiftj1727
        # title_pos =-0.27
        legend_pos = [.98,0.92]
        grid_lines, grid_labels = plt.thetagrids(range(-90, 90, 5)) ## se no rimetti 30 come sopra, così mette le grid ogni 5 deg

    elif aspect=='custom theta':
        theta_min = np.min(POL_ANGLE)-30
        theta_max = np.max(POL_ANGLE)+30
        ax.set_thetamin(theta_min)
        ax.set_thetamax(theta_max)
        tex_info = [[0., 1.2, 'N'], [1.25, 0, 'W']]
        # title_pos =-0.27
        legend_pos = [.98,0.92]
        grid_lines, grid_labels = plt.thetagrids(range(int(theta_min), int(theta_max), 10))

    else:
        ax.set_thetamin(-90)
        ax.set_thetamax(90)
        tex_info = [[0.45, 0.8, 'N'], [1.14, 0.25, 'W'], [-0.12, 0.25, 'E']]
        # title_pos =0.1
        legend_pos = [0.3,.95]
        grid_lines, grid_labels = plt.thetagrids(range(-90, 91, 30))

    ### LEGEND SETTING ###
    if legend:
        ax.legend(markerscale=2, fontsize='x-large', bbox_to_anchor=legend_pos, bbox_transform=plt.gcf().transFigure)

    ### DIRECTION TEXT ###
    if text:
        for i in range(len(tex_info)):
            ax.text(tex_info[i][0],tex_info[i][1],tex_info[i][2], horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize='large')

    ax.set_rlim(0)
    ax.grid(True, lw=1, zorder=0, alpha=1., ls=':')

    return ax

def polarization_contour(input, output=None, aspect=None, ax=None, levels=None, sigma_unit=None,legend=False, text=False, rmax=None, global_color=None, obs_label=None, nsigma=None, marker=None, line=None):
    src_pcube = xBinnedPolarizationCube.from_file_list(input)
   # bkg_pcube = xBinnedPolarizationCube.from_file_list(bkg_input)
    #print("SRC_COUNTS", float(src_pcube.COUNTS), "BKG_COUNTS", float(bkg_pcube.COUNTS))

    #bkg_pcube *= src_pcube.backscal() / bkg_pcube.backscal()
    #src_pcube -= bkg_pcube
    #print('BACKSCALE_SRC', src_pcube.backscal(), 'BACKSCALE_BKG', bkg_pcube.backscal(), 'BACKSCALE_RATIO', np.round(src_pcube.backscal() / bkg_pcube.backscal(), 2))

    EBINS_NUM=  src_pcube.hdu_list[1].header['NAXIS2']
    for num in range(EBINS_NUM):
        print("EBINS_NUM", f'{num+1} / {EBINS_NUM}')
        ax_out = POL_CONTOUR_PLOT(float(src_pcube.QN[num]), float(src_pcube.UN[num]), float(src_pcube.QN_ERR[num]), 
                                  float(src_pcube.UN_ERR[num]), aspect=aspect, ax=ax, levels=levels, sigma_unit=sigma_unit,
                                  legend=legend, text=text, rmax=rmax, global_color=global_color[num], obs_label=obs_label, nsigma=nsigma, marker=marker, line=line)

    if output:
        plt.savefig(output, dpi=300, transparent=True, bbox_inches='tight')

    return ax_out

def polarization_contour_from_STOKES(QN,QN_ERR,UN,UN_ERR, EBINS_NUM, output=None, aspect=None, ax=None, levels=None, sigma_unit=None,legend=False, text=False, rmax=None, global_color=None, obs_label=None, nsigma=None, marker=None, line=None):

    for num in range(EBINS_NUM):
        print("EBINS_NUM", f'{num+1} / {EBINS_NUM}')
        ax_out = POL_CONTOUR_PLOT(QN[num], UN[num], QN_ERR[num], 
                                  UN_ERR[num], aspect=aspect, ax=ax, levels=levels, sigma_unit=sigma_unit,
                                  legend=legend, text=text, rmax=rmax, global_color=global_color[num], obs_label=obs_label, nsigma=nsigma, marker=marker, line=line)

    if output:
        plt.savefig(output, dpi=300, transparent=True, bbox_inches='tight')

    return ax_out

# configuration of the pipeline
import os

#directory
class configuration():
    def __init__(self):
        #directory
        self.root_dir = r'J:\Xunda\Xunda_OG_TRN_fMRI_During_2023'
        self.pathseed = os.path.join(self.root_dir, r'ROI_RatTRNH1-20230518')
        self.pathroi = os.path.join(self.root_dir, r'Atlas-based_ROIs_TRNorVSfMRI')
        self.raw_path = os.path.join(self.root_dir, r'RatTRNH5RsfMRISinglePulse-20230722')
        self.average_path = os.path.join(self.root_dir, 'Average')
        self.path1 = os.path.join(self.raw_path, 'Inter-Animal')
        self.outexcel = 'ALLLargeROIs'
        self.ppt_name = 'rsfMRI_CCMaps_ALLROIs_RatTRNH1-20230518'
        
        #experiment configurations
        self.func_ids = [[8]]#29,10,11,12,16,17,18,22,23,24,28,29,30,34,35,36
        self.iifiles = self.func_ids[0]
        #for TRN project
        self.netname =  ['S1BFR','S1BFL','S2R','S2L','V1R','V1L','A1R','A1L','M1R','M1L','SCR','SCL',
        'VPMR','VPML','POR','POL','TRNR','TRNL','LGNR','LGNL','MGBR','MGBL','CTR', 'CTL',
         'dPAG','vPAG','InsR','InsL','dCPuR','dCPuL','vCPuR','vCPuL',
         'CgR','CgL','Cgbilateral','RscR','RscL','Rscbilateral','PrLR','PrLL','HPR','HPL','AmgR', 'AmgL','OFCR','OFCL']
        #for Spindle aging memory project
        self.ROIname = ['S1BFR','S1BFL','S2R','S2L','VCR_new2','VCL_new2','AudR','AudL','MCR','MCL','SCR','SCL',
       'VPMR','VPML','POR','POL','TRNR','TRNL','LGNR','LGNL','MGBR','MGBL','CTR', 'CTL',
       'dPAG','vPAG','GIR','GIL','dCPuR','dCPuL','vCPuR','vCPuL',
         'CgR','CgL','Cgbilateral','RSR','RSL','RSbilateral','PrLR','PrLL','HPR','HPL','AmgR', 'AmgL','OFCR','OFCL']
        
        self.TR = 1
        self.DIM = [128, 128, 16, 600]
        self.timep = list(range(600))

        self.VOX = [0.25, 0.25, 1.0]
        self.T2 = os.path.join(self.path1, 'T2','rT2_128.img')#within animal      
        self.TaskmeanEPITrial = 15.1       
        # bandwidth-->fc :0--> fc=0.005-0.1; 1--> fc=0.005-0.05; 2--> fc=0.05-0.1; 3--> fc=0.1-0.3; 4--> fc=0.3-0.5;
        self.fcs = [[0.005, 0.1],[0.005, 0.05], [0.05, 0.1], [0.1, 0.3], [0.3, 0.5]]
        self.fs = 1
        self.filter_order = 2
        
        #frequenctly used parameters
        self.GSindex = 1
        self.filter = 0.5
        self.CCMapmaskindex = 1
        self.AtlasbasedROIregres = 0 #use atlas-based ROI for regression of task-evoked activties, otherwise use expanded seed ROIs   
        self.Motionregres=1
        self.bandwidth = -1     #in [0,1,2,3,4], -1 for no filtering
        self.Taskindex = 1
        self.gaussian_sigma = 0 #0 for no gaussian smoothing, the unit of self.gaussian_sigma is pixel
        self.gaussian_kernel = 9 #-1 for default gaussian kernel size(following the relationship of sigma = 0.3 * ((kernel_size - 1) * 0.5 - 1) + 0.8)
        
        #selection of frequenctly used parameters
        self.frequenctly_changed_parameters = {
          'GSindex':[0,1],
          'filter':[0.1, 0.5],
          'CCMapmaskindex':[0,1],
          'AtlasbasedROIregres':[0,1],
          'Motionregres':[0,1],
          'bandwidth':[0,1,2,3,4],
          'Taskindex':[0,1],
          'gaussian_sigma': [0,1],
          'no_parameter': [1],
        }
          
        #overlay settings
        self.overlay_thrmin = 0.1
        self.overlay_thrmax = 1
        
        #pptx settings
        self.pptw = 6
        self.ppth = 0.55
        self.pptt = 0.55
        self.pptg = 0.05

        self.update_config()

    def update_config(self):
        #update configuration based on other parameters
        if self.filter==0.1:
          self.prefix='rrsfra2dseq'
        else:
          self.prefix='rrsra2dseq'


# ----------------------------------------------------------- auxiliary function -----------------------------------------------------------
def get_study_ids_and_scan_nums(condition):
    Condidx = condition_names.index(condition) + 1
    if Condidx==1:
        study_ids = [
            'RatTRNG6RsfMRISinglePulse-20230505', #G6,6.1
            'RatTRNG6RsfMRISinglePulse-20230516', #G6-2,6.2
            'RatTRNG7RsfMRISinglePulse-20230510', #G7,7.1  
            'RatTRNG7RsfMRISinglePulse-20230516', #G7-2,7.2
            'RatTRNG7RsfMRISinglePulse-20230622', #G7-3,7.3
            'RatTRNG7RsfMRISinglePulse-20230628', #G7-4,7.4
            'RatTRNG8RsfMRISinglePulse-20230512', #G8,8.1  
            'RatTRNG8RsfMRISinglePulse-20230525', #G8-2,8.2
            'RatTRNG8RsfMRISinglePulse-20230623', #G8-3,8.3
            'RatTRNG8RsfMRISinglePulse-20230630', #G8-4,8.4
            'RatTRNH2RsfMRISinglePulse-20230514', #H2,9.1 
            'RatTRNH2RsfMRISinglePulse-20230527', #H2-2,9.2
            'RatTRNH2RsfMRISinglePulse-20230623', #H2-3,9.3
            'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
            'RatTRNH1RsfMRISinglePulse-20230529', #H1-2,10.2
            'RatTRNH1RsfMRISinglePulse-20230628', #H1-3,10.3
            'RatTRNH1RsfMRISinglePulse-20230706', #H1-4,10.4
            'RatTRNH1RsfMRISinglePulse-20230710', #H1-5,10.5
            'RatTRNH1RsfMRISinglePulse-20230714', #H1-6,10.6
            'RatTRNH3RsfMRISinglePulse-20230523', #H3,11
            'RatTRNH4RsfMRISinglePulse-20230531', #H4,12.1
            'RatTRNH4RsfMRISinglePulse-20230626', #H4-2,12.2
            'RatTRNH5RsfMRISinglePulse-20230702', #H5,13.1  
            'RatTRNH5RsfMRISinglePulse-20230708', #H5-2,13.2
            'RatTRNH5RsfMRISinglePulse-20230712', #H5-3,13.3
            'RatTRNH5RsfMRISinglePulse-20230718', #H5-4,13.4
            'RatTRNH5RsfMRISinglePulse-20230722', #H5-5,13.5
            'RatTRNH8RsfMRISinglePulse-20230704', #H8,14.1
            'RatTRNH8RsfMRISinglePulse-20230708', #H8-2,14.2
            'RatTRNH8RsfMRISinglePulse-20230718', #H8-4,14.4
            'RatTRNH8RsfMRISinglePulse-20230722', #H8-5,14.5
            'RatTRNH7RsfMRISinglePulse-20230716', #H7,15.1
            'RatTRNH7RsfMRISinglePulse-20230720', #H7-2,15.2
        ] 

        scan_num= [
            [13,14,15], #G6,6.1
            [19,20,21], #G6-2,6.2
            [13,14,15], #G7,7.1  
            [19,20,21], #G7-2,7.2
            [20,21,22], #G7-3,7.3
            [8], #G7-4,7.4
            [13,14,15,17], #G8,8.1  
            [14,15,16], #G8-2,8.2
            [19,20,21], #G8-3,8.3
            [19,20,21], #G8-4,8.4
            [13,14,15], #H2,9.1 
            [13,14,15], #H2-2,9.2
            [19,20,21], #H2-3,9.3
            [13,14,15], #H1,10.1
            [13,14,15,16], #H1-2,10.2
            [13,14,15], #H1-3,10.3
            [19,20,21], #H1-4,10.4
            [19,20,21], #H1-5,10.5
            [9], #H1-6,10.6
            [13,14,15,16], #H3,11
            [13,14,15], #H4,12.1
            [19,20,21], #H4-2,12.2
            [13,14,15,16], #H5,13.1  
            [19,20,21], #H5-2,13.2
            [19,20,21], #H5-3,13.3
            [18,19,20], #H5-4,13.4
            [26], #H5-5,13.5
            [13,14,15], #H8,14.1
            [19,20,21], #H8-2,14.2
            [19,20,21], #H8-4,14.4
            [27], #H8-5,14.5
            [19,20,21], #H7,15.1
            [21], #H7-2,15.2
        ]

        AllAVGanimals= [
            [6.1], #G6,6.1
            [6.2], #G6-2,6.2
            [7.1], #G7,7.1  
            [7.2], #G7-2,7.2
            [7.3], #G7-3,7.3
            [7.4], #G7-4,7.4
            [8.1], #G8,8.1  
            [8.2], #G8-2,8.2
            [8.3], #G8-3,8.3
            [8.4], #G8-4,8.4
            [9.1], #H2,9.1 
            [9.2], #H2-2,9.2
            [9.3], #H2-3,9.3
            [10.1], #H1,10.1
            [10.2], #H1-2,10.2
            [10.3], #H1-3,10.3
            [10.4], #H1-4,10.4
            [10.5], #H1-5,10.5
            [10.6], #H1-6,10.6
            [11], #H3,11
            [12.1], #H4,12.1
            [12.2], #H4-2,12.2
            [13.1], #H5,13.1  
            [13.2], #H5-2,13.2
            [13.3], #H5-3,13.3
            [13.4], #H5-4,13.4
            [13.5], #H5-5,13.5
            [14.1], #H8,14.1
            [14.2], #H8-2,14.2
	        [14.4], #H8-4,14.4
            [14.5], #H8-5,14.5
            [15.1], #H7,15.1
            [15.2], #H7-2,15.2                  
        ]


    # 1HzSineWave12sOn18sOff(all trials)
    elif Condidx==2:

        study_ids= [
            'RatTRNG6RsfMRISinglePulse-20230505', #G6,6.1
            'RatTRNG6RsfMRISinglePulse-20230516', #G6-2,6.2
            'RatTRNG7RsfMRISinglePulse-20230510', #G7,7.1  
            'RatTRNG7RsfMRISinglePulse-20230516', #G7-2,7.2
            'RatTRNG7RsfMRISinglePulse-20230622', #G7-3,7.3
            'RatTRNG7RsfMRISinglePulse-20230628', #G7-4,7.4
            'RatTRNG8RsfMRISinglePulse-20230512', #G8,8.1  
            'RatTRNG8RsfMRISinglePulse-20230525', #G8-2,8.2
            'RatTRNG8RsfMRISinglePulse-20230623', #G8-3,8.3
            'RatTRNG8RsfMRISinglePulse-20230630', #G8-4,8.4
            'RatTRNH2RsfMRISinglePulse-20230514', #H2,9.1 
            'RatTRNH2RsfMRISinglePulse-20230527', #H2-2,9.2
            'RatTRNH2RsfMRISinglePulse-20230623', #H2-3,9.3
            'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
            'RatTRNH1RsfMRISinglePulse-20230529', #H1-2,10.2
            'RatTRNH1RsfMRISinglePulse-20230628', #H1-3,10.3
            'RatTRNH1RsfMRISinglePulse-20230706', #H1-4,10.4
            'RatTRNH1RsfMRISinglePulse-20230710', #H1-5,10.5
            'RatTRNH1RsfMRISinglePulse-20230714', #H1-6,10.6
            'RatTRNH3RsfMRISinglePulse-20230523', #H3,11
            'RatTRNH4RsfMRISinglePulse-20230531', #H4,12.1
            'RatTRNH4RsfMRISinglePulse-20230626', #H4-2,12.2
            'RatTRNH5RsfMRISinglePulse-20230702', #H5,13.1  
            'RatTRNH5RsfMRISinglePulse-20230708', #H5-2,13.2
            'RatTRNH5RsfMRISinglePulse-20230712', #H5-3,13.3
            'RatTRNH5RsfMRISinglePulse-20230718', #H5-4,13.4
            'RatTRNH5RsfMRISinglePulse-20230722', #H5-5,13.5
            'RatTRNH8RsfMRISinglePulse-20230704', #H8,14.1
            'RatTRNH8RsfMRISinglePulse-20230708', #H8-2,14.2
            'RatTRNH8RsfMRISinglePulse-20230722', #H8-5,14.5
            'RatTRNH7RsfMRISinglePulse-20230716', #H7,15.1
            'RatTRNH7RsfMRISinglePulse-20230720', #H7-2,15.2
        ] 


        scan_num= [
            [19,20,21], #G6,6.1
            [13,14,15], #G6-2,6.2
            [19,20,21], #G7,7.1  
            [13,14,15], #G7-2,7.2
            [26,27,28], #G7-3,7.3
            [9], #G7-4,7.4
            [20,21,22,23,24], #G8,8.1  
            [20,21,22], #G8-2,8.2
            [13,14,15], #G8-3,8.3
            [13,14,15], #G8-4,8.4
            [19,20,21], #H2,9.1 
            [19,20,21], #H2-2,9.2
            [13,14,15], #H2-3,9.3
            [19,20,21], #H1,10.1
            [20,21,22], #H1-2,10.2
            [19,20,21], #H1-3,10.3
            [13,14,15], #H1-4,10.4
            [25,26,27], #H1-5,10.5
            [10], #H1-6,10.6
            [20,21,22], #H3,11
            [19,20,21], #H4,12.1
            [13,14,15], #H4-2,12.2
            [20,21,22], #H5,13.1  
            [13,14,15], #H5-2,13.2
            [25,26,27], #H5-3,13.3
            [24,25,26], #H5-4,13.4
            [27], #H5-5,13.5
            [19,20,21], #H8,14.1
            [13,14,15], #H8-2,14.2
            [28], #H8-5,14.5
            [25,26,27], #H7,15.1
            [22], #H7-2,15.2
        ]


        AllAVGanimals= [
            [6.1], #G6,6.1
            [6.2], #G6-2,6.2
            [7.1], #G7,7.1  
            [7.2], #G7-2,7.2
            [7.3], #G7-3,7.3
            [7.4], #G7-4,7.4
            [8.1], #G8,8.1  
            [8.2], #G8-2,8.2
            [8.3], #G8-3,8.3
            [8.4], #G8-4,8.4
            [9.1], #H2,9.1 
            [9.2], #H2-2,9.2
            [9.3], #H2-3,9.3
            [10.1], #H1,10.1
            [10.2], #H1-2,10.2
            [10.3], #H1-3,10.3
            [10.4], #H1-4,10.4
            [10.5], #H1-5,10.5
            [10.6], #H1-6,10.6
            [11], #H3,11
            [12.1], #H4,12.1
            [12.2], #H4-2,12.2
            [13.1], #H5,13.1  
            [13.2], #H5-2,13.2
            [13.3], #H5-3,13.3
            [13.4], #H5-4,13.4
            [13.5], #H5-5,13.5
            [14.1], #H8,14.1
            [14.2], #H8-2,14.2
            [14.5], #H8-5,14.5
            [15.1], #H7,15.1
            [15.2], #H7-2,15.2
        ]
 

        # 40HzSineWave10sOn20sOff(all trials)
    elif Condidx==3:
        study_ids= [
            'RatTRNG6RsfMRISinglePulse-20230505', #G6,6.1
            'RatTRNG6RsfMRISinglePulse-20230516', #G6-2,6.2
            'RatTRNG7RsfMRISinglePulse-20230510', #G7,7.1  
            'RatTRNG7RsfMRISinglePulse-20230516', #G7-2,7.2
            'RatTRNG7RsfMRISinglePulse-20230622', #G7-3,7.3
            'RatTRNG7RsfMRISinglePulse-20230628', #G7-4,7.4
            'RatTRNG8RsfMRISinglePulse-20230512', #G8,8.1  
            'RatTRNG8RsfMRISinglePulse-20230525', #G8-2,8.2
            'RatTRNG8RsfMRISinglePulse-20230623', #G8-3,8.3
            'RatTRNG8RsfMRISinglePulse-20230630', #G8-4,8.4
            'RatTRNH2RsfMRISinglePulse-20230514', #H2,9.1 
            'RatTRNH2RsfMRISinglePulse-20230527', #H2-2,9.2
            'RatTRNH2RsfMRISinglePulse-20230623', #H2-3,9.3
            'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
            'RatTRNH1RsfMRISinglePulse-20230529', #H1-2,10.2
            'RatTRNH1RsfMRISinglePulse-20230628', #H1-3,10.3
            'RatTRNH1RsfMRISinglePulse-20230706', #H1-4,10.4
            'RatTRNH1RsfMRISinglePulse-20230710', #H1-5,10.5
            'RatTRNH1RsfMRISinglePulse-20230714', #H1-6,10.6
            'RatTRNH3RsfMRISinglePulse-20230523', #H3,11
            'RatTRNH4RsfMRISinglePulse-20230531', #H4,12.1
            'RatTRNH4RsfMRISinglePulse-20230626', #H4-2,12.2
            'RatTRNH5RsfMRISinglePulse-20230702', #H5,13.1  
            'RatTRNH5RsfMRISinglePulse-20230708', #H5-2,13.2
            'RatTRNH5RsfMRISinglePulse-20230712', #H5-3,13.3
            'RatTRNH5RsfMRISinglePulse-20230718', #H5-4,13.4
            'RatTRNH5RsfMRISinglePulse-20230722', #H5-5,13.5
            'RatTRNH8RsfMRISinglePulse-20230704', #H8,14.1
            'RatTRNH8RsfMRISinglePulse-20230708', #H8-2,14.2
            'RatTRNH8RsfMRISinglePulse-20230712', #H8-3,14.3
            'RatTRNH8RsfMRISinglePulse-20230718', #H8-4,14.4
            'RatTRNH8RsfMRISinglePulse-20230722', #H8-5,14.5
            'RatTRNH7RsfMRISinglePulse-20230716', #H7,15.1
            'RatTRNH7RsfMRISinglePulse-20230720', #H7-2,15.2
        ] 


        scan_num= [
            [25,26,27], #G6,6.1
            [25,26,27], #G6-2,6.2
            [25,26,27], #G7,7.1  
            [25,26,27], #G7-2,7.2
            [14,15,16], #G7-3,7.3
            [10], #G7-4,7.4
            [28,29,30], #G8,8.1  
            [26,27,28,33,34], #G8-2,8.2
            [25,26,27], #G8-3,8.3
            [25,26,27], #G8-4,8.4
            [25,26,27], #H2,9.1 
            [25,26,27], #H2-2,9.2
            [25,26,27], #H2-3,9.3
            [26,27,28], #H1,10.1
            [26,27,28], #H1-2,10.2
            [25,26,27], #H1-3,10.3
            [25,26,27], #H1-4,10.4
            [13,14,15], #H1-5,10.5
            [11], #H1-6,10.6
            [27,28,29], #H3,11
            [25,26,27], #H4,12.1
            [25,26,27], #H4-2,12.2
            [26,27,28], #H5,13.1  
            [25,26,27], #H5-2,13.2
            [13,14,15], #H5-3,13.3
            [12,13,14], #H5-4,13.4
            [28], #H5-5,13.5
            [25,26,27], #H8,14.1
            [25,26,27], #H8-2,14.2
            [13,14,15,19,20], #H8-3,14.3
            [13,14,15], #H8-4,14.4
            [29], #H8-4,14.5
            [13,14,15], #H7,15.1
            [15,16,17], #H7-2,15.2
        ]
        AllAVGanimals= [
            [6.1], #G6,6.1
            [6.2], #G6-2,6.2
            [7.1], #G7,7.1  
            [7.2], #G7-2,7.2
            [7.3], #G7-3,7.3
            [7.4], #G7-4,7.4
            [8.1], #G8,8.1  
            [8.2], #G8-2,8.2
            [8.3], #G8-3,8.3
            [8.4], #G8-4,8.4
            [9.1], #H2,9.1 
            [9.2], #H2-2,9.2
            [9.3], #H2-3,9.3
            [10.1], #H1,10.1
            [10.2], #H1-2,10.2
            [10.3], #H1-3,10.3
            [10.4], #H1-4,10.4
            [10.5], #H1-5,10.5
            [10.6], #H1-6,10.6
            [11], #H3,11
            [12.1], #H4,12.1
            [12.2], #H4-2,12.2
            [13.1], #H5,13.1  
            [13.2], #H5-2,13.2
            [13.3], #H5-3,13.3
            [13.4], #H5-4,13.4
            [13.5], #H5-5,13.5
            [14.1], #H8,14.1
            [14.2], #H8-2,14.2
	        [14.3], #H8-2,14.3
	        [14.4], #H8-4,14.4
            [14.5], #H8-5,14.5
            [15.1], #H7,15.1
            [15.2], #H7-2,15.2
        ]


    # 5sConstWave1sDura(all trials)
    elif Condidx==4:
        study_ids= [
            'RatTRNG6RsfMRISinglePulse-20230505', #G6,6.1
            'RatTRNG6RsfMRISinglePulse-20230516', #G6-2,6.2
            'RatTRNG7RsfMRISinglePulse-20230510', #G7,7.1  
            'RatTRNG7RsfMRISinglePulse-20230516', #G7-2,7.2
            'RatTRNG7RsfMRISinglePulse-20230622', #G7-3,7.3
            'RatTRNG7RsfMRISinglePulse-20230628', #G7-4,7.4
            'RatTRNG8RsfMRISinglePulse-20230512', #G8,8.1  
            'RatTRNG8RsfMRISinglePulse-20230525', #G8-2,8.2
            'RatTRNG8RsfMRISinglePulse-20230623', #G8-3,8.3
            'RatTRNH2RsfMRISinglePulse-20230514', #H2,9.1 
            'RatTRNH2RsfMRISinglePulse-20230527', #H2-2,9.2
            'RatTRNH2RsfMRISinglePulse-20230623', #H2-3,9.3
            'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
            'RatTRNH1RsfMRISinglePulse-20230529', #H1-2,10.2
            'RatTRNH1RsfMRISinglePulse-20230628', #H1-3,10.3
            'RatTRNH1RsfMRISinglePulse-20230706', #H1-4,10.4
            'RatTRNH1RsfMRISinglePulse-20230710', #H1-5,10.5
            'RatTRNH1RsfMRISinglePulse-20230714', #H1-6,10.6
            'RatTRNH3RsfMRISinglePulse-20230523', #H3,11
            'RatTRNH4RsfMRISinglePulse-20230531', #H4,12.1
            'RatTRNH4RsfMRISinglePulse-20230626', #H4-2,12.2
            'RatTRNH5RsfMRISinglePulse-20230702', #H5,13.1  
            'RatTRNH5RsfMRISinglePulse-20230708', #H5-2,13.2
            'RatTRNH5RsfMRISinglePulse-20230712', #H5-3,13.3
            'RatTRNH5RsfMRISinglePulse-20230718', #H5-4,13.4
            'RatTRNH8RsfMRISinglePulse-20230704', #H8,14.1
            'RatTRNH7RsfMRISinglePulse-20230716', #H7,15.1
            'RatTRNH7RsfMRISinglePulse-20230720', #H7-2,15.2
        ] 


        scan_num= [
            [31,32,33], #G6,6.1
            [31,32,33], #G6-2,6.2
            [31,32,33], #G7,7.1  
            [31,32,33], #G7-2,7.2
            [32,33,34], #G7-3,7.3
            [13], #G7-4,7.4
            [34,35,36], #G8,8.1  
            [35,36,37], #G8-2,8.2
            [33,34,35], #G8-3,8.3
            [31,32,33], #H2,9.1 
            [31,32,33], #H2-2,9.2
            [31,32,33], #H2-3,9.3
            [32,33,34,35], #H1,10.1
            [32,33,34], #H1-2,10.2
            [31,32,33], #H1-3,10.3
            [31,32,33], #H1-4,10.4
            [31,32,33], #H1-5,10.5
            [15], #H1-6,10.6
            [33,34,35], #H3,11
            [31,32,33], #H4,12.1
            [31,32,33], #H4-2,12.2
            [32,33,34], #H5,13.1  
            [31,32,33], #H5-2,13.2
            [31,32,33], #H5-3,13.3
            [30,31,32], #H5-4,13.4
            [31,32,33], #H8,14.1
            [31,32,33], #H7,15.1
            [26], #H7-2,15.2
                    
        ]

        AllAVGanimals= [
            [6.1], #G6,6.1
            [6.2], #G6-2,6.2
            [7.1], #G7,7.1  
            [7.2], #G7-2,7.2
            [7.3], #G7-3,7.3
            [7.4], #G7-4,7.4
            [8.1], #G8,8.1  
            [8.2], #G8-2,8.2
            [8.3], #G8-3,8.3
            [9.1], #H2,9.1 
            [9.2], #H2-2,9.2
            [9.3], #H2-3,9.3
            [10.1], #H1,10.1
            [10.2], #H1-2,10.2
            [10.3], #H1-3,10.3
            [10.4], #H1-4,10.4
            [10.5], #H1-5,10.5
            [10.6], #H1-6,10.6
            [11], #H3,11
            [12.1], #H4,12.1
            [12.2], #H4-2,12.2
            [13.1], #H5,13.1  
            [13.2], #H5-2,13.2
            [13.3], #H5-3,13.3
            [13.4], #H5-4,13.4
            [14.1], #H8,14.1
            [15.1], #H7,15.1
            [15.2], #H7-2,15.2
        ]


        # 2ms 0.625mW
    elif Condidx==5:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                ] 

        scan_num= [
            [39], #G6,6
            [26], #G7,7
            [49], #G8-1, 8.1
            [57], #G8-2, 8.2
            [53], #H2, 9
            [52], #H1,10.1
            [27], #H1,10.2
            [53], #H4,12 
            [8], #H5,13
            [15], #H8,14
            [38], #H7,15
        ] 
        AllAVGanimals= [
            [75]
        ]

        # 2ms 1.25mW
    elif Condidx==6:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [40], #G6,6
            [25], #G7,7
            [48], #G8-1, 8.1
            [56], #G8-2, 8.2
            [52], #H2, 9
            [51], #H1,10.1
            [26], #H1,10.2
            [52], #H4,12 
            [9], #H5,13
            [15], #H8,14
            [38], #H7,15
            ] 
        AllAVGanimals= [
            [75]
        ]


    # 2ms 2.5mW
    elif Condidx==7:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [41], #G6,6
            [24], #G7,7
            [47], #G8-1, 8.1
            [55], #G8-2, 8.2
            [51], #H2, 9
            [53], #H1,10.1
            [25], #H1,10.2
            [51], #H4,12 
            [10], #H5,13
            [16], #H8,14
            [37], #H7,15
            ] 
        AllAVGanimals= [
            [75]
            ]


    # 5ms 0.625mW
    elif Condidx==8:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [53], #G6,6
            [27], #G7,7
            [53], #G8-1, 8.1
            [46], #G8-2, 8.2
            [42], #H2, 9
            [39], #H1,10.1
            [28], #H1,10.2
            [42], #H4,12 
            [19], #H5,13
            [9], #H8,14
            [39], #H7,15
            ] 

        AllAVGanimals= [
            [75]
        ]



    # 5ms 1.25mW
    elif Condidx==9:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [52], #G6,6
            [28], #G7,7
            [54], #G8-1, 8.1
            [47], #G8-2, 8.2
            [43], #H2, 9
            [40], #H1,10.1
            [29], #H1,10.2
            [43], #H4,12 
            [18], #H5,13
            [10], #H8,14    
            [40], #H7,15
            ] 

        AllAVGanimals= [
            [75]
            ]


    # 5ms 2.5mW
    elif Condidx==10:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [51], #G6,6
            [28], #G7,7
            [55], #G8-1, 8.1
            [48], #G8-2, 8.2
            [44], #H2, 9
            [41], #H1,10.1
            [30], #H1,10.2
            [44], #H4,12 
            [17], #H5,13
            [11], #H8,14  
            [41], #H7,15
            ] 

        AllAVGanimals= [
            [75]
            ]


    # 20ms 0.625mW
    elif Condidx==11:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [47], #G6,6
            [20], #G7,7
            [44], #G8-1, 8.1
            [45], #G8-2, 8.2
            [41], #H2, 9
            [47], #H1,10.1
            [21], #H1,10.2
            [41], #H4,12 
            [20], #H5,13
            [20], #H8,14  
            [32], #H7,15
            ]

        AllAVGanimals= [
            [75]
        ]



    # 20ms 1.25mW
    elif Condidx==12:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [46], #G6,6
            [19], #G7,7
            [45], #G8-1, 8.1
            [44], #G8-2, 8.2
            [40], #H2, 9
            [46], #H1,10.1
            [20], #H1,10.2
            [40], #H4,12 
            [21], #H5,13
            [19], #H8,14
            [31], #H7,15
            ]

        AllAVGanimals= [
            [75]
        ]



    # 20ms 2.5mW
    elif Condidx==13:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [45], #G6,6
            [18], #G7,7
            [46], #G8-1, 8.1
            [43], #G8-2, 8.2
            [39], #H2, 9
            [45], #H1,10.1
            [19], #H1,10.2
            [39], #H4,12 
            [22], #H5,13
            [18], #H8,14    
            [30], #H7,15
            ] 

        AllAVGanimals= [
            [75]
        ]


    # 100ms 0.625mW
    elif Condidx==14:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [44], #G6,6
            [16], #G7,7
            [50], #G8-1, 8.1
            [52], #G8-2, 8.2
            [50], #H2, 9
            [49], #H1,10.1
            [17], #H1,10.2
            [48], #H4,12 
            [13], #H5,13
            [14], #H8,14  
            [28], #H7,15
            ] 

        AllAVGanimals= [
            [75]
        ]


    # 100ms 1.25mW
    elif Condidx==15:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [43], #G6,6
            [15], #G7,7
            [51], #G8-1, 8.1
            [53], #G8-2, 8.2
            [49], #H2, 9
            [48], #H1,10.1
            [16], #H1,10.2
            [49], #H4,12 
            [12], #H5,13
            [27], #H7,14
            [13], #H8,15
            ] 

        AllAVGanimals= [
            [75]
        ]


    # 100ms 2.5mW
    elif Condidx==16:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [42], #G6,6
            [17], #G7,7
            [52], #G8-1, 8.1
            [54], #G8-2, 8.2
            [48], #H2, 9
            [50], #H1,10.1
            [18], #H1,10.2
            [50], #H4,12 
            [11], #H5,13
            [12], #H8,14
            [29], #H7,15
            ] 

        AllAVGanimals= [
            [75]
        ]



    # 800ms 0.625mW
    elif Condidx==17:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [50], #G6,6
            [21], #G7,7
            [56], #G8-1, 8.1
            [51], #G8-2, 8.2
            [45], #H2, 9
            [42], #H1,10.1
            [22], #H1,10.2
            [47], #H4,12 
            [14], #H5,13
            [21], #H8,14
            [33], #H7,15
            ] 

        AllAVGanimals= [
            [75]
            ]


    # 800ms 1.25mW
    elif Condidx==18:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [49], #G6,6
            [22], #G7,7
            [57], #G8-1, 8.1
            [50], #G8-2, 8.2
            [46], #H2, 9
            [43], #H1,10.1
            [23], #H1,10.2 
            [46], #H4,12 
            [15], #H5,13
            [22], #H8,14
            [34], #H7,15
            ] 

        AllAVGanimals= [
            [75]
        ]

    # 800ms 2.5mW
    elif Condidx==19:

        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [48], #G6,6
            [23], #G7,7
            [58], #G8-1, 8.1
            [49], #G8-2, 8.2
            [47], #H2, 9
            [44], #H1,10.1
            [24], #H1,10.2
            [45], #H4,12 
            [16], #H5,13
            [23], #H8,14
            [34], #H7,15
            ] 

        AllAVGanimals= [
            [75]
        ]


    # 8Hz3sPulsetrain
    elif Condidx==20:
        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [37], #G6,6
            [11], #G7,7
            [40], #G8-1, 8.1
            [41], #G8-2, 8.2
            [37], #H2, 9
            [54], #H1,10.1
            [9], #H1,10.2
            [37], #H4,12 
            [23], #H5,13
            [24], #H8,14
            [23], #H7,15
            ] 

        AllAVGanimals= [
            [71]
        ]


    # 1Hz12sPulsetrain
    elif Condidx==21:
        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [38], #G6,6
            [12], #G7,7
            [41], #G8-1, 8.1
            [42], #G8-2, 8.2
            [38], #H2, 9
            [55], #H1,10.1
            [10], #H1,10.2
            [38], #H4,12 
            [24], #H5,13
            [25], #H8,14
            [24], #H7,15
            ] 

        AllAVGanimals= [
            [71]
            ]


    # 40Hz8mspulsetrain
    elif Condidx==22:
        study_ids= [
                    'RatTRNG7RsfMRISinglePulse-20230628', #G7,7
                    'RatTRNH1RsfMRISinglePulse-20230714', #H1,10.2
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    'RatTRNH7RsfMRISinglePulse-20230720', #H7,15
                    ] 

        scan_num= [
            [14], #G7,7
            [14], #H1,10.2
            [25], #H5,13
            [26], #H8,14
            [25], #H7,15
            ] 

        AllAVGanimals= [
            [71]
        ]


    # 8Hz3sCstAmpSineWave
    elif Condidx==23:
        study_ids= [
                    'RatTRNG6RsfMRISinglePulse-20230505', #G6,6
                    'RatTRNG8RsfMRISinglePulse-20230512', #G8-1, 8.1
                    'RatTRNG8RsfMRISinglePulse-20230525', #G8-2, 8.2
                    'RatTRNH2RsfMRISinglePulse-20230514', #H2, 9
                    'RatTRNH1RsfMRISinglePulse-20230518', #H1,10.1
                    'RatTRNH4RsfMRISinglePulse-20230531', #H4,12 
                    'RatTRNH5RsfMRISinglePulse-20230722', #H5,13
                    'RatTRNH8RsfMRISinglePulse-20230722', #H8,14
                    ] 

        scan_num= [
            [55], #G6,6
            [43], #G8-1, 8.1
            [58], #G8-2, 8.2
            [54], #H2, 9
            [56], #H1,10.1
            [54], #H4,12 
            [29], #H5,13
            [30], #H8,14
            ] 

        AllAVGanimals= [
            [71]
        ]

    return study_ids, scan_num, AllAVGanimals


condition_names = [
  '8HzSineWave3sOn0.5sUp2.5sDown_2', #1
  '1HzSineWave12sOn18sOff_2', 
  '40HzSineWave10sOn20sOff_2',
  '5sConstWave1sDura_2',
  '2ms0.625mW', #5
  '2ms1.25mW',
  '2ms2.5mW',
  '5ms0.625mW',
  '5ms1.25mW',
  '5ms2.5mW', #10
  '20ms0.625mW',
  '20ms1.25mW',
  '20ms2.5mW',
  '100ms0.625mW',
  '100ms1.25mW', #15
  '100ms2.5mW',
  '800ms0.625mW',
  '800ms1.25mW',
  '800ms2.5mW',
  '8Hz3sPulsetrain', #20
  '1Hz12sPulsetrain',
  '40Hz8mspulsetrain',
  '8Hz3sCstAmpSineWave',    
]



# configuration of the pipeline
import os

#directory
class configuration():
    def __init__(self):
        #directory
        self.root_dir = r'D:\Xunda\data'
        self.pathseed = os.path.join(self.root_dir, r'ROI_RatTRNH1-20230518')
        self.pathroi = os.path.join(self.root_dir, r'Atlas-based_ROIs_TRNorVSfMRI')
        self.raw_path = os.path.join(self.root_dir, r'RatTRNH5RsfMRISinglePulse-20230722')
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
        self.Taskindex = 0
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
        
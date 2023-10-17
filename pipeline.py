import numpy as np
import os
import torch
from torchvision import transforms as T
from torchvision.transforms import functional as TF
from torchvision import utils as vutils
import inspect
import itertools
import time
import nibabel as nib
from matplotlib import pyplot as plt
from tqdm import tqdm
from scipy import io as scio
import pandas as pd
from functools import partial
from prettytable import PrettyTable

import utils
from configs import configuration, condition_names, get_study_ids_and_scan_nums

def GenCCMap_v10_NoFilterMulSeedsTaskRegressedMotionRegressedBP(
    netname,
    ROIname, 
    pathseed,
    pathroi,
    path1,
    raw_path,
    iifiles, 
    prefix,
    DIM,
    VOX,
    outexcel, 
    TR,
    T2,
    GSindex,
    CCMapmaskindex,
    timep,
    filter,
    Taskindex,
    TaskmeanEPITrial,
    AtlasbasedROIregres,
    Motionregres,
    bandwidth,
    fs,
    filter_order,
    gaussian_kernel,
    gaussian_sigma,
    average_path = None,
    condition = None,
    overlay_thrmin = 0.1,
    overlay_thrmax = 1,
    ):
    #total time: 1800.8250391483307
    #setting parameters
    fs = 1/TR
    device = torch.device('cuda')
    current_dir = '.'       #parameter for adaption from matlab
    
    #read all seed masks
    LargerROI = torch.zeros((*DIM[0:3], len(netname))).to(device)
    
    #initializing parameters
    Seed = torch.zeros((*DIM[0:3], len(netname))).to(device)
    fcs = [[0.005, 0.1],[0.005, 0.05], [0.05, 0.1], [0.1, 0.3], [0.3, 0.5]]
    
    #initializing filters
    if bandwidth >= 0:
        fc = fcs[bandwidth]
        bp_filter = utils.filter('bandpass', fs, fc, filter_order, device)   
    if gaussian_sigma > 0:    
        gaussian = T.GaussianBlur(kernel_size=gaussian_kernel, sigma=gaussian_sigma)
    else:
        gaussian = lambda x:x
    


    for net_idx in range(len(netname)):
        current_dir = pathseed
        #read data
        seedmask_name = 'l' + netname[net_idx] + '.img'
        seedmask_dir = os.path.join(current_dir, seedmask_name)
        
        raw_seedmask = np.array(utils.read_bfiles(seedmask_dir))
        Seed[:,:,:,net_idx] = torch.Tensor(np.reshape(raw_seedmask, DIM[0:3], order='F') / np.max(raw_seedmask)).to(device)
        
        #Obtain the larger ROI by extending the seed 3*3 along x and y directions
        ind = torch.where(Seed[:,:,:,net_idx]) 
        LargerROI[ind[0][0]-2:ind[0][3]+3, ind[1][0]-2:ind[1][1]+3, ind[2][0], net_idx] = 1
    
    LargerROI = torch.Tensor(LargerROI).to(device)
    
    #read Atlas based ROIs
    if Taskindex == 1:
        AtlasbasedROI = np.zeros((*DIM[0:3], len(ROIname)))
        for ROI_idx in range(len(ROIname)):
            current_dir = pathroi
            ROImask_name = ROIname[ROI_idx] + '.img'
            ROImask_dir = os.path.join(current_dir, ROImask_name)
            raw_ROImask = np.array(utils.read_bfiles(ROImask_dir))
            AtlasbasedROI[:,:,:, ROI_idx] = np.reshape(raw_ROImask, DIM[0:3], order='F')/np.max(raw_ROImask)
        AtlasbasedROI = torch.Tensor(AtlasbasedROI).to(device)
    
    #Read CCMapmask / to focus the calculation within the brain
    if CCMapmaskindex == 1:
        current_dir = path1
        CCMapmask_dir = os.path.join(current_dir, 'lrrsfra2dseq.img')
        raw_CCMapmask = np.array(utils.read_bfiles(CCMapmask_dir))
        SBAmask = np.reshape(raw_CCMapmask, DIM[0:3], order='F')/np.max(raw_CCMapmask)
        SBAmask = torch.Tensor(SBAmask).to(device)
    
    #Read GSRmask / to perform Global Signal Regression
    if GSindex == 1:
        current_dir = path1
        GSmask_dir = os.path.join(current_dir, 'lrrsfra2dseq.img')
        GSmask_raw = np.array(utils.read_bfiles(GSmask_dir))
        GSmask = np.reshape(GSmask_raw, DIM[0:3], order='F')/np.max(GSmask_raw)
        GSmask = torch.Tensor(GSmask).to(device)
        
    #Initialize the data structure
    CCmap = torch.zeros((*DIM[0:3], len(netname), len(iifiles))).to(device)
    CCvalue1 = torch.zeros((len(netname), len(netname), len(iifiles))).to(device)
    MeanAllRoiCCmap = torch.zeros((*DIM[0:3], len(iifiles))).to(device)
    seedtimecourse = torch.zeros(DIM[3], len(iifiles), len(netname)).to(device)
    
    #Extract mean responses of Local ROI (larger than seed) from across-trial averaged EPI
    if Taskindex == 1:
        
        #read crosstrial-everaged EPI
        if average_path is None:
            trialnum = TaskmeanEPITrial
                
            directory = os.path.join(path1, str(trialnum))  if filter == 0.1 else os.path.join(path1, str(trialnum), 'NoFilter')
        else:
            trialnum = TaskmeanEPITrial
            directory = os.path.join(average_path,'Inter-Animal',str(trialnum))  if filter == 0.1 else os.path.join(path1, str(trialnum), 'NoFilter')
        current_dir = directory
        file_dir = os.path.join(current_dir, prefix+'.img')
        meanEPIdata = np.array(utils.read_bfiles(file_dir, type_data='h'))
        meanEPIdata = np.reshape(meanEPIdata, DIM, order='F')
        meanEPIdata = torch.Tensor(meanEPIdata).to(device)
        DIM[3] = len(timep)
        
        #generate ROImean time course for each large ROI
        ROImeanResponse = torch.zeros((DIM[3], len(netname)))
        for net_idx in range(len(netname)):
            if AtlasbasedROIregres == 1:
                ROImeanResponse[:,net_idx] = torch.sum(AtlasbasedROI[:,:,:,net_idx].unsqueeze(-1) * meanEPIdata, dim=(0,1,2)) / torch.sum(AtlasbasedROI[:,:,:,net_idx], dim=(0,1,2))
            else:
                ROImeanResponse[:,net_idx] = torch.sum(LargerROI[:,:,:,net_idx].unsqueeze(-1) * meanEPIdata, dim=(0,1,2)) / torch.sum(LargerROI[:,:,:,net_idx], dim=(0,1,2))

            #normalize
            mean_ROI = torch.mean(ROImeanResponse[:, net_idx], dim=0)
            ROImeanResponse[:,net_idx] -= mean_ROI
    
    seedtimecourse = torch.zeros(DIM[3], len(iifiles), len(netname)).to(device)
    for iifile_idx in range(len(iifiles)):
        # go to rs data directory
        RS_dir = os.path.join(path1, str(iifiles[iifile_idx])) if filter == 0.1 else os.path.join(path1, str(iifiles[iifile_idx]), 'NoFilter')           
        current_dir = RS_dir
        RS_file = os.path.join(current_dir, prefix+'.img')
        #read rs data
        RS_raw = np.array(utils.read_bfiles(RS_file, type_data='h'))
        RS_raw = np.reshape(RS_raw, DIM, order='F')
        RSdata = RS_raw[:,:,:, timep]
        origin_DIM3 = DIM[3]
        DIM[3] = len(timep)
        RSdata = torch.Tensor(RSdata).to(device)
        #Motion regression using the matrix generated by realignment
        if Motionregres == 1:
            rpdir = os.path.join(raw_path, 'Results',str(iifiles[iifile_idx]))
            current_dir = rpdir
            rpfdir = os.path.join(current_dir, 'rp_sa2dseq.txt')
            rp = np.loadtxt(rpfdir)
            rp = torch.Tensor(rp).to(device)
            #construct regresson basis function
            RegBasFuc= torch.cat([torch.ones(rp.shape[0],1, device=device), rp], axis=1)
            
            #regression for head motion
            # data_ready_regress = utils.fmask(RSdata, SBAmask)
            data_ready_regress = RSdata
            data_ready_regress[torch.where(torch.isnan(data_ready_regress))] = 0
            
            for x, y, z in zip(*torch.where(SBAmask > 0)):
                Beta, Residuals = utils.regress(torch.unsqueeze(data_ready_regress[x, y, z, :], 1), RegBasFuc)
                data_ready_regress[x, y, z,:] = (Residuals + Beta[0]).reshape(1,-1)
            
            if CCMapmaskindex == 1:
                data_regressout = data_ready_regress * SBAmask.unsqueeze(-1)
                RSdata = data_regressout

            
        #global regression
        if GSindex == 1:
            #extract global signal
            GS = torch.sum((GSmask.unsqueeze(-1) * RSdata), dim=[0,1,2])/torch.sum(GSmask, dim=[0,1,2])

            file_name = 'globalsignal' + prefix +'.mat'
            utils.save_mat(os.path.join(current_dir, file_name), GS.cpu().numpy())
            
            #27 seconds
            for z in range(RSdata.shape[2]):
                for y in range(RSdata.shape[1]):
                    for x in range(RSdata.shape[0]):
                        beta, Residuals = utils.regress(torch.unsqueeze(RSdata[x, y, z, :], 1), GS.unsqueeze(1))
                        RSdata[x, y, z, :] = Residuals.reshape(-1)
            
            file_name = 'gs_smooth' + prefix +'.mat'
            #utils.save_mat(os.path.join(current_dir, file_name), RSdata.cpu().numpy())
        #Normalize rs data
        mean_image = RSdata.mean(dim = 3)
        RSdata = RSdata - mean_image.unsqueeze(-1)
        
        #mask
        if CCMapmaskindex == 1:
            RSdata = SBAmask.unsqueeze(-1) * RSdata
        
        #bandpass filter
        
        if bandwidth >= 0:
            #12 seconds
            RSdata = bp_filter.filter(RSdata)
            
        #2D spatial smoothing
        RSdata = torch.permute(RSdata, (3,2,0,1))
        RSdata = gaussian(RSdata)
        RSdata = torch.permute(RSdata, (2,3,1,0))
        
        if CCMapmaskindex == 1:
            RSdata = SBAmask.unsqueeze(-1) * RSdata
                     
        #creating saving directory
        #Add the specific part of the directory name based on the GSindex
        common_dir = 'CCMaps' if GSindex == 1 else 'CCMaps_NGSR'
        #Add the specific part of the directory name based on the filter
        if filter == 0.5:
            common_dir = os.path.join('NoFilter', common_dir)
            
        #Add the specific part of the directory name based on the AtlasbasedROIregres
        if Taskindex == 1:
            common_dir = os.path.join(common_dir, 'TaskRegres') if AtlasbasedROIregres == 1 else os.path.join(common_dir, 'TaskRegresSingleAnimal')
        #Add the specific part of the directory name based on the Motionregres
        if Motionregres == 1:
           common_dir = os.path.join(common_dir, 'MotionReg')
        #Add the specific part of the directory name based on the bandwidth   
        common_dir = os.path.join(common_dir, '{}-{}Hz'.format(fc[0], fc[1])) if bandwidth in configs.frequenctly_changed_parameters['bandwidth'] else common_dir
        #Add the specific part of the directory name based on the smoothing
        if gaussian_sigma > 0:
            common_dir = os.path.join(common_dir, 'smooth')

        dir_name = common_dir
        #Create the directory
        utils.create_folder(os.path.join(path1, '{}'.format(iifiles[iifile_idx]), dir_name))
        
        #11seconds
        save_folder = os.path.join(path1, '{}'.format(iifiles[iifile_idx]), dir_name)
        current_dir = save_folder
        for net_idx in tqdm(range(len(netname)), desc='Cal Maps... Trial {}... Network {}'.format(iifiles[iifile_idx], outexcel)):
            #Extract Seed
            Seedv = torch.sum(Seed[:,:,:,net_idx].unsqueeze(-1)*RSdata, dim=(0,1,2)) / torch.sum(Seed[:,:,:,net_idx], dim=(0,1,2))
            
            #regress task-evoked activations out from the seed time course 
            if Taskindex == 1:
                _, Seedv = utils.regress(Seedv.unsqueeze(1), ROImeanResponse[:,net_idx].unsqueeze(1))
            
            #save Seed Time Course
            seedtimecourse[:,iifile_idx, net_idx] = Seedv
            
            #Calculate CCmap
            CCmap[:,:,:, net_idx, iifile_idx] = torch.sum(Seedv.reshape((1,1,1,-1))*RSdata, dim=3)/(torch.norm(Seedv, dim=0) * torch.norm(RSdata, dim=3)+1e-6)
            
            #save CCmap
            file_dir = os.path.join(current_dir, 'CCmap_{}.mat'.format(netname[net_idx])) if gaussian_sigma == 0 else os.path.join(current_dir, 'CCmap_{}_smooth.mat'.format(netname[net_idx]))
            utils.save_mat(file_dir, CCmap[:,:,:,net_idx, iifile_idx].cpu().numpy())
            
            #Save Overlay
            T2_img = utils.read_bfiles(T2, type_data='h')
            T2_img = np.reshape(T2_img, (128, 128, DIM[2]), order='F')
            T2_img = torch.Tensor(T2_img).to(device)
            structv = T2_img[25:103, 25:103, :]
            ovCCmap = CCmap[25:103, 25:103, :, net_idx, iifile_idx]
            
            overlays = []
            for z in range(DIM[2]):
                overlay = torch.zeros((3, 78, 78)).to(device)
                ovCCmap_z = ovCCmap[:,:,z]
                minus_idx = torch.where(ovCCmap_z < -overlay_thrmin)
                positive_idx = torch.where(ovCCmap_z > overlay_thrmin)

                overlay[:] = torch.round(structv[:,:,z]/128).to(device)
                
                ovCCmap_z = (abs(ovCCmap_z)-overlay_thrmin)/(overlay_thrmax-overlay_thrmin)
                # < -thrmin
                overlay[0, minus_idx[0], minus_idx[1]] = 0
                overlay[1, minus_idx[0], minus_idx[1]] = torch.round(ovCCmap_z[minus_idx[0], minus_idx[1]] * 255)
                overlay[2, minus_idx[0], minus_idx[1]] = 255-overlay[1, minus_idx[0], minus_idx[1]]
                #[0-> 1][red yellow]
                #>thrmin
                overlay[0, positive_idx[0], positive_idx[1]] = 255
                overlay[1, positive_idx[0], positive_idx[1]] = torch.round(ovCCmap_z[positive_idx[0], positive_idx[1]] * 255)
                overlay[2, positive_idx[0], positive_idx[1]] = 0
                
                #rotation and flip
                overlay = TF.vflip(overlay)
                overlay = TF.rotate(overlay, -90)

                overlays.append(overlay)

            #save images
            overlays = torch.stack(overlays)
            imgs_save = vutils.make_grid(overlays, normalize=True, value_range=(0, 255), nrow = overlays.shape[0], padding=0)
            file_name = os.path.join(current_dir, '{}.tif'.format(netname[net_idx])) if gaussian_sigma == 0 else os.path.join(current_dir, '{}_smooth.tif'.format(netname[net_idx]))
            vutils.save_image(imgs_save, file_name)
            
            #Extract CCvalue %%Contralateral
            CCvalue1[net_idx,:, iifile_idx] = torch.sum(CCmap[:,:,:, net_idx, iifile_idx].unsqueeze(-1) * LargerROI, dim=(0,1,2))/ torch.sum(LargerROI, dim=(0,1,2))
        
        #Save Mean All ROIs
        MeanAllRoiCCmap[:,:,:, iifile_idx] = torch.mean(CCmap[:,:,:,:,iifile_idx], dim = 3)
        file_name = os.path.join(current_dir, 'CCmapMeanAll.mat') if gaussian_sigma == 0 else os.path.join(current_dir, 'CCmapMeanAll_smooth.mat')
        utils.save_mat(file_name, MeanAllRoiCCmap[:,:,:, iifile_idx].cpu().numpy())
        del RSdata
        DIM[3] = origin_DIM3
    
    #average output
    #Add the specific part of the directory name based on the filter
    common_dir2 = 'MeanCCMaps2_Nofilter' if filter == 0.5 else 'MeanCCMaps2'
    
    #Add the specific part of the directory name based on the GSindex
    common_dir2 = common_dir2 + '_NGSR' if GSindex == 0 else common_dir2
        
    if Taskindex == 1:
        #Add the specific part of the directory name based on the AtlasbasedROIregres
        common_dir2 = common_dir2 + '_TaskRegres' if AtlasbasedROIregres == 1 else common_dir2 + '_TaskRegresSingleAnimal'
    
    #Add the specific part of the directory name based on the Motionregres
    common_dir2 = common_dir2 + '_MotionReg' if Motionregres == 1 else common_dir2
    
    #Add the specific part of the directory name based on the bandwidth
    common_dir2 = common_dir2 + '_{}-{}Hz'.format(fc[0], fc[1]) if bandwidth in configs.frequenctly_changed_parameters['bandwidth'] else common_dir2
    
    #Add the specific part of the directory name based on the smoothing
    common_dir2 = common_dir2 + '_smooth' if gaussian_sigma > 0 else common_dir2
    
    #Add the specific part of the directory name based on the condition
    common_dir2 = common_dir2 + '_{}'.format(condition) if condition is not None else common_dir2
    
    dir_name2 = common_dir2
    
    current_dir = os.path.join(path1, dir_name2)
    utils.create_folder(current_dir)
    
    #average mean all
    mean_ALLCC = torch.mean(MeanAllRoiCCmap, dim=3)
    file_dir = os.path.join(current_dir, 'MeanCCmapAll.mat') if gaussian_sigma == 0 else os.path.join(current_dir, 'MeanCCmapALL_smooth.mat')
    utils.save_mat(file_dir, mean_ALLCC.cpu().numpy())
    
    for net_idx in range(len(netname)):
        file_dir = os.path.join(current_dir, 'MeanCCmap_{}.mat'.format(netname[net_idx])) if gaussian_sigma == 0 else os.path.join(current_dir, 'MeanCCmap_{}_smooth.mat'.format(netname[net_idx]))
        mean_netwise = torch.mean(CCmap[:,:,:,net_idx, :], dim=3)
        utils.save_mat(file_dir, mean_netwise.cpu().numpy())
    
    #save Mean Overlay   
    for net_idx in range(len(netname)):
        ovCCmap = torch.mean(CCmap[25:103,25:103, :, net_idx, :], 3)
        overlays = []
        for z in range(DIM[2]):
            overlay = torch.zeros((3, 78, 78)).to(device)
            ovCCmap_z = ovCCmap[:,:,z]
            minus_idx = torch.where(ovCCmap_z < -overlay_thrmin)
            positive_idx = torch.where(ovCCmap_z > overlay_thrmin)

            overlay[:] = torch.round(structv[:,:,z]/128).to(device)
            
            ovCCmap_z = (abs(ovCCmap_z)-overlay_thrmin)/(overlay_thrmax-overlay_thrmin)
            #bgr rgb
            # < -thrmin
            overlay[0, minus_idx[0], minus_idx[1]] = 0
            overlay[1, minus_idx[0], minus_idx[1]] = torch.round(ovCCmap_z[minus_idx[0], minus_idx[1]] * 255)
            overlay[2, minus_idx[0], minus_idx[1]] = 255-overlay[1, minus_idx[0], minus_idx[1]]
            #[0-> 1][red yellow]
            #>thrmin
            overlay[0, positive_idx[0], positive_idx[1]] = 255
            overlay[1, positive_idx[0], positive_idx[1]] = torch.round(ovCCmap_z[positive_idx[0], positive_idx[1]] * 255)
            overlay[2, positive_idx[0], positive_idx[1]] = 0
            
            #rotation and flip
            overlay = TF.vflip(overlay)
            overlay = TF.rotate(overlay, -90)

            overlays.append(overlay)
            
        #save images
        overlays = torch.stack(overlays)
        imgs_save = vutils.make_grid(overlays, normalize=True, value_range=(0, 255), nrow = overlays.shape[0], padding=0)
        filename = os.path.join(current_dir, 'MeanCCmap_{}.tif'.format(netname[net_idx])) if gaussian_sigma == 0 else os.path.join(current_dir, 'MeanCCmap_{}_smooth.tif'.format(netname[net_idx]))
        vutils.save_image(imgs_save, filename)
        
        
        
        #---------------save CC values fo SeedROIs---------------
        excel_name = outexcel + '.xlsx' if gaussian_sigma == 0 else outexcel + '_smooth.xlsx'
        with pd.ExcelWriter(os.path.join(current_dir, excel_name)) as writer:
            #Write CCvalues to xls
            for net_idx in range(len(netname)):
                sheet_name = 'CCvalue'+ netname[net_idx]
                data = pd.DataFrame(CCvalue1[net_idx, :, :].cpu().numpy(), index=netname, columns=iifiles)
                data.to_excel(writer, sheet_name=sheet_name)

            #Write seedTC to xls
            for net_idx in range(len(netname)):
                sheet_name = 'TC' + netname[net_idx]
                data = pd.DataFrame(seedtimecourse[:,:,net_idx].cpu().numpy(), index=list(range(1,DIM[3]+1)), columns=iifiles)
                data.to_excel(writer, sheet_name=sheet_name)
            
            #write ROITC to xls
            if Taskindex == 1:
                sheet_name = 'TC_AllROIs'
                data = pd.DataFrame(ROImeanResponse.cpu().numpy, index = list(range(1,DIM[3]+1)), columns=net_idx)
                

if __name__ == '__main__':
    configs = configuration()
    all_start = time.time()
    # setting kwargs
    configs.pathroi = os.path.join(configs.root_dir, 'ROI_rsfMRI', 'Atlas-based_ROIs_TRNorVSfMRI')
    for condition_name in condition_names:
        print('Now processing condition: {}'.format(condition_name))
        configs.condition = condition_name
        study_ids, scan_nums, AllAVGanimals = get_study_ids_and_scan_nums(condition_name)
        configs.average_path = os.path.join(configs.root_dir,'AVG', condition_name)
        
        for study_idx, study_id, scan_num in enumerate(zip(study_ids, scan_nums)):
            configs.TaskmeanEPITrial = AllAVGanimals[study_idx][0]
            print('Now processing study_id: {}, scan_num: {}'.format(study_id, scan_num))
            #setting study_id and scan_num
            configs.raw_path = os.path.join(configs.root_dir, study_id)
            configs.pathseed = os.path.join(configs.root_dir, 'ROI_rsfMRI','ROI_'+study_id)
            #parameters_name_to_change = ['GSindex', 'CCMapmaskindex', 'AtlasbasedROIregres', 'Motionregres', 'gaussian_sigma','bandwidth']
            parameters_name_to_change = ['bandwidth'] # 
            if len(parameters_name_to_change) == 0:
                parameters_name_to_change = ['no_parameter']
            parameters_to_change =(configs.frequenctly_changed_parameters[param] for param in parameters_name_to_change)
            #for different settings

            
            for setting in itertools.product(*parameters_to_change):
                table = PrettyTable(parameters_name_to_change, title='Current Settings')
                table.add_row(setting)       
                print(table)
                for name in parameters_name_to_change:
                    setattr(configs, name, setting[parameters_name_to_change.index(name)])
                    
                configs.update_config()
                
                kwargs = {}
                for k in inspect.signature(GenCCMap_v10_NoFilterMulSeedsTaskRegressedMotionRegressedBP).parameters.keys():
                        kwargs[k] = getattr(configs, k)
                        

                start = time.time()
                GenCCMap_v10_NoFilterMulSeedsTaskRegressedMotionRegressedBP(**kwargs)
                utils.save_pptx(configs)
                print('time:', time.time()-start)
        
        

    print('all_time',time.time()-all_start)
    
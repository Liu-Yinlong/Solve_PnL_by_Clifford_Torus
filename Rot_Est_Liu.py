import numpy as np
import matplotlib.pyplot as plt 
import scipy
import scipy.linalg
from scipy.spatial.transform import Rotation
import pyvista as pv 
from pyvista.plotting import plotter 
import matplotlib as mpl
import time
import pyvista as pv 
import cupy as cp
from pyvista.plotting import plotter 


def gen_syn_data(num_total,num_outlier,noise_level):
    R_gt=Rotation.random(1)
    x_data_=np.random.random((num_total,3))*2-1
    x_data=x_data_/scipy.linalg.norm(x_data_,axis=1)[:,None]
    y_data=R_gt.apply(x_data)
    for ii,x in enumerate(y_data):
        y=scipy.linalg.null_space(x[None,:])
        y_data[ii,:]=y[:,0]+noise_level*np.random.randn(1,3)

    y_outlier_=np.random.random((num_outlier,3))*2-1
    y_outlier=y_outlier_/scipy.linalg.norm(y_outlier_,axis=1,keepdims=True)
    y_data[0:num_outlier,:]=y_outlier
    
    return x_data,y_data,R_gt
def gen_axis(x_data,y_data):

    num=x_data.shape[0]
    axis_1=cp.zeros((num,4))
    axis_2=cp.zeros((num,4))
    axis_3=cp.zeros((num,4))
    axis_4=cp.zeros((num,4))
    for ii in range(num):
        x=x_data[ii,:]
        y=y_data[ii,:]

        delta_1=x[1]*y[2]-x[2]*y[1]
        delta_2=x[1]*y[2]+x[2]*y[1]
        delta_3=x[2]*y[0]-x[0]*y[2]
        delta_4=x[2]*y[0]+x[0]*y[2]
        delta_5=x[0]*y[1]-x[1]*y[0]
        delta_6=x[0]*y[1]+x[1]*y[0]

        M=cp.zeros((4,4))
        M[0,0]=cp.sum(x*y)
        M[1,1]=x[0]*y[0]-x[1]*y[1]-x[2]*y[2]
        M[2,2]=x[1]*y[1]-x[0]*y[0]-x[2]*y[2]
        M[3,3]=x[2]*y[2]-x[1]*y[1]-x[0]*y[0]

        M[0,1]=delta_1
        M[0,2]=delta_3
        M[0,3]=delta_5

        M[1,0]=delta_1
        M[2,0]=delta_3
        M[3,0]=delta_5

        M[1,2]=delta_6
        M[1,3]=delta_4
        M[2,3]=delta_2
        
        M[2,1]=delta_6
        M[3,1]=delta_4
        M[3,2]=delta_2

        _, axis_ii = cp.linalg.eigh(M)
 

        axis_1[ii,:]=axis_ii[:,0] #注意这里转置了！！！！
        axis_2[ii,:]=axis_ii[:,1] #注意这里转置了！！！！
        axis_3[ii,:]=axis_ii[:,2] #注意这里转置了！！！！
        axis_4[ii,:]=axis_ii[:,3] #注意这里转置了！！！！

    return (axis_1,axis_2,axis_3,axis_4)


def rot_estimation(x_data,y_data):

    x_data=cp.asarray(x_data)
    y_data=cp.asarray(y_data)

    ratio=1
    alpha_sampling_num=cp.round(360*ratio).astype(cp.int64)
    beta_sampling_num=cp.round(180*ratio).astype(cp.int64) #<采样一半即可

    alpha_init=cp.linspace(0,2*cp.pi,alpha_sampling_num.item(),endpoint=False)
    beta_init=cp.linspace(0,cp.pi,beta_sampling_num.item(),endpoint=False)

    alpha_,beta_=cp.meshgrid(alpha_init,beta_init)
    alpha=alpha_.reshape((-1,1))
    beta=beta_.reshape((-1,1))

    theta_num=len(alpha)

    input_num=x_data.shape[0]

    blocks=180#<----------------This is the block number for the accumulator

    hist_all=cp.zeros((blocks,blocks,blocks))

    each_size=500

    divided_num=cp.ceil(input_num/each_size).astype(cp.int64)   
                    #< divided inputs number depend on your GPU memory
                    # if "Out of memory allocating", the increase the num
                    # if you have better GPU, decrease this number

    list_ind=cp.array_split(cp.arange(input_num),divided_num.item())

    bins=cp.linspace(-1,1,blocks+1)
    bin=2/blocks

    for list_ii in list_ind:

        list_num=len(list_ii)
        axis_all=gen_axis(x_data[list_ii,:],y_data[list_ii,:])

        axis_1=cp.broadcast_to(axis_all[0],(theta_num,list_num,4))
        axis_2=cp.broadcast_to(axis_all[1],(theta_num,list_num,4))
        axis_3=cp.broadcast_to(axis_all[2],(theta_num,list_num,4))
        axis_4=cp.broadcast_to(axis_all[3],(theta_num,list_num,4))

        k1=cp.cos(alpha).reshape((theta_num,1,1))
        k2=cp.sin(alpha).reshape((theta_num,1,1))
        k3=cp.cos(beta).reshape((theta_num,1,1))
        k4=cp.sin(beta).reshape((theta_num,1,1))

        all_data=(axis_1*k1+axis_2*k2+axis_3*k3+axis_4*k4)/cp.sqrt(2)

    
    #------这个是R3下的计算--------------------------
        ind_positive=cp.where(all_data[:,:,3]<0)
        all_data[ind_positive[0],ind_positive[1],:]*=-1

        all_point_3d=all_data[:,:,0:3]/(1+all_data[:,:,3:4])

        # hist,bin_edge=cp.histogramdd(all_point_3d.reshape((-1,3)),(bins,bins,bins))
 
        pos=cp.floor((all_point_3d+1)/bin).astype(cp.int64)

        for ii in cp.arange(list_num):
            hist_all[pos[:,ii,0],pos[:,ii,1],pos[:,ii,2]]+=1

    ind_=cp.argmax(hist_all)
    ind_xyz=cp.unravel_index(ind_,hist_all.shape)
    
    r_opt=cp.zeros(3)
    r_opt[0]=0.5*(bins[ind_xyz[0]]+bins[ind_xyz[0]+1])
    r_opt[1]=0.5*(bins[ind_xyz[1]]+bins[ind_xyz[1]+1])
    r_opt[2]=0.5*(bins[ind_xyz[2]]+bins[ind_xyz[2]+1])

    r_2=1+cp.sum(r_opt*r_opt)
    v=cp.asarray((2*r_opt[1]/r_2,2*r_opt[2]/r_2,(2-r_2)/r_2,2*r_opt[0]/r_2,)) #<---------- This is because scipy uses{sin(theta)*n cos(theta)} for quaternion

    R_est=Rotation.from_quat((v.get()))

    return R_est


def get_rot_dist(R1,R2):
    R_err=R1.inv()*R2
    err_deg=R_err.magnitude()[0]/np.pi*180
    return err_deg



def test_rot_estimation(num_total,num_outlier,noise_level):
        
    x_data,y_data,R_gt=gen_syn_data(num_total,num_outlier,noise_level)

    tim_start=time.perf_counter_ns()
    R_est=rot_estimation(x_data,y_data)
    tim_end=time.perf_counter_ns()

    tim_duration=(tim_end-tim_start)/1000000    #换算为毫秒
    rot_err=get_rot_dist(R_gt,R_est)            #弧度(degree)

    return rot_err,tim_duration


if __name__=='__main__':
    num_total=1000
    noise_level=0.001
    outlier_list_num=10
    repeat=200
    num_outlier_list=10*np.arange(outlier_list_num)+900
    rot_err=np.zeros((repeat,outlier_list_num))
    tim=np.zeros((repeat,outlier_list_num))

    for ii in range(repeat):
        for jj in range(outlier_list_num):
            rot_err[ii,jj],tim[ii,jj]=test_rot_estimation(num_total,num_outlier_list[jj],noise_level)
            print([ii,jj])
    
    plt.figure(figsize=(3.6,2))
    boxprops = dict(linewidth=0.2,)
    bp=plt.boxplot(rot_err,showfliers=True,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

    # for f in bp['boxes']:
    #     f.set_facecolor('lime')
    # f.set_label('Ours')

    # plt.legend()
    plt.xticks(np.arange(outlier_list_num)+1, labels=[f'{x*10}%' for x in np.arange(outlier_list_num)], rotation=0)
    plt.xlabel('outlier ratio')
    plt.ylabel('Rotation error (deg)')
    plt.tight_layout()
    plt.grid()
    plt.savefig('./save_img/rotation_error_multi-2.pdf')

    plt.figure(figsize=(3.6,2))
    boxprops = dict(linewidth=0.2,)
    bp=plt.boxplot(tim,showfliers=False,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

    # for f in bp['boxes']:
    #     f.set_facecolor('lime')
    # f.set_label('Ours')

    # plt.legend()
    plt.xticks(np.arange(outlier_list_num)+1, labels=[f'{x*10}%' for x in np.arange(outlier_list_num)], rotation=0)
    plt.xlabel('outlier ratio')
    plt.ylabel('Time (ms)')
    plt.tight_layout()
    plt.grid()
    plt.savefig('./save_img/rotation_tim_multi-2.pdf')



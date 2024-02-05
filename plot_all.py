from Rot_Est_Liu import *
import scienceplots
plt.style.use(['science','no-latex'])
mpl.rcParams['font.family']='FreeSans'

################这个是outlier##################

num_total=1000
noise_level=0.001
outlier_list_num=10
repeat=500
num_outlier_list=100*np.arange(outlier_list_num)
rot_err=np.zeros((repeat,outlier_list_num))
tim=np.zeros((repeat,outlier_list_num))

rot_err=np.loadtxt('./save_data/outlier_err.txt')
tim=np.loadtxt('./save_data/outlier_tim.txt')


plt.figure(figsize=(4,3))
boxprops = dict(linewidth=0.2,)
bp=plt.boxplot(rot_err,showfliers=True,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

# for f in bp['boxes']:
#     f.set_facecolor('lime')
# f.set_label('Ours')

# plt.legend()
plt.xticks(np.arange(outlier_list_num)+1, labels=[f'{x*10}%' for x in np.arange(outlier_list_num)], rotation=0)
plt.xlabel('outlier ratio (%)')
plt.ylabel('Rotation error (deg)')
plt.tight_layout()
plt.grid()
plt.savefig('./save_img/rotation_error_outlier.pdf')

plt.figure(figsize=(4,3))
boxprops = dict(linewidth=0.2,)
bp=plt.boxplot(tim,showfliers=False,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

# for f in bp['boxes']:
#     f.set_facecolor('lime')
# f.set_label('Ours')

# plt.legend()
plt.xticks(np.arange(outlier_list_num)+1, labels=[f'{x*10}%' for x in np.arange(outlier_list_num)], rotation=0)
plt.xlabel('outlier ratio (%)')
plt.ylabel('Time (ms)')
plt.tight_layout()
plt.grid()
plt.savefig('./save_img/rotation_tim_outlier.pdf')


#################################################


################这个是high outlier##################

num_total=1000
noise_level=0.001
outlier_list_num=10
repeat=500
num_outlier_list=10*np.arange(outlier_list_num)+900
rot_err=np.zeros((repeat,outlier_list_num))
tim=np.zeros((repeat,outlier_list_num))


rot_err=np.loadtxt('./save_data/high_outlier_err.txt')
tim=np.loadtxt('./save_data/high_outlier_tim.txt')


plt.figure(figsize=(4,3))
boxprops = dict(linewidth=0.2,)
bp=plt.boxplot(rot_err,showfliers=True,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

# for f in bp['boxes']:
#     f.set_facecolor('lime')
# f.set_label('Ours')

# plt.legend()
plt.xticks(np.arange(outlier_list_num)+1, labels=[f'{x+90}%' for x in np.arange(outlier_list_num)], rotation=0)
plt.xlabel('outlier ratio (%)')
plt.ylabel('Rotation error (deg)')
plt.tight_layout()
plt.grid()
plt.savefig('./save_img/rotation_error_high_outlier.pdf')

plt.figure(figsize=(4,3))
boxprops = dict(linewidth=0.2,)
bp=plt.boxplot(tim,showfliers=False,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

# for f in bp['boxes']:
#     f.set_facecolor('lime')
# f.set_label('Ours')

# plt.legend()
plt.xticks(np.arange(outlier_list_num)+1, labels=[f'{x+90}%' for x in np.arange(outlier_list_num)], rotation=0)
plt.xlabel('outlier ratio (%)')
plt.ylabel('Time (ms)')
plt.tight_layout()
plt.grid()
plt.savefig('./save_img/rotation_tim_high_outlier.pdf')


#################################################


################ 这个是input number ##################

noise_level=0.001
input_list_num=10
num_total=np.arange(input_list_num)*500+500

repeat=500

rot_err=np.zeros((repeat,input_list_num))
tim=np.zeros((repeat,input_list_num))

rot_err=np.loadtxt('./save_data/num_err.txt')
tim=np.loadtxt('./save_data/num_tim.txt')


plt.figure(figsize=(4,3))
boxprops = dict(linewidth=0.2,)
bp=plt.boxplot(rot_err,showfliers=True,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

# for f in bp['boxes']:
#     f.set_facecolor('lime')
# f.set_label('Ours')

# plt.legend()
plt.xticks(np.arange(input_list_num)+1, labels=num_total, rotation=45)
plt.xlabel('Number of inputs')
plt.ylabel('Rotation error (deg)')
plt.tight_layout()
plt.grid()
plt.savefig('./save_img/rotation_error_num.pdf')

plt.figure(figsize=(4,3))
boxprops = dict(linewidth=0.2,)
bp=plt.boxplot(tim,showfliers=False,boxprops=boxprops,patch_artist=True,whiskerprops=dict(linewidth=0.5),capprops=dict(linewidth=0.5))

# for f in bp['boxes']:
#     f.set_facecolor('lime')
# f.set_label('Ours')

# plt.legend()
plt.xticks(np.arange(input_list_num)+1, labels=num_total, rotation=45)
plt.xlabel('Number of inputs')
plt.ylabel('Time (ms)')
plt.tight_layout()
plt.grid()
plt.savefig('./save_img/rotation_tim_num.pdf')


#################################################










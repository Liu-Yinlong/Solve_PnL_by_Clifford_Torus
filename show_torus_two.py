import numpy as np 
# import scienceplots
# plt.style.use(['science','no-latex','ieee'])
import pyvista as pv                    #<--------------------注意这个版本是 0.43.3
from pyvista.plotting import plotter    #<--------------------注意这个版本是 0.43.3

# plt.rcParams['font.family']='Work Sans'
np.random.seed(0)

def gen_rand_basis():
    A=np.random.randn(4,4)*2-1
    _, B=np.linalg.eigh(A@A.T)
    return B

def obtain_surface(basis):

    alpha_list=np.linspace(0,np.pi*2,500)
    beta_list=np.linspace(0,np.pi*2,500)

    alpha,beta=np.meshgrid(alpha_list,beta_list)

    sin_alpha=np.sin(alpha)
    cos_alpha=np.cos(alpha)
    sin_beta=np.sin(beta)
    cos_beta=np.cos(beta)
    
    b1=basis[0,0]*cos_alpha+basis[0,1]*sin_alpha+basis[0,2]*cos_beta+basis[0,3]*sin_beta
    b2=basis[1,0]*cos_alpha+basis[1,1]*sin_alpha+basis[1,2]*cos_beta+basis[1,3]*sin_beta
    b3=basis[2,0]*cos_alpha+basis[2,1]*sin_alpha+basis[2,2]*cos_beta+basis[2,3]*sin_beta
    b4=basis[3,0]*cos_alpha+basis[3,1]*sin_alpha+basis[3,2]*cos_beta+basis[3,3]*sin_beta
    
    ind_neg=np.where(b4<0)
    
    b1[ind_neg]=np.nan
    b2[ind_neg]=np.nan
    b3[ind_neg]=np.nan
    b4[ind_neg]=np.nan
    
    data_x=b1/(1+b4)/np.sqrt(2)
    data_y=b2/(1+b4)/np.sqrt(2)
    data_z=b3/(1+b4)/np.sqrt(2)

    return data_x,data_y,data_z

def print_figure_1(data_x,data_y,data_z):
        
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))


    pt=plotter.Plotter()
    sphere = pv.StructuredGrid(x, y, z) 
    torus_1=pv.StructuredGrid(data_x,data_y,data_z)
    pt.add_mesh(sphere,style='wireframe')
    pt.add_mesh(torus_1,style='wireframe',color='fuchsia')
    pt.show()
    return

def print_figure_2(data_x_1,data_y_1,data_z_1,data_x_2,data_y_2,data_z_2):
        
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    pt=plotter.Plotter(off_screen=False)
    sphere = pv.StructuredGrid(x, y, z) 
    torus_1=pv.StructuredGrid(data_x_1,data_y_1,data_z_1)
    torus_2=pv.StructuredGrid(data_x_2,data_y_2,data_z_2)
    pt.add_mesh(sphere,style='wireframe')
    pt.add_mesh(torus_1,style='surface',color='salmon',show_edges=False)
    pt.add_mesh(torus_2,style='surface',color='lime',show_edges=False)

    #####这是绘制动图的#########################
    path = pt.generate_orbital_path(n_points=36,factor=5)
    pt.open_gif("orbit.gif",fps=10)
    pt.orbit_on_path(path, write_frames=True,step=0.05)
    # pt.close()
    ##############################
    pt.show()


    return

if __name__=='__main__':
    b1=gen_rand_basis()
    b2=gen_rand_basis()
    data_x_1,data_y_1,data_z_1=obtain_surface(b1)
    data_x_2,data_y_2,data_z_2=obtain_surface(b2)
    print_figure_2(data_x_1,data_y_1,data_z_1,data_x_2,data_y_2,data_z_2)
















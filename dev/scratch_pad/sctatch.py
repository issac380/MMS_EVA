import pyspedas
import pyspedas as ps
import pytplot as pt
from pyspedas import mms
from pytplot import tplot
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from eva_get_selections_file import eva_get_selections_file

#######  USER SETTINGS ######
probe = '3'
start_date  = '2020-07-11/06:00'
end_date    = '2020-07-12/01:00'
#############################

#================
# Get ABS
#================
# out_files = eva_get_selections_file(start_date=start_date, end_date=end_date)
# abs_file  = out_files[0]
# 
# Eventually, we need to have some code to generate a tplot variable to display ABS.
# The SITLs modify ABS with EVA.
#
#================
# Get Science Data
#================
trange    = [start_date, end_date]
data_rate = 'srvy'
sc        = 'mms'+probe
tvmag     = sc+'_fgm_b_gsm_'+data_rate+'_l2'
tvion = sc+'_dis_energyspectr_omni_fast'
tvvel = sc+'_dis_bulkv_gse_fast'
tvden = sc+'_dis_numberdensity_fast'
tpara = sc+'_dis_temppara_fast'
mms.fgm(trange=trange, probe=probe, time_clip=True, varnames=tvmag)
mms.fpi(trange=trange, probe=probe, time_clip=True, datatype=['dis-moms'], center_measurement=True)

#================
# PLOT
#================
def onClick(event):
    print(event.x, event.y, event.xdata, event.ydata, event.button, event.dblclick)


fig,axes = pt.tplot([tvmag+'_btot', tvmag+'_bvec', tvion, tvden, tvvel, tpara], return_plot_objects=True)
# cursor = Cursor(axes[1], horizOn=False, vertOn=True, color='green', linewidth=2.0)
fig.canvas.mpl_connect('button_press_event', onClick)
plt.show()
from mpl_toolkits.basemap import Basemap, cm
# requires netcdf4-python (netcdf4-python.googlecode.com)
from netCDF4 import Dataset as NetCDFFile
import numpy as np
import matplotlib.pyplot as plt

# plot rainfall from NWS using special SAOitation
# colormap used by the NWS, and included in basemap.

nc = NetCDFFile('./subsuf_timmean_fwppiSGa_sao_1800-6699_yearmean_remapcon_1deg_for_density_setT_0-2400.nc')
# data from http://water.weather.gov/SAO/
prcpvar = nc.variables['SAO'] #*32140800

data = prcpvar[:]
latcorners = nc.variables['lon'][:]
loncorners = -nc.variables['lat'][:]
#lon_0 = -nc.variables['true_lon'].getValue()
#lat_0 = nc.variables['true_lat'].getValue()
# create figure and axes instances
fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.1,0.1,0.8,0.8])
# create polar stereographic Basemap instance.
#m = Basemap(projection='stere',lon_0=lon_0,lat_0=90.,lat_ts=lat_0,\
#            llcrnrlat=latcorners[0],urcrnrlat=latcorners[2],\
#           llcrnrlon=loncorners[0],urcrnrlon=loncorners[2],\
#            rsphere=6371200.,resolution='l',area_thresh=10000)
# draw coastlines, state and country boundaries, edge of map.
lon1=2,-12,-50,-110,-89,
lon2=8,-2,-40,-80,-60
lat1=75,65,50,-5,9
lat2=79,71,60,5,22
for i in np.arange(int(len(lon1))):
	x=np.arange(lon1[i],lon2[i]+1,1)
	y1=0*x+lat1[i]
	plt.plot(x,y1,linewidth=1,color='red')
	y2=0*x+lat2[i]
	plt.plot(x,y2,linewidth=1,color='red')
	y=np.arange(lat1[i],lat2[i]+1,1)
	x1=0*y+lon1[i]
	plt.plot(x1,y,linewidth=1,color='red')
	x2=0*y+lon2[i]
	plt.plot(x2,y,linewidth=1,color='red')




m = Basemap(projection='cyl',llcrnrlat=-89.5,urcrnrlat=89.5,\
            llcrnrlon=-179.5,urcrnrlon=179.5,lat_ts=20,resolution='c')
m.drawcoastlines(linewidth=0.5, linestyle='dashed', color='GreenYellow',\
                 antialiased=1, ax=None, zorder=None)
# draw parallels.
parallels = np.arange(-90.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=8)
# draw meridians
meridians = np.arange(-180.,180.,20.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=8)
ny = 180; nx = 360
lons, lats = m.makegrid(nx, ny)
#get lat/lons of ny by nx evenly space grid.
x, y = m(lons, lats)


from matplotlib.patches import Polygon
m.readshapefile("/Users/zhengkai/slm5/RasterT_Int_slm9_SplitLine3",'states',drawbounds=False)
# m.readshapefile("./slm/land_sea",'states',drawbounds=False)
# m.readshapefile("./CHN_adm/CHN_adm1",'states',drawbounds=False)
for info, shp in zip(m.states_info, m.states):
    # proid = info['NAME_0']
    # if proid == 'China':
        poly = Polygon(shp,facecolor='w',fill=False,edgecolor='k', lw=1.0)
        ax.add_patch(poly)
#compute map proj coordinates.
#draw filled contours.
# clevs = [-2,-1,0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]
#clevs = [-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1]
# clevs = [0,1,5,10,20,30,45,50,70,85,100,130,150,170,190,210,230]
#cs = m.contourf(x,y,prcpvar[0,:,:],clevs,linewidths=0.5,colors='k',animated=True)
clevs = np.arange(33.5,36.3,0.2)
#clevs = [-1,0,0.5,0.75,1,15,20,30,40,70]
lonnumber=360# data.shape[2];
latnumber=180
prcpvar1=np.zeros(shape=(latnumber,lonnumber))

for i in range(int(lonnumber/2),int(lonnumber)):
	prcpvar1[:,i]= prcpvar[0,:,i-int(lonnumber/2)]

for i in range(0,int(lonnumber/2)):
	prcpvar1[:,i]= prcpvar[0,:,i+int(lonnumber/2)]
# print (min(prcpvar[0,:,:]))
cs = m.contourf(x,y,prcpvar1[:,:],clevs,cmap="jet") #plt.cm.cubehelix  cm.s3pcpn "jet" "rainbow" "BrBG" "terrain"
# cs = m.contour(x,y,prcpvar[0,:,:],15,linewidths=1.5)
# add colorbar.
CSBar = m.colorbar(cs,location='bottom',pad="5%")
CSBar.set_label('psu')
# add title
plt.title("subsuf_SAO_SGa_timmean_0-2400")#+prcpvar.long_name
plt.savefig('subsuf_SAO_SGa_timmean_0-2400.png')
plt.show()
# plt.savefig('SAO.png')#  plt show 在前面 叉掉 后面save不存图的内容

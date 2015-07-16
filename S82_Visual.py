try:
	import matplotlib
	matplotlib.use('TkAgg')
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
	from matplotlib.figure import Figure
	import matplotlib.pyplot as plt
	import sys
	import os
	import aplpy
	import numpy as np
	from astropy.io import fits
	from Tkinter import *
except ImportError as error:
	print "You don't have module {0} installed".format(error.message[16:])
	if error.message[16:]=='aplpy':
		print "See {0} documentation for installation details: {1}".format('APLpy','https://aplpy.github.io/')
	if error.message[16:]=='fits':
		print "See {0} documentation for installation details: {1}".format('Astropy','http://www.astropy.org/')
	sys.exit(1)

class Plot:
	
	def __init__(self, master):
		frame1 = Frame(master, bd=2, relief=SUNKEN) 
		frame1.pack(side=LEFT, padx=10)
		self.button1 = Button(frame1, text="Stripe 82 Title", command=self.onClick1)
		self.button1.pack()
		self.button2 = Button(frame1, text="Radio", command=self.onClick2)
		self.button2.pack()
		self.button3 = Button(frame1, text="FIR", command=self.onClick3)
		self.button3.pack()
		self.button4 = Button(frame1, text="MIR", command=self.onClick4)
		self.button4.pack()
		self.button5 = Button(frame1, text="Op/NIR", command=self.onClick5)
		self.button5.pack()
		self.button6 = Button(frame1, text="UV", command=self.onClick6)
		self.button6.pack()
		self.button7 = Button(frame1, text="X-Ray", command=self.onClick7)
		self.button7.pack()
		self.button8 = Button(frame1, text="Save Image", command=self.onClick8)
		self.button8.pack()
		self.button9 = Button(frame1, text="Region Titles OFF", command=self.onClick9)
		self.button9.pack()
		self.button0 = Button(frame1, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
		self.rad_exist, self.fir_exist, self.mir_exist, self.op_nir_exist, self.uv_exist, self.xray_exist, self.save_exist = ([None],[None],[None],[None],[None],[None],[None])
		
		frame2 = Frame(master) 
		frame2.pack(side=LEFT)
		plot_FITS()
		
		global canvas
		canvas = FigureCanvasTkAgg(f, frame2)
		canvas.show()
		canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		
		toolbar = NavigationToolbar2TkAgg(canvas, frame2)
		toolbar.update()
		canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
		
	def onClick1(self,tog=[True]):
		tog[0] = not tog[0]
		if tog[0]:
			fig.show_regions(reg_dir + 'stripe82_title.reg')
			set_title[0]=True
		else:
			set_title[0]=False
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick2(self):
		newWindow("Radio Footprints","300x100+300+300",bands[2],self.rad_exist)

	def onClick3(self):
		newWindow("Far Infrared Footprints","300x75+300+300",bands[3],self.fir_exist)
		
	def onClick4(self):
		newWindow("Mid-Infrared Footprints","300x125+300+300",bands[4],self.mir_exist)
	
	def onClick5(self):
		newWindow("Optical/Near Infrared Footprints","300x150+300+300",bands[5],self.op_nir_exist)
		
	def onClick6(self):
		newWindow("Ultraviolet Footprints","300x100+300+300",bands[6],self.uv_exist)

	def onClick7(self):
		newWindow("X-Ray Footprints","300x125+300+300",bands[7],self.xray_exist)
	
	def onClick8(self):
		newWindow("Save Image","200x175+300+300",bands[8],self.save_exist)
	
	def onClick9(self,tog=[False]):
		tog[0] = not tog[0]
		if tog[0]:
			self.button9.config(text="Region Titles ON")
			set_reg_titles[0]=False
		else:
			self.button9.config(text="Region Titles OFF")
			set_reg_titles[0]=True
		f.clf()
		plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class Radio:
	tog=[False,False]
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="VLA (Hodge 2011)", command=self.onClick1)
		self.button1.pack()
		self.button2 = Button(frame, text="CNSS", command=self.onClick2)
		self.button2.pack()
		self.button0 = Button(frame, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
	
	def onClick1(self,tog=[False]):
		tog[0] = not tog[0]
		if tog[0]:
			display_regions(region_titles=set_reg_titles[0], REG='vla_foot3')
			act_regs.append('vla_foot3')
		else:
			act_regs.remove('vla_foot3')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()

	def onClick2(self,tog=[False]):
		tog[0] = not tog[0]
		if tog[0]:
			display_regions(region_titles=set_reg_titles[0], REG='CNSS_foot2')
			act_regs.append('CNSS_foot2')
		else:
			act_regs.remove('CNSS_foot2')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()

	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class FIR:
	tog=[False]
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="HeLMS and HeRS", command=self.onClick1)
		self.button1.pack()
		self.button0 = Button(frame, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
		

	def onClick1(self):
		self.tog[0] = not self.tog[0]
		if self.tog[0]:
			display_regions(region_titles=set_reg_titles[0], REG='HeLMS_and_HeRS_only')
			act_regs.append('HeLMS_and_HeRS_only')
		else:
			act_regs.remove('HeLMS_and_HeRS_only')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()

	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class MIR:
	tog=[False,False,False]
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="SHELA", command=self.onClick1)
		self.button1.pack()
		self.button2 = Button(frame, text="SpIES (Ch. 1)", command=self.onClick2)
		self.button2.pack()
		self.button3 = Button(frame, text="SpIES (Ch. 2)", command=self.onClick3)
		self.button3.pack()
		self.button0 = Button(frame, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
		

	def onClick1(self):
		self.tog[0] = not self.tog[0]
		if self.tog[0]:
			display_regions(region_titles=set_reg_titles[0], REG='SHELA')
			act_regs.append('SHELA')
		else:
			act_regs.remove('SHELA')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()

	def onClick2(self):
		self.tog[1] = not self.tog[1]
		if self.tog[1]:
			display_regions(region_titles=set_reg_titles[0], REG='SpIES_regions_ch1')
			act_regs.append('SpIES_regions_ch1')
		else:
			act_regs.remove('SpIES_regions_ch1')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick3(self):
		self.tog[2] = not self.tog[2]
		if self.tog[2]:
			display_regions(region_titles=set_reg_titles[0], REG='SpIES_regions_ch2')
			act_regs.append('SpIES_regions_ch2')
		else:
			act_regs.remove('SpIES_regions_ch2')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()

	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class Op_NIR:
	tog=[False,False,False,False]
	
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="SDSS S82", command=self.onClick1)
		self.button1.pack()
		self.button2 = Button(frame, text="HSC", command=self.onClick2)
		self.button2.pack()
		self.button3 = Button(frame, text="DES", command=self.onClick3)
		self.button3.pack()
		self.button4 = Button(frame, text="PRIMUS", command=self.onClick4)
		self.button4.pack()		
		self.button0 = Button(frame, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
	
	def onClick1(self):
		self.tog[0] = not self.tog[0]
		if self.tog[0]:
			display_regions(region_titles=set_reg_titles[0], REG='stripe82')
			act_regs.append('stripe82')
		else:
			act_regs.remove('stripe82')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick2(self):
		self.tog[1] = not self.tog[1]
		if self.tog[1]:
			display_regions(region_titles=set_reg_titles[0], REG='HSC')
			act_regs.append('HSC')
		else:
			act_regs.remove('HSC')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick3(self):
		self.tog[2] = not self.tog[2]
		if self.tog[2]:
			display_regions(region_titles=set_reg_titles[0], REG='DES')
			act_regs.append('DES')
		else:
			act_regs.remove('DES')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick4(self,tog=[False]):
		self.tog[3] = not self.tog[3]
		if self.tog[3]:
			display_regions(region_titles=set_reg_titles[0], REG='PRIMUS_stripe82')
			display_regions(region_titles=set_reg_titles[0], REG='PRIMUS_stripe82_masks')
			act_regs.append('PRIMUS_stripe82')
			act_regs.append('PRIMUS_stripe82_masks')
		else:
			act_regs.remove('PRIMUS_stripe82')
			act_regs.remove('PRIMUS_stripe82_masks')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class UV:
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="GALEX", command=self.onClick1)
		self.button1.pack()
		self.button2 = Button(frame, text="Clear GALEX Footprints", command=self.onClick2)
		self.button2.pack()
		self.button0 = Button(frame, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
		self.im_exist = [None]
		self.leg_exist = [None]
	
	def onClick1(self):
		if self.im_exist[0] is None:
			image = Toplevel()
			image.title('GALEX Survey(s)')
			image.geometry('+650+300')
			entry = Entry(image, bd=3)
			image.bind("<Return>", (lambda event, e=entry: self.survey(e,image)))
			label = Label(image, text="Please enter 'DIS', 'MIS', 'AIS', or 'All' (separated by commas if multiple) for desired survey(s)")
			label.pack(side=LEFT)
			entry.pack(side=LEFT)
			self.im_exist[0] = 1
			image.protocol("WM_DELETE_WINDOW", lambda image=image: existance(image,self.im_exist))
		if self.leg_exist[0] is None:
			legend = Toplevel()
			legend.title('GALEX Survey Legend')
			legend.geometry('225x100+1645+300')
			legend.configure(background='grey20')
			Label(legend, text='AIS', fg='white', bg='grey20', font=('TkDefaultFont',24)).pack()
			Label(legend, text='MIS', fg='red', bg='grey20', font=('TkDefaultFont',24)).pack()
			Label(legend, text='DIS', fg='blue', bg='grey20', font=('TkDefaultFont',24)).pack()
			self.leg_exist[0] = 1
			legend.protocol("WM_DELETE_WINDOW", lambda legend=legend: existance(legend,self.leg_exist))
		
	def survey(self, entry, image):
		surveylist = ['dis','mis','ais']
		surveys = [x.strip().lower() for x in entry.get().split(',')]
		if len(surveys)>1:
			if all((y in surveys for y in surveylist)):
				display_regions(region_titles=set_reg_titles[0], REG='gr67')
				act_regs.append('gr67')
			elif all((y in surveys for y in [surveylist[0],surveylist[1]])):
				display_regions(region_titles=set_reg_titles[0], REG='gr67_mis')
				display_regions(region_titles=set_reg_titles[0], REG='gr67_dis')
				act_regs.append('gr67_mis')
				act_regs.append('gr67_dis')
			elif all((y in surveys for y in [surveylist[0],surveylist[2]])):
				display_regions(region_titles=set_reg_titles[0], REG='gr67_ais')
				display_regions(region_titles=set_reg_titles[0], REG='gr67_dis')
				act_regs.append('gr67_ais')
				act_regs.append('gr67_dis')
			elif all((y in surveys for y in [surveylist[2],surveylist[2]])):
				display_regions(region_titles=set_reg_titles[0], REG='gr67_ais')
				display_regions(region_titles=set_reg_titles[0], REG='gr67_mis')
				act_regs.append('gr67_ais')
				act_regs.append('gr67_mis')	
		else:
			if surveys[0] == 'all':
				display_regions(region_titles=set_reg_titles[0], REG='gr67')
				act_regs.append('gr67')
			if surveys[0] == surveylist[0]:
				display_regions(region_titles=set_reg_titles[0], REG='gr67_dis')
				act_regs.append('gr67_dis')
			if surveys[0] == surveylist[1]:
				display_regions(region_titles=set_reg_titles[0], REG='gr67_mis')
				act_regs.append('gr67_mis')
			if surveys[0] == surveylist[2]:
				display_regions(region_titles=set_reg_titles[0], REG='gr67_ais')
				act_regs.append('gr67_ais')		
		image.destroy()
		self.im_exist[0] = None
		canvas.show()
	
	def onClick2(self):
		for region in act_regs[::-1]:
			if region.startswith('gr67'):
				act_regs.remove(region)
		f.clf()
		plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class XRAY:
	tog=[False]
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="Chandra", command=self.onClick1)
		self.button1.pack()
		self.button2 = Button(frame, text="XMM-Newton", command=self.onClick2)
		self.button2.pack()
		self.button3 = Button(frame, text="Clear Chandra Footprints", command=self.onClick3)
		self.button3.pack()
		self.button0 = Button(frame, text="Clear All Footprints", command=self.onClick0)
		self.button0.pack()
		self.im_exist = [None]
		self.leg_exist = [None]

	def onClick1(self):
		if self.im_exist[0] is None:
			image = Toplevel()
			image.title('Chandra Camera(s)')
			image.geometry('+650+300')
			entry = Entry(image, bd=3)
			image.bind("<Return>", (lambda event, e=entry: self.camera(e,image)))
			label = Label(image, text="Please enter 'ACIS-S', 'ACIS-I', 'HRC-S', 'HRC-I', or 'All' (separated by commas if multiple) for desired survey(s)")
			label.pack(side=LEFT)
			entry.pack(side=LEFT)
			self.im_exist[0] = 1
			image.protocol("WM_DELETE_WINDOW", lambda image=image: existance(image,self.im_exist))
		if self.leg_exist[0] is None:
			legend = Toplevel()
			legend.title('Chandra Camera Legend')
			legend.geometry('225x135+1645+300')
			legend.configure(background='grey20')
			Label(legend, text='ACIS-S', fg='red', bg='grey20', font=('TkDefaultFont',24)).pack()
			Label(legend, text='ACIS-I', fg='blue', bg='grey20', font=('TkDefaultFont',24)).pack()
			Label(legend, text='HRC-S', fg='magenta', bg='grey20', font=('TkDefaultFont',24)).pack()
			Label(legend, text='HRC-I', fg='green2', bg='grey20', font=('TkDefaultFont',24)).pack()
			self.leg_exist[0] = 1
			legend.protocol("WM_DELETE_WINDOW", lambda legend=legend: existance(legend,self.leg_exist))
	
	def camera(self, entry, image):
		cameralist = ['acis-s','acis-i','hrc-s','hrc-i']
		cameras = [x.strip().lower() for x in entry.get().split(',')]
		if len(cameras)>1:
			if all((y in cameras for y in cameralist)):
				display_regions(region_titles=set_reg_titles[0], REG='chandra_foot')
				act_regs.append('chandra_foot')
			elif all((y in cameras for y in [cameralist[0],cameralist[1]])):
				display_regions(region_titles=set_reg_titles[0], REG='chandra_acis-i')
				display_regions(region_titles=set_reg_titles[0], REG='chandra_acis-s')
				act_regs.append('chandra_acis-i')
				act_regs.append('chandra_acis-s')
			elif all((y in cameras for y in [cameralist[2],cameralist[3]])):
				display_regions(region_titles=set_reg_titles[0], REG='chandra_hrc-i')
				display_regions(region_titles=set_reg_titles[0], REG='chandra_hrc-s')
				act_regs.append('chandra_hrc-i')
				act_regs.append('chandra_hrc-s')
		else:
			if cameras[0] == 'all':
				display_regions(region_titles=set_reg_titles[0], REG='chandra_foot')
				act_regs.append('chandra_foot')
			if cameras[0] == cameralist[0]:
				display_regions(region_titles=set_reg_titles[0], REG='chandra_acis-s')
				act_regs.append('chandra_acis-s')
			if cameras[0] == cameralist[1]:
				display_regions(region_titles=set_reg_titles[0], REG='chandra_acis-i')
				act_regs.append('chandra_acis-i')
			if cameras[0] == cameralist[2]:
				display_regions(region_titles=set_reg_titles[0], REG='chandra_hrc-s')
				act_regs.append('chandra_hrc-s')
			if cameras[0] == cameralist[3]:
				display_regions(region_titles=set_reg_titles[0], REG='chandra_hrc-i')
				act_regs.append('chandra_hrc-i')
		image.destroy()
		self.im_exist[0] = None
		canvas.show()
	
	def onClick2(self):
		self.tog[0] = not self.tog[0]
		if self.tog[0]:
			display_regions(region_titles=set_reg_titles[0], REG='xmm_archival')
			display_regions(region_titles=set_reg_titles[0], REG='xmm_ao10')
			act_regs.append('xmm_archival')
			act_regs.append('xmm_ao10')
		else:
			act_regs.remove('xmm_archival')
			act_regs.remove('xmm_ao10')
			f.clf()
			plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick3(self):
		for region in act_regs[::-1]:
			if region.startswith('chandra'):
				act_regs.remove(region)
		f.clf()
		plot_FITS(title=set_title[0],regions=True)
		canvas.show()
	
	def onClick0(self):
		act_regs[:]=[]
		reset_buttons()
		f.clf()
		plot_FITS(title=set_title[0])
		canvas.show()

class Save:
	
	def __init__(self, master):
		frame = Frame(master) 
		frame.pack()
		self.button1 = Button(frame, text="PNG", command=lambda x=self.onClick0: x('png'))
		self.button1.pack()
		self.button2 = Button(frame, text="PS", command=lambda x=self.onClick0: x('ps'))
		self.button2.pack()
		self.button3 = Button(frame, text="EPS", command=lambda x=self.onClick0: x('eps'))
		self.button3.pack()
		self.button4 = Button(frame, text="JPEG", command=lambda x=self.onClick0: x('jpeg'))
		self.button4.pack()
		self.button5 = Button(frame, text="PDF", command=lambda x=self.onClick0: x('pdf'))
		self.button5.pack()
		self.button6 = Button(frame, text="SVG", command=lambda x=self.onClick0: x('svg'))
		self.button6.pack()
		self.im_exist = [None]
	
	def onClick0(self,type):
		if self.im_exist[0] is None:
			image = Toplevel()
			image.title('Save as {0} Image'.format(type.upper()))
			image.geometry('+550+300')
			entry = Entry(image, bd=3)
			image.bind("<Return>", (lambda event, e=entry: self.saveimage(e,image,type)))
			label = Label(image, text='.{0}'.format(type))
			entry.pack(side=LEFT)
			label.pack(side=LEFT)
			self.im_exist[0] = 1
			image.protocol("WM_DELETE_WINDOW", lambda image=image: existance(image,self.im_exist))
		
	def saveimage(self, entry, image, type):
		if def_dir=="D":
			fig.save('{0}.{1}'.format(entry.get(),type),dpi=300)
		else:
			fig.save('{0}/{1}.{2}'.format(def_dir,entry.get(),type),dpi=300)
		self.im_exist[0] = None
		image.destroy()

def reset_buttons():
	for i in [Radio.tog, FIR.tog, MIR.tog, Op_NIR.tog]:
		for j in range(len(i)):
			i[j] = False

def newWindow(Title,geo,band,ex):
	if ex[0]==None:
		wdw = Toplevel()
		wdw.title(Title)
		wdw.geometry(geo)
		if band=='plot':
			app = Plot(wdw)
		if band=='T':
			app = Stripe82(wdw)
		if band=='r':
			app = Radio(wdw)
		if band=='far':
			app = FIR(wdw)
		if band=='mid':
			app = MIR(wdw)
		if band=='op':
			app = Op_NIR(wdw)
		if band=='uv':
			app = UV(wdw)
		if band=='x':
			app = XRAY(wdw)
		if band=='save':
			app = Save(wdw)	
		windows.append(wdw)
		act_bands.append(band)
		ex[0]=1
		wdw.protocol('WM_DELETE_WINDOW', lambda wdw=wdw: closeWindow(wdw,band,ex))
	else:
		idx=act_bands.index(band)
		windows[idx].lift()

def closeWindow(wdw, band, ex):
	ex[0]=None
	wdw.destroy()
	if wdw in windows: windows.remove(wdw)
	if band in act_bands: act_bands.remove(band)
	if not windows: root.quit()

def existance(wdw,ex):
	ex[0] = None
	wdw.destroy()

def display_regions(region_titles=True,REG=''):
	if len(REG)>0:
		if region_titles:
			fig.show_regions(reg_dir + REG + '.reg')
		elif REG.startswith('chandra') | REG.startswith('gr67'):
			fig.show_regions(reg_dir + REG + '.reg')
		else:
			fig.show_regions(reg_dir + REG + '_noTitle.reg')

def plot_FITS(title=True,regions=False):
	global fig
	fig = aplpy.FITSFigure('stripe82.fits',figure=f,subplot=[0.05,0.2,0.9,0.6], convention='calabretta')
	fig.show_grayscale()
	
	fig.ticks.set_xspacing(10.0)
	fig.ticks.set_yspacing(5.0)
	fig.ticks.set_color('black')
	fig.tick_labels.set_xformat('dd.d')
	fig.tick_labels.set_yformat('dd')

	fig.add_grid()
	fig.grid.show()
	fig.grid.set_color('blue')
	
	if title:
		fig.show_regions(reg_dir + 'stripe82_title.reg')
	
	if regions:
		for region in act_regs:
			display_regions(region_titles=set_reg_titles[0], REG=region)
	
def visual():
	global windows,bands,root,d,def_dir,reg_dir,fig,f,act_regs,act_bands,set_title,set_reg_titles
	
	reg_dir = './Regions/'
	def_dir = raw_input("Name of directory to save images in (Current Working Directory: D): ")
	while os.path.isdir(def_dir)==False:
		if def_dir=="D":
			break
		print "{0} does not exist".format(def_dir)
		def_dir=raw_input("Try another directory:  ")
	
	root = Tk()
	root.withdraw()
	
	f = plt.figure(figsize=(21.7,11.2))
	s82_vis_exist,s82_exist = ([None],[None])
	set_title,set_reg_titles = ([True],[True])
	windows,act_regs,act_bands=([],[],[])
	bands=['plot','T','r','far','mid','op','uv','x','save']
	
	newWindow("Stripe 82 Visual","",bands[0],s82_vis_exist)
	root.mainloop()

if __name__ == '__main__':
	visual()

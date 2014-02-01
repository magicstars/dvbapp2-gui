#	-*-	coding:	utf-8	-*-
# magicstar FAQ from YouTube - base on MediaPortal UserList

from os.path import exists

try:
	from Plugins.Extensions.MediaPortal.resources.imports import *
	from Plugins.Extensions.MediaPortal.resources.youtubeplayer import YoutubePlayer
except:
	pass
      
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN

USER_Version = "USER-Channels v0.96"

USER_siteEncoding = 'utf-8'

def magicstarFaq_YTChannelListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 495, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[1], 16777215, 16777215)
		] 
		
def magicstarFaq_YTChannelListEntry2(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 495, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1])
		] 
		
class magicstarFaq_YTChannel(Screen):
	
	def __init__(self, session):
		self.session = session
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		self.skin = """
		<screen name="defaultGenre" position="center,center" size="900,655" backgroundColor="#00060606" flags="wfNoBorder">
			<widget name="title" position="20,10" size="500,40" backgroundColor="#00101214" transparent="1" zPosition="10" font="Regular; 26" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="730,8" size="150,30" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular; 26" valign="center" halign="right" foregroundColor="#00dcdcdc">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="580,39" size="300,20" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right" foregroundColor="#00dcdcdc">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="ContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center" />
			<widget name="genreList" position="0,135" size="900,450" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" />
			<widget name="name" position="20,95" size="860,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<ePixmap pixmap="~/original/images/buttonred.png" position="60,630" size="100,2" alphatest="blend" />
			<widget name="key_red" position="60,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />
		</screen>"""
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red" : self.keyGreen
		}, -1)
		
		
		self['title'] = Label(USER_Version)
		self['ContentTitle'] = Label("Channel Auswahl")
		self['name'] = Label("")
		self['key_red'] = Label("Load")
		
		mypath = resolveFilename(SCOPE_PLUGINS)

		if (os.path.isfile("/proc/stb/info/vumodel")): 
			f = open("/proc/stb/info/vumodel", "r")
			model = f.read().strip()
			f.close()

		if model == "solo" or model == "ultimo":
			self.user_path = mypath + "Extensions/magicstarFaq/channels_3.xml"
		elif model == "duo" or model == "uno" or model == "duo2":
			self.user_path = mypath + "Extensions/magicstarFaq/channels_2.xml"
		elif model == "ini-3000" or model == "ini-5000" or model == "ini-7000" or model == "ini-7012":
			self.user_path = mypath + "Extensions/magicstarFaq/channels_1.xml"
		else:
			self.user_path = mypath + "Extensions/magicstarFaq/channels.xml"
			
		self.keyLocked = True
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append((0, "Mit dieser Erweiterung kannst Du deine Lieblings Youtube Kanäle selber hinzufügen.", ""))
		self.genreliste.append((0, "Für jeden Kanal müssen nur zwei Einträge hinzugefügt werden:", ""))
		self.genreliste.append((0, "'<name> Kanal Bezeichnung </name>' und '<user> Besitzername </user>'", ""))
		self.genreliste.append((0, " ", ""))
		self.genreliste.append((0, "Mit der Taste 'Grün' wird die Datei:", ""))
		self.genreliste.append((0, "'"+self.user_path+"' geladen.", ""))
		self.genreliste.append((0, " ", ""))
		self.genreliste.append((0, "With this extension you can add your favorite Youtube channels themselves.", ""))
		self.genreliste.append((0, "For each channel, only two entries are added:", ""))
		self.genreliste.append((0, "'<name> channel name </name>' and '<user> owner name </ user>'", ""))
		self.genreliste.append((0, " ", ""))
		self.genreliste.append((0, "With the 'Green' button the user file:", ""))
		self.genreliste.append((0, "'"+self.user_path+"' is loaded.", ""))
		
		if not exists(self.user_path):
			self.getUserFile(fInit=True)
			
		self.getUserFile()
		self.chooseMenuList.setList(map(magicstarFaq_YTChannelListEntry, self.genreliste))
		
	def getUserFile(self, fInit=False):
		mypath = resolveFilename(SCOPE_PLUGINS)
		
		fname = mypath + "Extensions/magicstarFaq/channels.xml"
				
		print "fname: ",fname
		try:
			if fInit:
				shutil.copyfile(fname, self.user_path)
				return
				
			fp = open(self.user_path)
			data = fp.read()
			fp.close()
		except IOError, e:
			print "File Error: ",e
			self.genreliste = []
			self.genreliste.append((0, str(e), ""))
			self.chooseMenuList.setList(map(magicstarFaq_YTChannelListEntry, self.genreliste))
		else:
			self.userData(data)

	def userData(self, data):
		list = re.findall('<name>(.*?)</name>.*?<user>(.*?)</user>', data, re.S)
		
		self.genreliste = []
		if list:
			i = 1
			for (name, user) in list:
				self.genreliste.append((i, name.strip(), '/'+user.strip()))
				i += 1
				
			self.genreliste.sort(key=lambda t : t[1].lower())
			self.keyLocked = False
		else:
			self.genreliste.append((0, "Keine User Channels gefunden !", ""))
			
		self.chooseMenuList.setList(map(magicstarFaq_YTChannelListEntry2, self.genreliste))
	
	def keyGreen(self):
		self.getUserFile()
	
	def keyOK(self):
		if self.keyLocked:
			return
			
		genreID = self['genreList'].getCurrent()[0][0]
		genre = self['genreList'].getCurrent()[0][1]
		stvLink = self['genreList'].getCurrent()[0][2]
		self.session.open(magicstarFaq_ListChannel_ListScreen, genreID, stvLink, genre)

	def keyCancel(self):
		self.close()

def magicstarFaq_ListChannel_ListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 495, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+entry[1], 16777215, 16777215)
		] 
		
class magicstarFaq_ListChannel_ListScreen(Screen):
	
	def __init__(self, session, genreID, stvLink, stvGenre):
		self.session = session
		self.genreID = genreID
		self.stvLink = stvLink
		self.genreName = stvGenre
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		self.skin = """
		<screen name="dokuList" position="center,center" size="900,655" backgroundColor="#00060606" flags="wfNoBorder">
			<widget name="title" position="20,10" size="500,40" backgroundColor="#00101214" transparent="1" zPosition="10" font="Regular; 26" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="730,8" size="150,30" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular; 26" valign="center" halign="right" foregroundColor="#00dcdcdc">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="580,39" size="300,20" backgroundColor="#00101214" transparent="1" zPosition="1" font="Regular;18" valign="center" halign="right" foregroundColor="#00dcdcdc">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="ContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="0" foregroundColor="#00000000" font="Regular;22" halign="center" />
			<widget name="liste" position="0,86" size="900,303" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" />
			<eLabel position="20,390" size="860,2" backgroundColor="#00555556" />
			<widget name="coverArt" pixmap="~/original/images/no_coverArt.png" position="20,396" size="270,200" transparent="1" alphatest="blend" borderWidth="2" borderColor="#00555556" />
			<widget name="name" position="300,395" size="580,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" zPosition="0" />
			<widget name="handlung" position="300,425" size="580,170" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" zPosition="0" />
			<widget name="VideoPrio" position="745,605" size="105,24" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular; 20" valign="center" halign="right" zPosition="1" />
			<widget name="vPrio" position="855,605" size="25,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="center" halign="center" zPosition="1" foregroundColor="#00bab329" />
			<widget name="Page" position="700,605" size="56,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="center" halign="right" zPosition="0" />
			<widget name="page" position="755,605" size="95,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="center" halign="right" zPosition="0" />
			<ePixmap pixmap="~/original/images/buttonred.png" position="60,630" size="100,2" alphatest="blend" />
			<ePixmap pixmap="~/original/images/buttongreen.png" position="205,630" size="100,2" alphatest="blend" />
			<ePixmap pixmap="~/original/images/buttonyellow.png" position="350,630" size="100,2" alphatest="blend" />
			<ePixmap pixmap="~/original/images/buttonblue.png" position="492,630" size="100,2" alphatest="blend" />
			<widget name="key_red" position="60,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />
			<widget name="key_green" position="205,605" size="100,30" transparent="1" backgroundColor="#00101214" font="Regular; 20" valign="bottom" halign="center" />
			<widget name="key_yellow" position="350,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />
			<widget name="key_blue" position="492,605" size="100,30" transparent="1" font="Regular; 20" backgroundColor="#00101214" valign="bottom" halign="center" />
		</screen>"""
		
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" 		: self.keyOK,
			"cancel"	: self.keyCancel,
			"up" 		: self.keyUp,
			"down" 		: self.keyDown,
			"right" 	: self.keyRight,
			"left" 		: self.keyLeft,
			"nextBouquet": self.keyPageUpFast,
			"prevBouquet": self.keyPageDownFast,
			"red" 		:  self.keyTxtPageUp,
			"blue" 		:  self.keyTxtPageDown,
			"yellow"	: self.keyYellow,
			"1" 		: self.key_1,
			"3" 		: self.key_3,
			"4" 		: self.key_4,
			"6" 		: self.key_6,
			"7" 		: self.key_7,
			"9" 		: self.key_9
		}, -1)

		self['title'] = Label(USER_Version)
		self['ContentTitle'] = Label(self.genreName)
		self['name'] = Label("")
		self['handlung'] = ScrollLabel("")
		self['page'] = Label("")
		self['key_red'] = Label("Text-")
		self['key_green'] = Label("")
		self['key_yellow'] = Label("")
		self['key_blue'] = Label("Text+")
		self['VideoPrio'] = Label("")
		self['vPrio'] = Label("")
		self['Page'] = Label("Page")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.baseUrl = "http://www.youtube.com"

		self.videoPrio = int(config.mediaportal.youtubeprio.value)
		self.videoPrioS = ['L','M','H']
		self.setVideoPrio()
		
		self.keckse = {}
		self.filmliste = []
		self.start_idx = 1
		self.max_res = 12
		self.total_res = 0
		self.pages = 0
		self.page = 0
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.loadPageData()
		
	def loadPageData(self):
		self.keyLocked = True
		print "getPage: ",self.stvLink
		
		self.filmliste = []
		self.filmliste.append(('Bitte warten...','','','',''))
		self.chooseMenuList.setList(map(magicstarFaq_ListChannel_ListEntry, self.filmliste))
		
		url = "http://gdata.youtube.com/feeds/api/users"+self.stvLink+"/uploads?"+\
				"start-index=%d&max-results=%d&v=2" % (self.start_idx, self.max_res)
		getPage(url, cookies=self.keckse, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		print "genreData:"
		print "genre: ",self.genreID
		if not self.pages:
			m = re.search('totalResults>(.*?)</', data)
			if m:
				a = int(m.group(1))
				self.pages = a // self.max_res
				if a % self.max_res:
					self.pages += 1
				self.page = 1
		
		a = 0
		l = len(data)
		self.filmliste = []
		while a < l:
			mg = re.search('<media:group>(.*?)</media:group>', data[a:], re.S)
			if mg:
				a += mg.end()
				m1 = re.search('description type=\'plain\'>(.*?)</', mg.group(1), re.S)
				if m1:
					desc = decodeHtml(m1.group(1))
					desc = urllib.unquote(desc)
				else:
					desc = "Keine weiteren Info's vorhanden."
					
				m2 = re.search('<media:player url=.*?/watch\?v=(.*?)&amp;feature=youtube_gdata_player.*?'\
					'<media:thumbnail url=\'(.*?)\'.*?<media:title type=\'plain\'>(.*?)</.*?<yt:duration seconds=\'(.*?)\'', mg.group(1), re.S)
				if m2:
					vid = m2.group(1)
					img = m2.group(2)
					dura = int(m2.group(4))
					vtim = str(datetime.timedelta(seconds=dura))
					title = decodeHtml(m2.group(3))
					self.filmliste.append((vtim+' ', title, vid, img, desc))
			else:
				a = l
				
		if len(self.filmliste) == 0:
			print "No audio drama found!"
			self.pages = 0
			self.filmliste.append(('Keine Videos gefunden !','','','',''))
		else:
			#self.filmliste.sort(key=lambda t : t[0].lower())
			menu_len = len(self.filmliste)
			print "Audio dramas found: ",menu_len
			
		self.chooseMenuList.setList(map(magicstarFaq_ListChannel_ListEntry, self.filmliste))
		self.keyLocked = False
		self.showInfos()
		
	def dataError(self, error):
		print "dataError: ",error

	def dataErrorP(self, error):
		print "dataError:"
		printl(error,self,"E")
		self.ShowCoverNone()
		
	def showInfos(self):
		self['page'].setText("%d / %d" % (self.page,self.pages))
		stvTitle = self['liste'].getCurrent()[0][1]
		stvImage = self['liste'].getCurrent()[0][3]
		desc = self['liste'].getCurrent()[0][4]
		print "Img: ",stvImage
		self['name'].setText(stvTitle)
		self['handlung'].setText(desc)
		if stvImage != '':
			url = stvImage
			print "Img: ",url
			downloadPage(url, "/tmp/Icon.jpg").addCallback(self.ShowCover).addErrback(self.dataErrorP)
		else:
			self.ShowCoverNone()
		
	def ShowCover(self, picData):
		print "ShowCover:"
		picPath = "/tmp/Icon.jpg"
		self.ShowCoverFile(picPath)
		
	def ShowCoverNone(self):
		print "ShowCoverNone:"
		picPath = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/no_coverArt.png"
		self.ShowCoverFile(picPath)
	
	def ShowCoverFile(self, picPath):
		print "showCoverFile:"
		if fileExists(picPath):
			print "picpath: ",picPath
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload
	
	def youtubeErr(self, error):
		print "youtubeErr: ",error
		self['handlung'].setText("Das Video kann leider nicht abgespielt werden !\n"+str(error))
		
	def setVideoPrio(self):
		"""
		if self.videoPrio+1 > 2:
			self.videoPrio = 0
		else:
			self.videoPrio += 1
		"""
		self.videoPrio = int(config.mediaportal.youtubeprio.value)
		self['vPrio'].setText(self.videoPrioS[self.videoPrio])

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		i = self['liste'].getSelectedIndex()
		if not i:
			self.keyPageDownFast()
			
		self['liste'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		i = self['liste'].getSelectedIndex()
		l = len(self.filmliste) - 1
		#print "i, l: ",i,l
		if l == i:
			self.keyPageUpFast()
			
		self['liste'].down()
		self.showInfos()
		
	def keyTxtPageUp(self):
		self['handlung'].pageUp()
			
	def keyTxtPageDown(self):
		self['handlung'].pageDown()
			
	def keyPageUpFast(self,step=1):
		if self.keyLocked:
			return
		#print "keyPageUp: "
		oldpage = self.page
		if (self.page + step) <= self.pages:
			self.page += step
			self.start_idx += self.max_res * step
		else:
			self.page = 1
			self.start_idx = 1
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPageData()
		
	def keyPageDownFast(self,step=1):
		if self.keyLocked:
			return
		print "keyPageDown: "
		oldpage = self.page
		if (self.page - step) >= 1:
			self.page -= step
			self.start_idx -= self.max_res * step
		else:
			self.page = self.pages
			self.start_idx = self.max_res * (self.pages - 1) + 1
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPageData()
			
	def keyYellow(self):
		self.setVideoPrio()

	def key_1(self):
		#print "keyPageDownFast(2)"
		self.keyPageDownFast(2)
		
	def key_4(self):
		#print "keyPageDownFast(5)"
		self.keyPageDownFast(5)
		
	def key_7(self):
		#print "keyPageDownFast(10)"
		self.keyPageDownFast(10)
		
	def key_3(self):
		#print "keyPageUpFast(2)"
		self.keyPageUpFast(2)
		
	def key_6(self):
		#print "keyPageUpFast(5)"
		self.keyPageUpFast(5)
		
	def key_9(self):
		#print "keyPageUpFast(10)"
		self.keyPageUpFast(10)

	def keyOK(self):
		if self.keyLocked:
			return
		"""
		dhTitle = self['liste'].getCurrent()[0][1]
		dhVideoId = self['liste'].getCurrent()[0][2]
		print "Title: ",dhTitle
		#print "VideoId: ",dhVideoId
		y = youtubeUrl(self.session)
		y.addErrback(self.youtubeErr)
		dhLink = y.getVideoUrl(dhVideoId, self.videoPrio)
		if dhLink:
			print dhLink
			sref = eServiceReference(0x1001, 0, dhLink)
			sref.setName(dhTitle)
			self.session.open(MoviePlayer, sref)
		"""
		self.session.openWithCallback(
			self.setVideoPrio,
			YoutubePlayer,
			self.filmliste,
			self['liste'].getSelectedIndex(),
			playAll = True,
			listTitle = self.genreName,
			title_inr=1
			)
		

	def keyCancel(self):
		self.close()

def main(session, **kwargs):
	if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.pyo"):
		session.open(magicFaq_YTChannel)
	else:
		from Screens.MessageBox import MessageBox 
		session.open(MessageBox, _('Sorry: You have to install MediaPortal to get running this plugin'), MessageBox.TYPE_INFO, 3)
		
def Plugins(**kwargs):
	return PluginDescriptor(name=_("magicstar FAQ"), description="Video Tutorials", where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon="plugin_icon.png", fnc=main)

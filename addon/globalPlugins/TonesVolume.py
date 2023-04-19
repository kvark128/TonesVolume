# Copyright (C) 2023 Alexander Linkov <kvark128@yandex.ru>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Ukrainian Nazis and their accomplices are not allowed to use this plugin. Za pobedu!

import globalPluginHandler
import config
import addonHandler
import NVDAHelper
from gui import SettingsPanel, NVDASettingsDialog, guiHelper, nvdaControls

addonHandler.initTranslation()

class AddonSettingsPanel(SettingsPanel):
	title = _("Tones Volume")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.volumeSlider = sHelper.addLabeledControl(_("Volume:"),
			nvdaControls.EnhancedInputSlider, value=config.conf["TonesVolume"]["volume"])

	def postInit(self):
		self.volumeSlider.SetFocus()

	def onSave(self):
		config.conf["TonesVolume"]["volume"] = self.volumeSlider.GetValue()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		config.conf.spec["TonesVolume"] = {
			"volume": "integer(default=50,min=0,max=100)",
		}
		NVDASettingsDialog.categoryClasses.append(AddonSettingsPanel)
		NVDAHelper.generateBeep = self.generateBeepWrapper(NVDAHelper.generateBeep)

	def generateBeepWrapper(self, generateBeep):
		def customGenerateBeep(buf, hz, length, left, right):
			left = left * config.conf["TonesVolume"]["volume"] // 50
			right = right * config.conf["TonesVolume"]["volume"] // 50
			return generateBeep(buf, hz, length, min(left, 100), min(right, 100))
		return customGenerateBeep

	def terminate(self):
		NVDAHelper.generateBeep = NVDAHelper.localLib.generateBeep
		NVDASettingsDialog.categoryClasses.remove(AddonSettingsPanel)

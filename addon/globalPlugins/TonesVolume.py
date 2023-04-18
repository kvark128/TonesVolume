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
	title = _("Tones volume")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.volumeFactor = sHelper.addLabeledControl(_("Volume factor:"),
			nvdaControls.SelectOnFocusSpinCtrl, min=-50, max=50,
			initial=config.conf["TonesVolume"]["volumeFactor"])

	def postInit(self):
		self.volumeFactor.SetFocus()

	def onSave(self):
		config.conf["TonesVolume"]["volumeFactor"] = self.volumeFactor.GetValue()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		config.conf.spec["TonesVolume"] = {
			"volumeFactor": "integer(default=0,min=-50,max=50)",
		}
		NVDASettingsDialog.categoryClasses.append(AddonSettingsPanel)
		NVDAHelper.generateBeep = self.generateBeepWrapper(NVDAHelper.generateBeep)

	def generateBeepWrapper(self, generateBeep):
		def customGenerateBeep(buf, hz, length, left, right):
			left = left * (config.conf["TonesVolume"]["volumeFactor"] + 50) // 50
			right = right * (config.conf["TonesVolume"]["volumeFactor"] + 50) // 50
			return generateBeep(buf, hz, length, min(left, 100), min(right, 100))
		return customGenerateBeep

	def terminate(self):
		NVDAHelper.generateBeep = NVDAHelper.localLib.generateBeep
		NVDASettingsDialog.categoryClasses.remove(AddonSettingsPanel)

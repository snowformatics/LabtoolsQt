import sys
import os
import shutil
import logging
import time
import platform
import webbrowser
import errno

from PyQt4 import QtGui, QtCore
from labtools_ui import Ui_LabtoolsQt

import calculate_reactions

#pyrcc4 labtools.qrc > rc_labtools.py
#pyuic4 labtools.ui > labtools_ui.py

class AboutPopup(QtGui.QWidget):
    def __init__(self, images_location):
        QtGui.QWidget.__init__(self)

        self.setWindowTitle('LabtoolsQt v. 1.0.3')
        self.images_location = images_location
        label = QtGui.QLabel(self)
        pixmap = QtGui.QPixmap(self.images_location + "about.png")
        label.setPixmap(pixmap)

class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_LabtoolsQt()

        # Main paths
        self.data_location = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation))
        self.data_location = self.data_location.split('Local')[0] + '/Local/'
        self.home_location = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation))
        self.temp_location = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.TempLocation))
        self.app_location = self.data_location + '/LabtoolsQt/'
        self.images_location = self.app_location + '/images/'
        self.mm = {'Silicondioxide(SiO2)': 60.1, 'Sodium-Dodecyl-Sulfate(C12H25NaO4S)': 288.4, 'Sodiumchloride(NaCl)': 58.5, 'Calciumcarbide(CaC2)': 64.1, 'Propane(C3H8)': 44.1, 'Hydrogenperoxide(H2O2)': 34.0, 'Potassiumnitrate(KNO3)': 101.1, 'Calciumhydroxide(Ca(OH)2)': 74.1, 'Arsenictrioxide(Arsenic(III)oxide)(As2O3)': 198.0, 'Pentane(C5H12)': 72.1, 'Sulfane(H2S)': 34.1, 'Ammoniumsulfate((NH4)2SO4)': 132.1, 'Lead(IV)oxide(PbO2)': 239.0, 'Lead(II)oxide(PbO)': 223.2, 'Ammoniumchloride(NH4Cl)': 53.5, 'Bariumhydroxide(Ba(OH)2)': 171.4, 'Calciumchloride(CaCl2)': 111.0, 'Calciumfluoride(CaF2)': 78.0, 'Nitrogendioxide(NO2)': 46.0, 'Potassiumpermanganate(KMnO4)': 158.0, 'Sodiumhydroxide(NaOH)': 40.0, 'Magnesiumchloride(MgCl2)': 95.2, 'Copper(II)sulfate(CuSO4)': 159.6, 'Copper(II)chloride(CuCl2)': 134.4, 'Zincoxide(ZnO)': 81.4, 'Carbondisulfide(CS2)': 76.1, 'Sodiumcarbonate(Na2CO3)': 106.0, 'Lead(II)iodide(PbI2)': 58.1, 'Lead(II)chloride(PbCl2)': 60.1, 'Aluminiumhydroxide(Al(OH)3)': 78.0, 'Hydrogenfluoride(HF)': 20.0, 'Lead(II)sulfide(PbS)': 98.1, 'Silverchloride(AgCl)': 143.3, 'Hydrochloricacid(HCl(Hydrogenchloride(HCl))': 36.5, 'Sodiumnitrate(NaNO3)': 85.0, 'Chromium(III)chloride(CrCl3)': 158.0, 'TRIS(C4H11NO3)': 121.14, 'Ammoniumnitrate(NH4NO3)': 80.0, 'Boric-acid(H3BO3)': 61.8, 'Urea(CO(NH2)2)': 60.1, 'Methanol(CH3OH)': 32.0, 'Cobalt(II)chloride(CoCl2)': 130.0, 'Iron(III)chloride(FeCl3)': 162.2, 'Orthophosphoricacid(H3PO4)': 98.0, 'Formicacid(HCHO)': 46.0, 'Calciumsulfate(Gypsum)(CaSO4)': 136.1, 'Glucose': 180.0, 'Hydrobromicacid(HBr)': 80.9, 'Chromium(III)oxide(Cr2O3)': 152.0, 'Nitricoxide(NO)': 30.0, 'Magnesiumsulfate(MgSO4)': 120.4, 'Benzene(C6H6)': 78.1, 'Potassiumhydroxide(KOH)': 56.1, 'Hydroiodicacid(HI)': 127.9, 'Chromium(II)chloride(CrCl2(alsochromouschlori)': 123.0, 'Lead(II)sulfate(Pb(SO4))': 64.1, 'Carbonmonoxide(CO)': 28.0, 'Aluminiumsulfate(Al2(SO4)3)': 342.1, 'Ethane(C2H6)': 30.1, 'Bariumchloride(BaCl2)': 208.2, 'Potassiumcarbonate(K2CO3)': 138.2, 'Butane(C4H10)': 58.1, 'Potassiumbromide(KBr)': 119.0, 'Tetrachloromethane(CCl4)': 153.8, 'Aluminiumchloride(AlCl3)': 133.3, 'Bariumsulfate(BaSO4)': 233.0, 'Chloroform(CHCl3)': 119.4, 'Phenol(C6H5OH)': 94.1, 'Magnesiumoxide(MgO)': 40.3, 'Bariumcarbonate(BaCO3)': 197.0, 'Silvernitrate(AgNO3)': 169.9, 'Zincsulfide(ZnS)': 97.4, 'Aluminiumoxide(Al2O3)': 101.9, 'Ethene(C2H4)': 28.1, 'Carbondioxide(CO2)': 44.0, 'Ethanol(C2H5OH)': 46.1, 'Formaldehyde': 30.0, 'Lead(II)nitrate(Pb(NO3)2)': 331.2, 'Silveriodide(AgI)': 234.8, 'Potassiumchloride(KCl)': 74.6, 'Ammonia(NH3)': 17.0, 'Hexane(C6H14)': 86.2, 'Methane(CH4)': 16.0, 'Copper(II)oxide(CuO)': 79.5, 'Ethanal(Acetaldehyde)(CH3CHO)': 44.1, 'Glycine': 75.1, 'Iron(II,III)oxide(Fe3O4)': 231.5, 'Ethanoicacid(CH3COOH)': 60.1, 'Iron(III)oxide(Fe2O3)': 159.7, 'Zincchloride(ZnCl2)': 136.3, 'Iron(II)oxide(FeO)': 72.0}

        try:
            self.create_folders()
            self.copying_files()
            # Logging
            self.log_file = self.app_location + '/logging_labtools.txt'
            logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

        except (IOError, OSError):
            logging.debug(time.strftime("%d.%m.%Y um %H:%M:%S Uhr"))
            logging.debug(str(platform.system()+platform.release()))
            logging.exception('Got exception on main handler')
            raise

        self.ui.setupUi(self)
        self.create_connects()

        self.update_combo()

    def create_connects(self):
        """Connect events."""
        self.ui.pushButton.clicked.connect(self.start_ligation)
        self.ui.pushButton_2.clicked.connect(self.start_solution)
        self.ui.pushButton_5.clicked.connect(self.start_mixer)
        self.ui.actionAbout.triggered.connect(self.show_about_message)
        self.ui.actionDocumentation.triggered.connect(self.show_help)


    def create_folders(self):
        """Create important folders of siFi in the data path."""
        location_folders = [self.app_location, self.images_location]
        for folder in location_folders:
            if not os.path.exists(folder):
                os.mkdir(folder)


    def copying_files(self):
        """Copy important files of siFi in the data path."""
        to_copy_folders = os.listdir(os.getcwd() + '/to_copy/')

        for folder in to_copy_folders:

            to_copy_files = os.listdir(os.getcwd() + '/to_copy/' + folder)
            for files in to_copy_files:
                if not files.startswith('.'):
                    if not os.path.exists(self.app_location + '/' + folder + '/' + files):
                        if not folder.startswith('.'):
                            shutil.copyfile(os.getcwd() + '/to_copy/' + folder + '/' + files, self.app_location + '/' + folder + '/' + files)

    def update_combo(self):
        """Append all compounds to the combobox."""
        comp_list = []
        for compound in self.mm.keys():
            comp_list.append(compound)
        comp_list.sort()
        self.ui.comboBox.addItems(comp_list)
    #================================================================================================================

    def is_empty(self, widget_lst):
        """Checks whether a text widget is empty and return False, otherwise return true."""
        for widget in widget_lst:
            if widget == '':
                return False

    def start_ligation(self):
        """Starts ligation calculator."""

        is_empty = self.is_empty([self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text(),
                                  self.ui.lineEdit_4.text(), self.ui.lineEdit_5.text(), self.ui.lineEdit_6.text()])
        if is_empty is False:
            message = ('Please insert a value', 'Error')
        else:

            info_message = calculate_reactions.calc_ligation(int(self.ui.lineEdit.text()),
                                                             int(self.ui.lineEdit_2.text()),
                                                             float(self.ui.lineEdit_3.text()),
                                                             float(self.ui.lineEdit_4.text()),
                                                             int(self.ui.lineEdit_5.text()),
                                                             float(self.ui.lineEdit_6.text()))
            message = (info_message, 'Results')
        self.show_info_message(message[0], message[1])

    def start_solution(self):
        """Starts solution calculator."""

        is_empty = self.is_empty([self.ui.lineEdit_13.text(), self.ui.lineEdit_14.text(), self.ui.spinBox.value()])

        if is_empty is False:
            message = ('Please insert a value', 'Error')
        else:
            info_message = calculate_reactions.calc_solution(str(self.ui.comboBox.currentText()),
                                                             float(self.ui.lineEdit_13.text()),
                                                             float(self.ui.lineEdit_14.text()),
                                                             int(self.ui.spinBox.value()),
                                                             self.mm)
            message = (info_message, 'Results')
        self.show_info_message(message[0], message[1])
        
    def start_mixer(self):
        """Starts mixer calculator."""

        is_empty = self.is_empty([self.ui.lineEdit_15.text(), self.ui.lineEdit_16.text(), self.ui.lineEdit_17.text()])
        if is_empty is False:
            message = ('Please insert a value', 'Error')
        else:
            info_message = calculate_reactions.calc_dilution(float(self.ui.lineEdit_15.text()),
                                                             float(self.ui.lineEdit_16.text()),
                                                             float(self.ui.lineEdit_17.text()),
                                                             str(self.ui.comboBox_2.currentText()),
                                                             str(self.ui.comboBox_3.currentText()),
                                                             str(self.ui.comboBox_4.currentText()))

            message = (info_message, 'Results')
        self.show_info_message(message[0], message[1])

    def show_info_message(self, message, msg_type):
        """Shows a message dialog."""
        QtGui.QMessageBox.information(self,
                                      msg_type,
                                      """<p style="font-family: 'Comic Sans MS'; font-size:14pt; color:#2E9AFE">"""
                                      + message + """</p>""")

    def show_about_message(self):
        """Shows about box."""
        self.w = AboutPopup(self.images_location)
        self.w.setGeometry(QtCore.QRect(100, 100, 610, 350))
        self.w.show()



    def show_help(self):
        """Show help."""
        webbrowser.open("labtools.ipk-gatersleben.de/help/LabtoolsQt/LabtoolsQt.html")






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("plastique"))
    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    my_app = MyMainWindow()
    my_app.show()
    sys.exit(app.exec_())
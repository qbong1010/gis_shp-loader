import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication

class GisShpLoaderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """대화상자 초기화"""
        super(GisShpLoaderDialog, self).__init__(parent)
        # UI 구성요소 설정
        self.setupUi()
        
    def setupUi(self):
        """UI 구성요소를 수동으로 설정합니다."""
        self.resize(400, 200)
        self.setWindowTitle("SHP 파일 로더 설정")
        
        # 레이아웃 설정
        layout = QtWidgets.QVBoxLayout()
        
        # 폴더 선택 그룹
        folder_group = QtWidgets.QGroupBox("폴더 설정")
        folder_layout = QtWidgets.QHBoxLayout()
        
        self.folder_edit = QtWidgets.QLineEdit()
        self.folder_button = QtWidgets.QPushButton("폴더 선택...")
        self.folder_button.clicked.connect(self.select_folder)
        
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(self.folder_button)
        folder_group.setLayout(folder_layout)
        
        # 파일 이름 설정 그룹
        file_group = QtWidgets.QGroupBox("파일 설정")
        file_layout = QtWidgets.QHBoxLayout()
        
        file_layout.addWidget(QtWidgets.QLabel("파일 이름:"))
        self.filename_edit = QtWidgets.QLineEdit("A0010000.shp")
        
        file_layout.addWidget(self.filename_edit)
        file_group.setLayout(file_layout)
        
        # 버튼 영역
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # 전체 레이아웃 설정
        layout.addWidget(folder_group)
        layout.addWidget(file_group)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def select_folder(self):
        """폴더 선택 대화상자를 엽니다."""
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "상위 폴더 선택",
            os.path.expanduser("~")
        )
        if folder:
            self.folder_edit.setText(folder)
            
    def get_values(self):
        """사용자가 설정한 값을 반환합니다."""
        return {
            'folder': self.folder_edit.text(),
            'filename': self.filename_edit.text()
        } 
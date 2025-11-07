import os
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject, QgsVectorLayer
from .gis_shp_loader_dialog import GisShpLoaderDialog

class GisShpLoader:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.dialog = None

    def initGui(self):
        """QGIS 플러그인 인터페이스가 시작될 때 호출됩니다."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text="SHP 파일 로더",
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """플러그인이 제거될 때 호출됩니다."""
        for action in self.actions:
            self.iface.removePluginMenu("SHP 로더", action)
            self.iface.removeToolBarIcon(action)

    def add_action(self, icon_path, text, callback, parent=None):
        """플러그인 액션을 추가합니다."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        
        self.iface.addToolBarIcon(action)
        self.iface.addPluginToMenu("SHP 로더", action)
        self.actions.append(action)
        
        return action

    def run(self):
        """플러그인 기능이 실행될 때 호출됩니다."""
        # 대화상자 생성 및 표시
        self.dialog = GisShpLoaderDialog(self.iface.mainWindow())
        
        # 기본 경로 설정 (사용자의 요구사항에 따라 초기값 설정)
        default_path = r"C:\Users\dohwa\Desktop\경기_남양주시"
        if os.path.exists(default_path):
            self.dialog.folder_edit.setText(default_path)
            
        # 대화상자가 확인(OK)으로 종료되면 처리 시작
        if self.dialog.exec_():
            values = self.dialog.get_values()
            base_folder = values['folder']
            file_name = values['filename']
            
            if not base_folder or not file_name:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    "경고",
                    "폴더 경로와 파일 이름을 모두 입력해주세요."
                )
                return
            
            if not os.path.exists(base_folder):
                QMessageBox.critical(
                    self.iface.mainWindow(),
                    "오류",
                    f"지정한 경로가 존재하지 않습니다: {base_folder}"
                )
                return
                
            # 하위 폴더 목록 가져오기
            try:
                subfolders = [f for f in os.listdir(base_folder) 
                              if os.path.isdir(os.path.join(base_folder, f))]
            except Exception as e:
                QMessageBox.critical(
                    self.iface.mainWindow(),
                    "오류",
                    f"폴더 목록을 가져오는 중 오류가 발생했습니다: {str(e)}"
                )
                return
            
            if not subfolders:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    "경고",
                    "선택한 경로에 하위 폴더가 없습니다."
                )
                return
            
            # 각 하위 폴더에서 SHP 파일 로드
            loaded_count = 0
            error_count = 0
            not_found_count = 0
            
            for subfolder in subfolders:
                full_path = os.path.join(base_folder, subfolder, file_name)
                if os.path.exists(full_path):
                    # 레이어 이름 설정 (폴더명_파일명)
                    layer_name = f"{subfolder}_{os.path.splitext(file_name)[0]}"
                    
                    # 벡터 레이어 생성 및 추가
                    layer = QgsVectorLayer(full_path, layer_name, "ogr")
                    if layer.isValid():
                        QgsProject.instance().addMapLayer(layer)
                        loaded_count += 1
                    else:
                        error_count += 1
                else:
                    not_found_count += 1
            
            # 결과 메시지 표시
            QMessageBox.information(
                self.iface.mainWindow(),
                "완료",
                f"작업 완료:\n"
                f"- {loaded_count}개 파일 로드됨\n"
                f"- {error_count}개 파일 로드 실패\n"
                f"- {not_found_count}개 파일 찾지 못함"
            ) 
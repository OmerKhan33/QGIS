# In this code we will plot a buffer layer in combination with vector_layer
# The buffer Layer has been created on QGIS software.
# Remember to change file path as per your path specified in your PC

import sys
from qgis.core import QgsApplication, QgsVectorLayer
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

def main():
    # Initialize QGIS
    QgsApplication.setPrefixPath('/usr', True)
    app = QApplication(sys.argv)
    QgsApplication.initQgis()

    # Create a map canvas
    canvas = QgsMapCanvas()
    canvas.setCanvasColor(Qt.white)

    # Set paths for shapefiles
    layer_path = "C:/Users/omerk/PycharmProjects/QGIS/QGIS_related_Files/PAK_adm2.shp"
    buffer_path = "C:/Users/omerk/PycharmProjects/QGIS/QGIS_related_Files/Pak_Buffer.shp"

    # Load shapefiles as vector layers
    pak_layer = QgsVectorLayer(layer_path, "Shape File", "ogr")
    if not pak_layer.isValid():
        print("Layer failed to load!")
        return

    buff_layer = QgsVectorLayer(buffer_path, "Shape File", "ogr")
    if not buff_layer.isValid():
        print("Layer failed to load!")
        return

    # Set layer opacities
    pak_layer.setOpacity(0.2)
    buff_layer.setOpacity(0.2)  # Corrected opacity value (was 20, should be between 0 and 1)

    # Create a main window and display the canvas
    main_window = QMainWindow()
    main_window.setCentralWidget(canvas)
    main_window.setFixedSize(800, 600)
    main_window.show()

    # Set canvas extent and layers
    canvas.setExtent(pak_layer.extent())
    canvas.setLayers([pak_layer, buff_layer])

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



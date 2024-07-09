# Simple code that plots a map and stationary points on a map canvas
# If this code does not run make sure that the file path matches as per location on your pc.
# Make sure the files given in the repository are copied to the same folder as your project file.


import sys
from qgis.core import QgsApplication, QgsVectorLayer
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

def main():
    """v
    Main function to set up and run the QGIS application.
    """
    # Set up the QGIS application environment
    QgsApplication.setPrefixPath('/usr', True)
    app = QApplication(sys.argv)
    QgsApplication.initQgis()

    # Create and configure the map canvas
    canvas = QgsMapCanvas()  # QgsMapCanvas is a widget that displays map layers, used to visualize geographical data
    canvas.setCanvasColor(Qt.white)
    canvas.show() # Set canvas background color to black

    # Path to the shapefile
    layer_path = "C:/Users/omerk/PycharmProjects/QGIS/QGIS_related_Files/PAK_adm2.shp"  # change accordingly
    new_layer = "C:/Users/omerk/PycharmProjects/QGIS/QGIS_related_Files/point_layer.shp"  # Change accordingly
    # Load the vector layer
    pak_layer = QgsVectorLayer(layer_path, "Shape File", "ogr")
    if not pak_layer.isValid():
        print("Layer failed to load!")
        return

    new_layer = QgsVectorLayer(new_layer, "Shape File", "ogr")
    if not new_layer.isValid():
        print("Layer failed to load!")
        return

    pak_layer.setOpacity(0.2) # Set layer opacity
    new_layer.setOpacity(20)


    # Set up the main window
    main_window = QMainWindow()  # Provides a main application window with standard features like menus, toolbars, and a status bar.
    main_window.setCentralWidget(canvas)  # Set the canvas as the central widget
    main_window.setFixedSize(800, 600)  # Set a fixed size for the window
    main_window.show()

    # Set the extent of the map to focus on the vector layer
    # Ensures that when the map canvas is displayed, it is zoomed and centered to show the entire area covered by the pak_layer.
    canvas.setExtent(pak_layer.extent())
    canvas.setLayers([pak_layer, new_layer])

    # Display the canvas
    #canvas.show()

    # Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

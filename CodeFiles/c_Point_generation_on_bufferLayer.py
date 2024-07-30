# QGIS Point and Line Generator
# This script generates random points and lines within a specified area in Pakistan using QGIS.
# It demonstrates how to create memory layers, add features, and visualize them on a map canvas.

# Remember to change file path as per your path of these files specified in your PC


import sys
import numpy as np
from qgis.core import (
    QgsApplication, QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry, QgsPointXY, QgsField
)
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QVariant

def main():
    # Initialize QGIS
    QgsApplication.setPrefixPath('/usr', True)
    app = QApplication(sys.argv)
    QgsApplication.initQgis()

    # Create a map canvas
    canvas = QgsMapCanvas()
    canvas.setCanvasColor(Qt.white)

    # Paths to shapefiles
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

    # Create memory layers for points and lines
    point_layer = QgsVectorLayer("Point?crs=EPSG:4326", "Points", "memory")
    point_provider = point_layer.dataProvider()
    point_layer.startEditing()
    point_provider.addAttributes([QgsField("id", QVariant.Int)])
    point_layer.commitChanges()

    line_layer = QgsVectorLayer("LineString?crs=EPSG:4326", "Lines", "memory")
    line_provider = line_layer.dataProvider()
    line_layer.startEditing()
    line_provider.addAttributes([QgsField("id", QVariant.Int)])
    line_layer.commitChanges()

    # Generate points and lines
    center_point = QgsPointXY(75.0, 30.0)  # Adjusted center point towards the right side
    num_points = 10
    num_lines_per_point = 4
    base_angle = 120  # Base angle towards the center of Pakistan
    angle_variation = 30  # Angle variation for the lines pointing inward
    radius = 1.0  # Radius for the lines

    points = []
    for i in range(num_points):
        # Generate points towards the right side of Pakistan
        x_coord = center_point.x() + np.random.uniform(1, 5)  # Adjust as needed
        y_coord = center_point.y() + np.random.uniform(-5, 5)
        point = QgsPointXY(x_coord, y_coord)
        points.append(point)

        # Create point features
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        feature.setAttributes([i])
        point_provider.addFeature(feature)

        # Create lines from each point
        for j in range(num_lines_per_point):
            angle = base_angle + j * angle_variation
            angle_rad = np.deg2rad(angle)
            end_point = QgsPointXY(point.x() + radius * np.cos(angle_rad), point.y() + radius * np.sin(angle_rad))
            line_feature = QgsFeature()
            line_feature.setGeometry(QgsGeometry.fromPolylineXY([end_point, point]))
            line_feature.setAttributes([i])
            line_provider.addFeature(line_feature)

    point_layer.commitChanges()
    line_layer.commitChanges()

    # Save points to a NumPy file
    points_array = np.array([(p.x(), p.y()) for p in points])
    np.save("points.npy", points_array)

    # Add layers to the canvas
    QgsProject.instance().addMapLayers([pak_layer, point_layer, line_layer])
    canvas.setExtent(pak_layer.extent())
    canvas.setLayers([pak_layer, point_layer, line_layer, buff_layer])

    # Display the main window
    main_window = QMainWindow()
    main_window.setCentralWidget(canvas)
    main_window.setFixedSize(800, 600)
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

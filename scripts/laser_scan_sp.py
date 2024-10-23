#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import Header
from builtin_interfaces.msg import Duration
from rclpy.qos import qos_profile_sensor_data

class LaserScanToMarker(Node):
    def __init__(self):
        super().__init__('laser_scan_to_marker_sp')
        self.publisher_ = self.create_publisher(Marker, '/visualization_marker', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile_sensor_data
        )
        self.subscription  # prevent unused variable warning

    def get_marker_with_points(self, points):
        ''' Creates a visualization_msgs/Marker from a list of points
        Input:
        points: A list of geometry_msgs/Point objects
        Return:
        marker: a visualization_msgs/Marker object that can be published to RViz
        on topic 'visualization_marker'
        '''
        marker = Marker()
        marker.header.frame_id = 'laser_link'
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = ''
        marker.id = 0
        marker.type = Marker.POINTS
        marker.action = Marker.ADD
        marker.scale.x = 0.02
        marker.scale.y = 0.02
        marker.scale.z = 0.02
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0
        marker.points = points
        marker.lifetime = Duration(sec=2)
        return marker

    def listener_callback(self, msg):
        points = []
        angle = msg.angle_min
        for distance in msg.ranges:
            if math.isinf(distance) or math.isnan(distance):
                # Skip invalid measurements
                angle += msg.angle_increment
                continue
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            point = Point(x=x, y=y, z=0.0)
            points.append(point)
            angle += msg.angle_increment

        marker = self.get_marker_with_points(points)
        self.publisher_.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    laser_scan_to_marker = LaserScanToMarker()
    rclpy.spin(laser_scan_to_marker)

    laser_scan_to_marker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


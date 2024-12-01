from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 使用 get_package_share_directory 获取包路径，并指向 install 文件夹中的 URDF 文件
    #urdf_path = Path(get_package_share_directory('innok_heros_description')) / 'install' / 'innok_heros_description' / 'share' / 'innok_heros_description' / 'urdf' / 'innok_heros_3w.urdf'
    urdf_path = Path(get_package_share_directory('innok_heros_description')) / 'urdf' / 'innok_heros_3w.urdf'
    
    # 读取 URDF 文件内容
    with open(urdf_path, 'r') as urdf_file:
        robot_description = urdf_file.read()

    # 配置 robot_state_publisher 节点
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    # 配置 gazebo 启动文件
    gazebo_launch = IncludeLaunchDescription(
        PathJoinSubstitution([
            get_package_share_directory('gazebo_ros'),
            'launch',
            'gazebo.launch.py'
        ])
    )

    # 配置 spawn_entity 节点
    spawn_entity_node = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "my_robot"],
        output="screen"
    )

    # 返回 LaunchDescription
    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_launch,
        spawn_entity_node
    ])

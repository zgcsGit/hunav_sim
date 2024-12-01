from launch import LaunchDescription
from pathlib import Path
import os
from ament_index_python.packages import get_package_share_path
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch_param_builder import load_xacro
import xacro
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():

    # 定义 xacro 文件的路径
    #urdf_path = Path(get_package_share_directory('innok_heros_description')) / 'urdf' / 'innok_heros_3w.xacro'
    #urdf_path=os.path.join(get_package_share_path('innok_heros_description'),'urdf','output.urdf')
    urdf_path=Path(os.path.join(
        get_package_share_directory('innok_heros_description'),
        'urdf',
        'innok_heros_3w.xacro',
    ))
    
    # 使用 load_xacro 来加载 xacro 文件并生成 URDF 内容
    #robot_description=xacro.process_file(urdf_path).toxml()
    robot_description=load_xacro(urdf_path)
    robot_description = ParameterValue(robot_description, value_type=str)
    

    #robot_description = ParameterValue(Command(['xacro',urdf_path]),value_type=str)
    #print("Robot Description:", robot_description)

    # 配置 robot_state_publisher 节点
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    # 配置 joint_state_publisher_gui 节点
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    # 配置 rviz2 节点
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2"
    )

    # 返回 LaunchDescription
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node
    ])

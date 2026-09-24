import math 
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class CosineTurtle(Node):
  def __init__(self):
    super().__init__('cosine_turtle')

    self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel',10)

    self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback,10)

    self.pose = None

    self.x_start = None
    self.y_start = None

    self.amp = 1.0
    self.freq = 2

    self.speed = 1.0

    self.timer = self.create_timer(.02, self.move_turtle)


    self.get_logger().info("cosine path strted")

  def pose_callback(self, pos_data):

        self.pose = pos_data

        if self.x_start is None:
            self.x_start = pos_data.x
            self.y_start = pos_data.y

            self.get_logger().info(f'Starting at (x,y) ({self.x_start:.2f}, {self.y_start:.2f})')

  def move_turtle(self):

      if self.pose is None:
          return

      x = self.pose.x
      y = self.pose.y
      theta = self.pose.theta

      amp = self.amp
      freq  = self.freq

      #plus y_start to off set in y direction
      #curr x - strt x to get the right loco in x direction
      #multiply by amp and freq to get the correct scale and stuff    
      # cos - 1 to make the starting point a peak otherwise it was starting at the mid and tried going up    
      final_y = self.y_start + amp * (math.cos(freq * (x - self.x_start)) - 1)

      #y = amp*cos(freq*x)
      #dy/dx = -amp*freq*sin(freq*x)
      slope = -amp*freq*math.sin(freq * (x - self.x_start))

      #convert slope into angle using sohcahtoa
      final_theta = math.atan(slope)

      change_angle = final_theta - theta

      #normalise the angle bw -pi and +pi
      change_angle = (change_angle + math.pi) % (2 * math.pi) - math.pi

      change_y = final_y - y

      command = Twist()

      command.linear.x = 0.0
      command.angular.z = 0.0

      command.linear.x = float(self.speed)
    #   command.angular.z = (change_angle*3 + change_y*1.5)
      command.angular.z = (change_angle*5 + change_y*2.5)


      # stop bfr hitting right wall
      if x > 10.0 or x < 1.0 or y > 10.0 or y < 1.0:

          command.linear.x= 0.0
          command.angular.z= 0.0

          self.publisher.publish(command)

          self.get_logger().info('Finished movement')

          self.timer.cancel()

          return

      # print("linear.x:", command.linear.x, type(command.linear.x))
      # print("linear.y:", command.linear.y, type(command.linear.y))
      # print("linear.z:", command.linear.z, type(command.linear.z))
      # print("angular.x:", command.angular.x, type(command.angular.x))
      # print("angular.y:", command.angular.y, type(command.angular.y))
      # print("angular.z:", command.angular.z, type(command.angular.z))

      self.publisher.publish(command)


def main(args=None):

    rclpy.init(args=args)

    node = CosineTurtle()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()


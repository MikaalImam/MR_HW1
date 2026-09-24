import rclpy

from std_msgs.msg import Char

from rclpy.node import Node

class CharPublisher(Node):
  def __init__(self):
    super().__init__('node_publisher') 

    self.publisher = self.create_publisher(Char, "char_topic", 15)

    commRate = 1

    self.timer = self.create_timer(commRate, self.send_char)

    self.counter = 0

  def send_char(self):
    user_char = input("Please enter a character: ")
    if len(user_char) != 1:
      self.get_logger().info("Please enter a single character")
      return
    
    char_publisher = Char()
    char_publisher.data = ord(user_char)

    self.publisher.publish(char_publisher)

    self.get_logger().info("Publisher node is publishing: %s" % user_char)


def main(args=None):
  rclpy.init(args=args)

  node_publisher = CharPublisher()

  #so it doesnt repeatedly ask for an input
  while rclpy.ok():
      node_publisher.send_char()
      rclpy.spin_once(node_publisher, timeout_sec=0)
      
  node_publisher.destroy_node()

  rclpy.shutdown()

if __name__ == '__main__':
  main()
import rclpy

from std_msgs.msg import Char

from rclpy.node import Node

class CharSubscriber(Node):
  def __init__(self):
    super().__init__("node_subsrciber")

    self.subscription = self.create_subscription(Char, "char_topic", self.recievechar, 15)

    self.subscription


  def recievechar(self, charsubscriber):
    recieved_char = chr(charsubscriber.data)

    self.get_logger().info("we recieved: %s"% recieved_char)



def main(args=None):
  rclpy.init(args=args)
  subscriber_node = CharSubscriber()
  rclpy.spin(subscriber_node)

  subscriber_node.destroy_node()

  rclpy.shutdown()


if __name__ == "__main__":
  main()



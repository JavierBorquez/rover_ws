import pygame
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class GamepadLabroverPublisher(Node):
    def __init__(self):
        super().__init__('gamepad_labrover_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.timer = self.create_timer(0.1, self.timer_callback)  # Check for input every 0.1 seconds
        self.mode = 3
        self.n_modes = 4

    def timer_callback(self):
        pygame.event.pump()
        left_x = self.joystick.get_axis(0)
        right_y= self.joystick.get_axis(4)
        button_square = self.joystick.get_button(3)

        if button_square == 1:
            self.mode += 1 # swithch mode
            if self.mode >= self.n_modes:
                self.mode = 0

        vx = 0.0; vy = 0.0; w = 0.0

        if self.mode == 0: # Mode 0: vx            
            vx = round(right_y * -1.8, 2)
        elif self.mode == 1: # Mode 1: vy
            vy = round(right_y * -0.045, 3)
        elif self.mode == 2: # Mode 2: w
            w = round(right_y * 3, 2)
        elif self.mode == 3: # Mode 3: vx, vy
            vx = round(right_y * -1.8, 2)
            vy = round(left_x * -0.045, 3)

        twist = Twist()
        twist.linear.x = vx; twist.linear.y = vy; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = w            
        self.publisher_.publish(twist)
        self.get_logger().info(f'Publishing vx: {vx}, vy: {vy}, w: {w}, Mode: {self.mode}')


def main(args=None):
    rclpy.init(args=args)
    gamepad_publisher = GamepadLabroverPublisher()
    rclpy.spin(gamepad_publisher)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gamepad_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

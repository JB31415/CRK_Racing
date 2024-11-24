import argparse
import time
from Video import VideoStreaming
from Command import COMMAND as cmd
from threading import Thread

class CarManager:
    def __init__(self):
        self.tcp = VideoStreaming()
        self.video_thread = None
        self.connected = False

    def connect(self, ip):
        if not self.connected:
            self.tcp.StartTcpClient(ip)
            self.tcp.socket1_connect(ip)
            self.connected = True
            print(f"Connected to {ip}")
        else:
            print("Already connected")

    def disconnect(self):
        if self.connected:
            self.tcp.StopTcpcClient()
            self.connected = False
            print("Disconnected")
        else:
            print("Not connected")

    def start_video(self, ip):
        if self.connected:
            if not self.video_thread:
                self.video_thread = Thread(target=self.tcp.streaming, args=(ip,))
                self.video_thread.start()
                self.tcp.sendData(cmd.CMD_VIDEO + cmd.CMD_START)
                print("Video started")
            else:
                print("Video already running")
        else:
            print("Not connected. Please connect first.")

    def stop_video(self):
        if self.connected:
            if self.video_thread:
                self.tcp.sendData(cmd.CMD_VIDEO + cmd.CMD_STOP)
                self.video_thread.join()
                self.video_thread = None
                print("Video stopped")
            else:
                print("Video not running")
        else:
            print("Not connected. Please connect first.")

def main():
    parser = argparse.ArgumentParser(description="Manage Freenove Raspberry Pi Mini Car")
    parser.add_argument("ip", help="IP address of the Raspberry Pi")
    parser.add_argument("action", choices=["connect", "disconnect", "video_on", "video_off"],
                        help="Action to perform")

    args = parser.parse_args()

    car_manager = CarManager()

    if args.action == "connect":
        car_manager.connect(args.ip)
    elif args.action == "disconnect":
        car_manager.disconnect()
    elif args.action == "video_on":
        car_manager.connect(args.ip)
        car_manager.start_video(args.ip)
    elif args.action == "video_off":
        car_manager.stop_video()
        car_manager.disconnect()

    # Keep the program running for a moment to allow threads to start/stop
    time.sleep(2)

if __name__ == "__main__":
    main()

# python manage_tool.py 192.168.1.100 connect
# python manage_tool.py 192.168.1.100 video_on
# python manage_tool.py 192.168.1.100 video_off
# python manage_tool.py 192.168.1.100 disconnect

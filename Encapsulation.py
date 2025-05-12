class TVRemote:
    def __init__(self):
        self.__infrared_signal = None

    def __generate_signal(self, command):
        # Private method (encapsulated)
        self.__infrared_signal = f"Infrared signal for {command}"
        print(f"Generated {self.__infrared_signal}")

    def change_channel(self, channel):
        # Public method (interface)
        self.__generate_signal(f"Change to Channel {channel}")
        print(f"Channel changed to {channel}")

    def adjust_volume(self, level):
        # Public method (interface)
        self.__generate_signal(f"Set Volume to {level}")
        print(f"Volume adjusted to {level}")

if __name__ == "__main__":
    remote = TVRemote()  # Create an instance of TVRemote
    remote.change_channel(5)    # Change the channel to 5
    remote.adjust_volume(10)    # Adjust the volume to level 10
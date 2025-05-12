from idlelib.debugobj_r import remote_object_tree_item


class TVRemote:
    def power(self):
        print("TV turned on/ off")

    def changeChannel(self, channel):
        print(f"Channel changed to {channel}")

    def adjustVolume(self, level):
        print(f"Volume adjusted to {level}")

if __name__ == "__main__":
    remote = TVRemote()
    remote.power()
    remote.adjustVolume(22)
    remote.changeChannel(5)

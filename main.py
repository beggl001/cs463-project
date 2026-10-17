import random



class Device():
    def __init__(self, name: str):
        self.name = name
        self.modulus = 0
        self.base = 0
        self.private_key = 0
        self.public_key = 0
        self.received_key = 0
        self.common_key = 0

    def set_modulus(self, p: int):
        self.modulus = p

    def set_base(self, g: int):
        self.base = g

    def prompt_for_secret(self):
        if self.modulus == 0:
            raise Exception()

        answer = input(f"Enter {self.name}'s secret key (1 to {self.modulus-1}), OR enter nothing to generate randomly: ")
        try:
            self.private_key = int(answer)
        except:
            self.private_key = random.randint(1, self.modulus-1)
            print(f"Randomly selected secret: {self.private_key}")
        self.generate_public_key()

    def generate_public_key(self):
        print("wa")
        self.public_key = self.base ** self.private_key % self.modulus
        print("wa")
        print(f"Public key generated: {self.base}^{self.private_key} mod {self.modulus} = {self.public_key}\n")

    def send_public_key_to[D: Device](self, device: D):
        device.receive_key(self.public_key)

    def receive_key(self, received):
        self.received_key = received
        self.common_key = self.received_key ** self.private_key % self.modulus
        print(f"{self.name} - Common secret key generated: {self.received_key}^{self.private_key} mod {self.modulus}")

    def print_known(self):
        print(f"""--- {self.name}'s known information: ---
Modulus:             {self.modulus or ""}
Base:                {self.base or ""}
Private key:         {self.private_key or ""}
My public key:       {self.public_key or ""}
Received public key: {self.received_key or ""}
Common secret key:   {self.common_key or ""}
""")


alice = Device("Alice")
bob = Device("Bob")

mode = input("Welcome! Enter \"local\" to run simulation on only this device; otherwise, two-device simulation will be chosen: ")

if mode == "local":
    print("Local mode chosen")
    preset = input("Enter \"small\" or \"large\" to decide preset: ")
else:
    print("Two-device mode chosen")
    preset = input("Enter \"small\" or \"large\" to decide preset.\n(IMPORTANT: Choose same option on other device): ")

if preset == "small":
    print(f"Simple preset chosen: modulus = 23, base = 5")
    alice.set_modulus(23)
    alice.set_base(5)
    bob.set_modulus(23)
    bob.set_base(5)
elif preset == "large":
    print("Large preset chosen: modulus = 115249, base = 58223")
    alice.set_modulus(115249)
    alice.set_base(5822)
    bob.set_modulus(115249)
    bob.set_base(5822)
else:
    raise Exception("Invalid argument")

print()

if mode == "local":
    alice.prompt_for_secret()
    bob.prompt_for_secret()
    alice.print_known()
    bob.print_known()

    input("(press enter)")

    print("The two devices send their public keys to each other.")
    alice.send_public_key_to(bob)
    bob.send_public_key_to(alice)
    alice.print_known()
    bob.print_known()

else: # two device mode
    name = ""
    while True:
        name = input("Would you like to be \"alice\" or \"bob\"?\n(Does not affect anything, only useful for making output consistent across devices): ")
        if name.lower() == "alice":
            me = alice
            other_name = "Bob"
            break
        if name.lower() == "bob":
            me = bob
            other_name = "Alice"
            break
        print("Invalid response")

    print()
    me.prompt_for_secret()
    me.print_known()
    me.receive_key(int(input(f"What is {other_name}'s PUBLIC key?: ")))
    me.print_known()
    print("Common secret key should be the same across both devices.")

print("Demo complete!")

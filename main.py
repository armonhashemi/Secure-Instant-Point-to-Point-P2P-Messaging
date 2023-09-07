from connection import server, client

if __name__ == "__main__":
    choice = input("Choose (s)erver or (c)lient: ")

    # Change these to be the ip address and an open port of the network you're connected to
    ip_address = '127.0.0.1'
    port = 50003
    # Use same ip address and port for both server and client
    # The program may give a 'Bad Public Key' or other error due to bad network transmission
    if choice.lower() == "s":
        server(ip_address, port)
    elif choice.lower() == "c":
        client(ip_address, port)


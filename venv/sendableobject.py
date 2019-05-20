class SendableObject(tuple):
    def __init__(self, *args):
        for arg in args:
            self.header = arg[0]
            self.data = arg[1]

    def get_header(self):
        return self.header

    def get_data(self):
        return self.data


class SendablePackage:
    def __init__(self, header = "Chat", parcel = "Chat member message"):
        self.header = header
        self.parcel = parcel

    # header value getter and setter
    def get_header_value(self):
        return self.header

    def set_header_value(self, text_value):
        self.header = text_value


    # parcel value getter and setter
    def get_parcel_value(self):
        return self.parcel

    def set_parcel_value(self, text_value):
        self.parcel = parcel_value


    def default_parcel(self):
        pack = [self.header, self.parcel]
        return pack

    # Helli newcomer Preset Package
    def hello_initial_package(self):
        return ["Hello", "HELLO NEWCOMER!!! \nPlease type your name and send it to the chat"]

    # Welcome user Preset Package
    def welcome_package(self, name):
        return ["Welcome", "Welcome %s!" % name]

    # New user has joined chat Preset Package
    def join_package(self, name):
        return ["Join", "%s has joined the chat!" % name]

    # Chat Preset Package
    def chat_package(self, name, parcel):
        return ["Chat", name + ": " + parcel]

    # Chat exit package
    def chat_exit_package(self, name):
        return ["Chat", "%s has left our chat." % name]

    # Picture announcing package
    def picture_package(self, data):
        return ["Picture", data]

    # Picture sending to server
    def picture_send_to_server(self, data):
        return ["Parcel", data]
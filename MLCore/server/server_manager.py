import logging
from abc import abstractmethod
import sys

from ..communication.gRPC.grpc_comm_manager import GRPCCommManager
from ..communication.observer import Observer


class ServerManager(Observer):
    def __init__(self, args, comm=None, rank=0, size=0, backend="MPI"):
        self.args = args
        self.size = size
        self.rank = rank

        self.backend = backend
        HOST = "0.0.0.0"
        PORT = 50000 + rank
        self.com_manager = GRPCCommManager(
            HOST, PORT, ip_config_path=args.grpc_ipconfig_path, client_id=rank, client_num=size - 1
        )
        self.com_manager.add_observer(self)
        self.message_handler_dict = dict()

    def run(self):
        self.register_message_receive_handlers()
        self.com_manager.handle_receive_message()

    def get_sender_id(self):
        return self.rank

    def receive_message(self, msg_type, msg_params) -> None:
        # logging.info("receive_message. rank_id = %d, msg_type = %s. msg_params = %s" % (
        #     self.rank, str(msg_type), str(msg_params.get_content())))
        handler_callback_func = self.message_handler_dict[msg_type]
        handler_callback_func(msg_params)

    def send_message(self, message):
        self.com_manager.send_message(message)

    @abstractmethod
    def register_message_receive_handlers(self) -> None:
        pass

    def register_message_receive_handler(self, msg_type, handler_callback_func):
        self.message_handler_dict[msg_type] = handler_callback_func

    def finish(self):
        logging.info("__finish server")
        self.com_manager.stop_receive_message()

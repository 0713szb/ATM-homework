from socket import *


def main():
    try:
        # 与服务器进行连接
        servername = '10.230.60.191'  # 我的IP地址
        serverport = 2525
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((servername, serverport))

        # 第一步：发送ID
        user_id = input("Enter your ID: ")
        client_socket.send(user_id.encode())

        # 接收服务器的响应 每次服务器发送响应，都要接受一次
        # 接受ID响应
        response = client_socket.recv(1024).decode()
        if response == "500 sp AUTH REQUIRED!":
            # 如果ID存在，提示输入密码
            print(response)
            # 发送密码
            user_password = input("Enter your password: ")
            client_socket.sendall(user_password.encode())

            # 接受password响应
            response = client_socket.recv(1024).decode()
            if response == "525 OK!":
                print(response)

                # 发送取款额
                user_withdraw = input("Enter withdraw:")
                client_socket.sendall(user_withdraw.encode())

                # 接受取款额响应
                response = client_socket.recv(1024).decode()

                # 取款失败
                if response <= user_withdraw:
                    print(response)

                # 取款成功
                else:
                    print(response)

                    # 发送结束语
                    user_over = input()
                    client_socket.sendall(user_over.encode())

                    # 接收结束语响应
                    response = client_socket.recv(1024).decode()
                    print(response)
                    client_socket.close()

        else:
            # 接收ID不正确响应
            print(response)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
